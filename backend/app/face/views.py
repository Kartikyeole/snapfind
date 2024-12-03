from django.http import JsonResponse
from django.core.files.storage import default_storage
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import face_recognition
import boto3
import os
import asyncio
from django.core.files.base import ContentFile
import uuid
from .pinecone_client import PineconeClient
import logging
from .models import Users
from asgiref.sync import sync_to_async

# Constants
SIMILARITY_THRESHOLD = 0.9
logger = logging.getLogger(__name__)

# Initialize shared clients
s3_client = boto3.client(
    "s3",
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name=settings.AWS_S3_REGION_NAME,
)

pinecone_client = PineconeClient()



async def process_face(encoding, file_url):
    try:
        
        # Query Pinecone for similar faces
        query_results = pinecone_client.query_face_encoding(encoding)
        is_duplicate = False

        if query_results and query_results.matches:
            top_match = query_results.matches[0]
            if top_match.score >= SIMILARITY_THRESHOLD:
                user = await sync_to_async(Users.objects.get)(userID=top_match.id)
                await sync_to_async(user.add_file_url)(file_url)
                await sync_to_async(user.save)()    
                return {"is_duplicate": True}

        # Upsert encoding to Pinecone
        user_id = str(uuid.uuid4())
        user = Users(userID=user_id, file_urls=[file_url])
        await sync_to_async(user.save)()
        await sync_to_async(pinecone_client.upsert_face_encoding)(user_id, encoding)
        

        return {"is_duplicate": is_duplicate}
    except Exception as e:
        logger.error(f"Error processing face: {e}")
        raise


async def upload_to_s3(file_name):
    loop = asyncio.get_event_loop()
    file_path = default_storage.path(file_name)
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    region = settings.AWS_S3_REGION_NAME

    await loop.run_in_executor(
        None,
        s3_client.upload_file,
        file_path,
        bucket_name,
        file_name,
        {"ContentType": "image/jpeg"},
    )

    return f"https://{bucket_name}.s3.{region}.amazonaws.com/{file_name}"




@csrf_exempt
async def upload(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request"}, status=400)

    uploaded_file = request.FILES.get("file")
    if not uploaded_file:
        return JsonResponse({"error": "No file provided"}, status=400)

    file_name = f"{uuid.uuid4()}_{uploaded_file.name}"
    try:
        # Save file temporarily
        saved_path = default_storage.save(file_name, ContentFile(uploaded_file.read()))
        file_path = default_storage.path(saved_path)

        # Process image
        image = face_recognition.load_image_file(file_path)
        face_locations = face_recognition.face_locations(image)
        face_encodings = face_recognition.face_encodings(image, face_locations)

        if not face_encodings:
            raise ValueError("No faces detected")

        # Prepare results
        num_faces = len(face_encodings)
        same_face_count = 0
        new_face_count = 0
        tasks = []
        
        file_url = await upload_to_s3(file_name)

        for encoding in face_encodings:
            encoding_list = encoding.tolist()
            tasks.append(process_face(encoding_list, file_url))

        # Process faces concurrently
        results = await asyncio.gather(*tasks)

        for result in results:
            if result["is_duplicate"]:
                same_face_count += 1
            else:
                new_face_count += 1

        return JsonResponse(
            {
                "message": "Process completed",
                "num_faces": num_faces,
                "same_face_count": same_face_count,
                "new_face_count": new_face_count,
            },
            status=200,
        )

    except ValueError as ve:
        logger.error(f"Validation error: {ve}")
        return JsonResponse({"error": str(ve)}, status=400)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return JsonResponse({"error": "An error occurred: " + str(e)}, status=500)
    finally:
        if os.path.exists(default_storage.path(file_name)):
            default_storage.delete(file_name)
            

@csrf_exempt
async def find_face(request):
    if request.method != "POST":  # Corrected method type
        return JsonResponse({"error": "Invalid request"}, status=400)

    uploaded_file = request.FILES.get("file")
    if not uploaded_file:
        return JsonResponse({"error": "No file provided"}, status=400)

    file_name = f"{uuid.uuid4()}_{uploaded_file.name}"
    try:
        # Save file temporarily
        saved_path = default_storage.save(file_name, ContentFile(uploaded_file.read()))
        file_path = default_storage.path(saved_path)

        # Process image using face_recognition
        image = face_recognition.load_image_file(file_path)
        face_locations = face_recognition.face_locations(image)  # 'hog' for faster detection
        if not face_locations:
            raise ValueError("No faces detected in the image.")

        face_encodings = face_recognition.face_encodings(image, face_locations)
        if len(face_encodings) > 1:
            raise ValueError("Multiple faces detected in the image. Provide a single-face selfie.")

        # Query the Pinecone index for matches
        encoding = face_encodings[0].tolist()
        query_results = pinecone_client.query_face_encoding(encoding, top_k=1)

        # Check for matches with the similarity threshold
        if query_results and query_results.matches:
            top_match = query_results.matches[0]
            if top_match.score > SIMILARITY_THRESHOLD:
                user_id = str(top_match.id)
                sore = top_match.score
                
                user = await sync_to_async(Users.objects.get)(userID=user_id)
                file_url = user.file_urls
                return JsonResponse({"files": file_url,"score":sore}, status=200)

        return JsonResponse({"message": "No matching faces found."}, status=200)

    except ValueError as ve:
        logger.warning(f"Validation error: {ve}")
        return JsonResponse({"error": str(ve)}, status=400)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return JsonResponse({"error": "An error occurred: " + str(e)}, status=500)
    finally:
        # Clean up the saved file
        if default_storage.exists(file_name):
            default_storage.delete(file_name)
            
            
@csrf_exempt
async def find_face_list(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request"}, status=400)
    
    uploaded_file = request.FILES.get("file")
    if not uploaded_file:
        return JsonResponse({"error": "No file provided"}, status=400)
    
    
    file_name = f"{uuid.uuid4()}_{uploaded_file.name}"
    try:
        # Save file temporarily
        saved_path = default_storage.save(file_name, ContentFile(uploaded_file.read()))
        file_path = default_storage.path(saved_path)

        # Process image using face_recognition
        image = face_recognition.load_image_file(file_path)
        face_locations = face_recognition.face_locations(image, model="hog")  # 'hog' for faster detection
        if not face_locations:
            raise ValueError("No faces detected in the image.")

        face_encodings = face_recognition.face_encodings(image, face_locations)
        if len(face_encodings) > 1:
            raise ValueError("Multiple faces detected in the image. Provide a single-face selfie.")

        # Query the Pinecone index for matches
        encoding = face_encodings[0].tolist()
        
        query_results = pinecone_client.query_face_encoding_list(encoding)
        
        

        # # Check for matches with the similarity threshold
        # if query_results and query_results.matches:
        #     top_match = query_results.matches[0]
        #     if top_match.score > SIMILARITY_THRESHOLD:
        #         user_id = str(top_match.id)
        #         sore = top_match.score
                
        #         user = await sync_to_async(Users.objects.get)(userID=user_id)
        #         file_url = user.file_urls
        #         return JsonResponse({"files": file_url,"score":sore}, status=200)

        return JsonResponse({"message": query_results }, status=200)

    except ValueError as ve:
        logger.warning(f"Validation error: {ve}")
        return JsonResponse({"error": str(ve)}, status=400)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return JsonResponse({"error": "An error occurred: " + str(e)}, status=500)
    finally:
        # Clean up the saved file
        if default_storage.exists(file_name):
            default_storage.delete(file_name)
    
    
