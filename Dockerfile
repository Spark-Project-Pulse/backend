# Use an official Python runtime as a base image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the Pipfile and Pipfile.lock
COPY Pipfile Pipfile.lock ./

# Install Pipenv and the project dependencies system-wide
RUN pip install --no-cache-dir pipenv && \
    pipenv install --system --deploy --ignore-pipfile

# Copy the entire project code into the container
COPY . .

# Ensure that pipenv does not try to use virtualenvs in runtime
ENV PIPENV_VENV_IN_PROJECT=1

# Expose the port the app runs on
EXPOSE 8000

# Default command to run the application
CMD ["gunicorn", "backend.wsgi:application"]