# Use official Python image as base
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy application files
COPY . /app

# Install package and dependencies
RUN pip install --no-cache-dir .

# Expose port for FastAPI
EXPOSE 8000

# Command to run FastAPI server
CMD ["uvicorn", "pwnagebox.app:app", "--host", "0.0.0.0", "--port", "8000"]
