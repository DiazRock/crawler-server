# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Extra libraries for Pyppeteer
RUN apt update
RUN apt install -y gnupg2 wget
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN echo 'deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main' | tee /etc/apt/sources.list.d/google-chrome.list
RUN apt update
RUN apt install -y google-chrome-stable

# Copy the current directory contents into the container at /app
COPY . /app

# Set the working directory in the container
WORKDIR /app

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Install uvicorn
RUN pip install uvicorn

# Make the screenshots directory in the container
RUN mkdir -p screenshots_folder

RUN chmod 755 screenshots_folder
RUN chown $USER:$USER screenshots_folder
# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run uvicorn server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]