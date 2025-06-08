# Use the official Python image as the base image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Create and activate virtual environment
RUN python -m venv /app/venv
ENV PATH="/app/venv/bin:$PATH"

# Copy the requirements file first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose port 5006 for the fast api app
EXPOSE 5006

# Run the Flask app using Uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5006"]
