# Use an official Python runtime as a base image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONUNBUFFERED 1
# Remove hardcoded PORT value and rely on Google Cloud Run's PORT
# ENV PORT 8080

# Set the working directory in the container
WORKDIR /app

# Copy the Pipfile and Pipfile.lock
COPY Pipfile Pipfile.lock ./

# Install Pipenv and the project dependencies
RUN pip install --no-cache-dir pipenv && \
    pipenv install --deploy --ignore-pipfile

# Copy the entire project code into the container
COPY . .

# Expose the port (not required by Cloud Run but for local development)
EXPOSE 8080

# Set the default command to run the Django app using Gunicorn, 
# binding to the dynamic PORT provided by Google Cloud Run.
CMD ["pipenv", "run", "gunicorn", "--bind", "0.0.0.0:${PORT:-8080}", "backend.wsgi:application"]
