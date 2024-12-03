# Base Image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Install system dependencies for face recognition and OpenCV
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    libboost-dev \
    libboost-system-dev \
    libboost-filesystem-dev \
    libboost-python-dev \
    libopenblas-dev \
    liblapack-dev \
    libjpeg-dev \
    libpng-dev \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    libatlas-base-dev \
    libfontconfig1 \
    libx11-dev \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN py manage.py createsuperuser

# Copy project files
COPY . .

# Collect static files (optional for production)
# RUN python manage.py collectstatic --noinput

# Expose the application port
EXPOSE 8000

# Command to run the application
CMD ["sh", "-c", "python manage.py runserver 0.0.0.0:8000"]
