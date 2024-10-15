# Use the official Python image from the Docker Hub
FROM --platform=$BUILDPLATFORM python:3.12.3

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy Promtail config
COPY promtail/config.yaml /etc/promtail/config.yaml

# Make port 8080 available to the world outside this container
EXPOSE 8080

# Start uvicorn server and Promtail simultaneously
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port 8080"]
