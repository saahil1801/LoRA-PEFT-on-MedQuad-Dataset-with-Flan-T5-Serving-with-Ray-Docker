# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install required packages
RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

# Expose the port that Ray Serve will run on
EXPOSE 8000 

EXPOSE 8265

# Expose the port that Streamlit will run on
EXPOSE 8501

# Copy the start script into the container
COPY start.sh /app/start.sh

# Make the script executable
RUN chmod +x /app/start.sh

# Use the script to start the application
CMD ["/app/start.sh"]