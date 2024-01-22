# Use the official Python 3.10 image
FROM python:3.11-slim-bullseye

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create a non-root user
RUN useradd -m appuser

# Copy all files into the container
COPY . .

# Give the non-root user ownership of the files
RUN chown -R appuser:appuser /app

# Change to the non-root user
USER appuser

# Delete the .env file
RUN rm -f .env
# Run main.py when the container starts
CMD ["python", "-OO", "main.py"]
