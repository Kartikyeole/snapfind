"use client";

import { useState, ChangeEvent } from "react";

const UploadImage: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);
  const [message, setMessage] = useState<string>("");

  const handleFileChange = (e: ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      setFile(e.target.files[0]);
    }
  };

  const uploadFile = async () => {
    if (!file) {
      setMessage("Please select a file to upload.");
      return;
    }

    try {
      // Request a presigned URL from the API
      const response = await fetch("/api/generate-presigned-url", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ fileName: file.name, fileType: file.type }),
      });

      if (!response.ok) {
        throw new Error("Failed to generate presigned URL");
      }

      const { url } = await response.json();

      

      // Upload the file directly to S3
      const uploadResponse = await fetch(url, {
        method: "PUT",
        body: file,
        headers: { "Content-Type": file.type },
      });

      if (uploadResponse.ok) {
        setMessage("File uploaded successfully!");
      } else {
        throw new Error("Failed to upload file");
      }
    } catch (error) {
      console.error("Upload error:", error);
      setMessage("An error occurred during upload.");
    }
  };

  return (
    <div>
      <input type="file" onChange={handleFileChange} />
      <button onClick={uploadFile}>Upload</button>
      {message && <p>{message}</p>}
    </div>
  );
};

export default UploadImage;
