# Use the official Python image from the Docker Hub
FROM python:3.12.3

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install Promtail
RUN wget https://github.com/grafana/loki/releases/download/v2.5.0/promtail-linux-amd64.zip && \
    unzip promtail-linux-amd64.zip && \
    mv promtail-linux-amd64 /usr/local/bin/promtail && \
    chmod +x /usr/local/bin/promtail

# Copy Promtail config
COPY promtail/config.yaml /etc/promtail/config.yaml

# Make port 8080 available to the world outside this container
EXPOSE 8080

# Run uvicorn server and Promtail when the container launches
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port 8080 & promtail -config.file=/etc/promtail/config.yaml"]
