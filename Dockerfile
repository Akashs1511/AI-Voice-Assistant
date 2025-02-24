# Use official Python image
FROM python:3.10

# Set the working directory inside the container
WORKDIR /app

# Copy project files into the container
COPY requirements.txt /app/
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the FastAPI port (8000)
EXPOSE 8000

# Run the FastAPI application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
