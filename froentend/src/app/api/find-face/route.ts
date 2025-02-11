import { NextRequest, NextResponse } from 'next/server';

const API_GATEWAY_URL = process.env.API_GATEWAY_URL_FIND_FACE as string;

export const POST = async (req: NextRequest) => {
  try {
    if (!API_GATEWAY_URL) {
      throw new Error('API_GATEWAY_URL_FIND_FACE environment variable is not set.');
    }

    // Parse the form data
    const contentType = req.headers.get('content-type') || '';
    if (!contentType.includes('multipart/form-data')) {
      return NextResponse.json({ error: 'Invalid content type' }, { status: 400 });
    }

    const formData = await req.formData();
    const file = formData.get('file') as File | null;

    if (!file) {
      return NextResponse.json({ error: 'No file provided' }, { status: 400 });
    }

    // Convert the file to a Base64 string
    const arrayBuffer = await file.arrayBuffer();
    if (!arrayBuffer) {
      throw new Error('Failed to read file content.');
    }

    const base64String = Buffer.from(new Uint8Array(arrayBuffer)).toString('base64');

    // Prepare the payload
    const payload = {
      imgBase64: base64String,
    };

    // Send a POST request to the API Gateway
    const response = await fetch(API_GATEWAY_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      const errorResponse = await response.text();
      return NextResponse.json(
        { error: 'Failed to send image to API Gateway', details: errorResponse },
        { status: response.status }
      );
    }

    const result = await response.json();

    return NextResponse.json({ message: 'Image processed successfully', result });
  } catch (error: unknown) {
    return NextResponse.json(
      { error: 'Something went wrong', details: (error as Error).message },
      { status: 500 }
    );
  }
};
