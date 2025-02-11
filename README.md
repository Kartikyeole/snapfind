# SnapFind

SnapFind is a project that leverages AWS Rekognition and DynamoDB to detect and recognize faces in images. It uses a serverless architecture with AWS Lambda functions to process images and store metadata in DynamoDB. The project also includes a frontend built with Next.js for uploading images and viewing results.

## Getting Started

### Prerequisites

- AWS account with access to Rekognition, S3, and DynamoDB
- Node.js and npm installed
- Python and pip installed
- Docker installed

### Setup

1. Clone the repository:

```bash
git clone https://github.com/Kartikyeole/snapfind.git
cd snapfind
```

2. Set up environment variables:

Create a `.env` file in the root directory and add the following variables:

```env
AWS_ACCESS_KEY_ID=your_aws_access_key_id
AWS_SECRET_ACCESS_KEY=your_aws_secret_access_key
AWS_STORAGE_BUCKET_NAME=your_s3_bucket_name
AWS_S3_REGION_NAME=your_s3_region_name
REKOGNITION_COLLECTION_ID=your_rekognition_collection_id
DYNAMODB_TABLE=your_dynamodb_table_name
PINECONE_API_KEY=your_pinecone_api_key
PROJECT_DEBUG=True
```

3. Install backend dependencies:

```bash
cd backend/app
pip install -r requirements.txt
```

4. Install frontend dependencies:

```bash
cd ../../froentend
npm install
```

5. Run the backend:

```bash
cd ../backend/app
docker-compose up
```

6. Run the frontend:

```bash
cd ../../froentend
npm run dev
```

## Usage

### Uploading an Image

1. Open the frontend application in your browser at `http://localhost:3000`.
2. Use the upload form to select and upload an image.
3. The image will be processed by the backend, and the results will be displayed.

### Finding a Face

1. Open the frontend application in your browser at `http://localhost:3000`.
2. Use the find face form to select and upload an image.
3. The backend will search for matching faces and display the results.

## Contributing

We welcome contributions to SnapFind! To contribute, follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Make your changes and commit them with a descriptive message.
4. Push your changes to your fork.
5. Open a pull request to the main repository.

Please ensure your code follows the project's coding standards and includes tests for any new functionality.
