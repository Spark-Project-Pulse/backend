# Use an official Python runtime as a base image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV PORT 8080

# Set the working directory in the container
WORKDIR /app

# Copy the Pipfile and Pipfile.lock
COPY Pipfile Pipfile.lock ./

# Install Pipenv and the project dependencies
RUN pip install --no-cache-dir pipenv && \
    pipenv install --deploy --ignore-pipfile && \
    pipenc install supabase

# Copy the entire project code into the container
COPY . .

# Expose the port that the Django app will run on
EXPOSE 8080

# Set the default command to run the Django app (or you can use a WSGI server like gunicorn)
CMD ["pipenv", "run", "gunicorn", "--bind", "0.0.0.0:8080", "backend.wsgi:application"]
