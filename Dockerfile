# Use an official Python runtime as a base image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV PORT 8080
EXPOSE 8080

# Set the working directory in the container
WORKDIR /app

# Copy the Pipfile and Pipfile.lock
COPY Pipfile Pipfile.lock ./

# Install Pipenv and the project dependencies
RUN pip install --no-cache-dir pipenv && \
    pipenv install --system --deploy --ignore-pipfile && \
    pipenv install supabase

# Copy the entire project code into the container
COPY . .

CMD ["pipenv", "run", "gunicorn", "--bind", "0.0.0.0:8080", "backend.wsgi:application"]
