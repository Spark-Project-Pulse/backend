# backend

## To run this project locally
### Docker 
1. Make sure the Docker daemon is running (open Docker Desktop)
2. Use this command to run the project locally:
   ``` bash
   docker compose up --build
   ```
3. Navigate to `http://localhost:8080` to view the project

### Django
1. **Install Pipenv** (if not already installed):
   ```bash
   pip install pipenv
2. Install the project dependencies using Pipenv:
   ``` bash
   pipenv install --dev
   ```
3. Activate the Pipenv virtual environment:
   ``` bash
   pipenv shell
   ```
4. Run the Django development server locally:
   ``` bash
   python manage.py runserver
   ```
