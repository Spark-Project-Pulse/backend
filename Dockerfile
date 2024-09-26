# Use an official Python runtime as a base image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project code into the container
COPY . .

# Expose the port that the Django app will run on
EXPOSE 8080

# Set the default command to run the Django app (or you can use a WSGI server like gunicorn)
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "backend.wsgi:application"]