import json
import base64
import os
import boto3

rekognition = boto3.client('rekognition')
dynamodb = boto3.resource('dynamodb')  # Use boto3.resource for DynamoDB table operations

COLLECTION_ID = os.getenv('REKOGNITION_COLLECTION_ID')
DYNAMODB_TABLE = os.getenv('DYNAMODB_TABLE')

def lambda_handler(event, context):    
    # Check for body in the request
    body = event.get('body', None)
    if not body:
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'No body data provided'}),
            'headers': {'Content-Type': 'application/json'}
        }
    
    body = json.loads(body)
    imgBase64 = body.get('imgBase64', None)
    if not imgBase64:
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'No imgBase64 provided'}),
            'headers': {'Content-Type': 'application/json'}
        }
    
    try:
        # Rekognition search_faces_by_image
        rekognition_response = rekognition.search_faces_by_image(
            CollectionId=COLLECTION_ID,
            Image={'Bytes': base64.b64decode(imgBase64)},
            MaxFaces=1,
            FaceMatchThreshold=70.0
        )

        face_matches = rekognition_response.get('FaceMatches', [])
        if not face_matches:
            return {
                'statusCode': 404,
                'body': json.dumps({'message': 'No matching face found'}),
                'headers': {'Content-Type': 'application/json'}
            }
        
        # Extract FaceId
        face_id = face_matches[0]['Face']['FaceId']
        print(f"Face ID: {face_id}")
        
        # Rekognition search_faces
        search_response = rekognition.search_faces(
            CollectionId=COLLECTION_ID,
            FaceId=face_id,
            MaxFaces=1,
            FaceMatchThreshold=99
        )

        print(f"Search Response: {search_response}")

        matched_faces = search_response.get('FaceMatches', [])
        print(f"Matched Faces: {matched_faces}")
        if not matched_faces:
            return {
                'statusCode': 404,
                'body': json.dumps({'message': 'No similar face found'}),
                'headers': {'Content-Type': 'application/json'}
            }

        matched_face_id = matched_faces[0]['Face']['FaceId']
        
        # Query DynamoDB
        table = dynamodb.Table(DYNAMODB_TABLE)
        response = table.get_item(Key={'face_ID': matched_face_id})
        item = response.get('Item', {})

        # Check if the record exists in DynamoDB
        if not item:
            return {
                'statusCode': 404,
                'body': json.dumps({'message': 'Face data not found in DynamoDB'}),
                'headers': {'Content-Type': 'application/json'}
            }
        image_urls = item.get('ImageKeys', [])
        
        # Successful response
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Face matched successfully',
                'data': image_urls
            }),
            'headers': {'Content-Type': 'application/json'}
        }
    
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Internal Server Error', 'error': str(e)}),
            'headers': {'Content-Type': 'application/json'}
        }
