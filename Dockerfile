# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Copy the current directory contents into the container at /app
COPY . /app

# Set the working directory in the container
WORKDIR /app

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Install uvicorn
RUN pip install uvicorn

# Make the screenshots directory in the container
RUN mkdir -p /screenshots

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run uvicorn server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]