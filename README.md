# backend

## To run this project locally
### Docker 
1. Make sure the Docker daemon is running (open Docker Desktop)
2. Use the command `docker compose up --build` to run the project locally
3. Navigate to `http://localhost:8080` to view the project

### Django
1. Set up the virtual environment with the command `python -m venv venv`
2. Activate the virtual environment with the command `source venv/bin/activate`
3. Install the requirements with the command `pip install -r requirements.txt`
4. Use the command `python manage.py runserver 0.0.0.0:8080` to run the project locally