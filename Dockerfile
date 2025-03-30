# Use a Python base image (adjust version as needed)
FROM python:3.12.4-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the model files into the container
COPY models/ridge.pkl ./models/ridge.pkl
COPY models/scaler.pkl ./models/scaler.pkl

# Copy the application files into the container
COPY . .

# Expose the port that Flask will run on
EXPOSE 8080

# Set the environment variable for Flask to run in production mode
ENV FLASK_APP=main.py

# Run the Flask application
CMD ["python", "main.py"]
