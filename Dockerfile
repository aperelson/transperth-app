# Use a small Python base image
FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# Copy requirements file first (for caching layers)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the actual app code
COPY . .

# Expose the Flask port
EXPOSE 5000

# Set environment variables (optional: avoids warnings)
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Run the Flask app
CMD ["python", "app.py"]
