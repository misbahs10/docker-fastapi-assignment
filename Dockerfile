
# Use official Python image (python base image selected based on your requirements)
FROM python:3.12-slim

# Set working directory (Container ke andar working directory banata hai)
WORKDIR /app

# Copy requirements (files container main copty kerta hai)
COPY requirements.txt .

# Install dependencies (dependencies intall kerta hai)
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY main.py .

# Expose application port (Application port document karta hai)
EXPOSE 8000

# Run FastAPI application (Container start hone par application run karta hai)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
