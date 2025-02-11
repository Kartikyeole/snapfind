import boto3
import os
import json

# Initialize AWS services
s3 = boto3.client('s3')
rekognition = boto3.client('rekognition')
dynamodb = boto3.resource('dynamodb')

# Environment variables
COLLECTION_ID = os.getenv('REKOGNITION_COLLECTION_ID')
DYNAMODB_TABLE = os.getenv('DYNAMODB_TABLE')

def lambda_handler(event, context):

    try:
        for record in event['Records']:
            bucket_name = record['s3']['bucket']['name']
            image_key = record['s3']['object']['key']

            # Detect faces in the image
            rekognition_response = rekognition.index_faces(
                CollectionId=COLLECTION_ID,
                Image={'S3Object': {'Bucket': bucket_name, 'Name': image_key}},
                ExternalImageId=image_key,
                DetectionAttributes=['DEFAULT']
            )

            face_records = rekognition_response.get('FaceRecords', [])
            if not face_records:
                print(f"No faces detected in image: {image_key}")
                continue

            # Focus only on confident faces (Confidence > 98%)
            confident_faces = [
                face_record for face_record in face_records
                if face_record['Face']['Confidence'] > 98
            ]

            if not confident_faces:
                print(f"No sufficiently confident faces found in image: {image_key}")
                continue

            # Update DynamoDB for each unique face
            table = dynamodb.Table(DYNAMODB_TABLE)
            for face_record in confident_faces:
                face_id = face_record['Face']['FaceId']

                # Search for similar faces in the collection
                search_response = rekognition.search_faces(
                    CollectionId=COLLECTION_ID,
                    FaceId=face_id,
                    MaxFaces=1,
                    FaceMatchThreshold=99  # Match threshold set to 99%
                )

                face_matches = search_response.get('FaceMatches', [])
                if face_matches:
                    # Face already exists in the database
                    matched_face_id = face_matches[0]['Face']['FaceId']

                    # Retrieve existing metadata
                    response = table.get_item(Key={'face_ID': matched_face_id})
                    item = response.get('Item', {})
                    image_keys = item.get('ImageKeys', [])

                    # Update metadata if the image URL is new
                    if image_key not in image_keys:
                        image_keys.append(image_key)
                        table.put_item(
                            Item={
                                'face_ID': matched_face_id,
                                'ImageKeys': image_keys
                            }
                        )
                        print(f"Metadata updated for FaceId: {matched_face_id}")
                    else:
                        print(f"Image already associated with FaceId: {matched_face_id}")
                else:
                    # Face is unique, add new entry to the database
                    table.put_item(
                        Item={
                            'face_ID': face_id,
                            'ImageKeys': [image_key]
                        }
                    )
                    print(f"New face added to database with FaceId: {face_id}")
        return {"statusCode": 200, "body": "Processing complete"}

    except KeyError as e:
        print(f"KeyError: {e}")
        return {"statusCode": 400, "body": f"Invalid event structure: {e}"}
    except Exception as e:
        print(f"Unexpected error: {e}")
        return {"statusCode": 500, "body": f"Internal server error: {e}"}
