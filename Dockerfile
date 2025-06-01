# Use official Python base image
FROM python:3.11-slim

# Set work directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Expose port (Flask default: 5000)
EXPOSE 5000

# Start the app
CMD ["python", "app.py"]
