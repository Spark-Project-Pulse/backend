# repositories/question_repository.py
from ..supabase_utils import get_supabase_client

# Create the supabase client
supabase = get_supabase_client()

# A function that returns all the questions stored within the Questions table within Supabase, throws an exception if an error occurs
def get_all_questions():
    try:
        response = supabase.table('Questions').select('*').execute()
        return response
    except Exception as e:
        raise Exception(f"Error fetching questions: {str(e)}")
