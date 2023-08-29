# Use a Python base image
FROM python:3.11.4-slim-buster

# Set the working directory
WORKDIR /app

# Copy Node.js package files and install dependencies
COPY package.json package-lock.json ./
RUN apt-get update && apt-get install -y nodejs npm
RUN npm install

# Copy the rest of your application files
COPY . .

# Create a Python virtual environment and activate it
RUN python -m venv venv
RUN /bin/bash -c "source venv/bin/activate"

# Install Python dependencies
RUN pip install -r requirements.txt

# Perform migration
RUN python manage.py migrate

# Create a superuser
# RUN python manage.py createsuperuser

# Set the command to run your application
CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]
