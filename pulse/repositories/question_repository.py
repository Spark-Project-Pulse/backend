# NOTE: commenting out this file (for now), as we are using the Django ORM instead (can bring this back if needed)

# # repositories/question_repository.py
# from ..supabase_utils import get_supabase_client

# # Create the supabase client
# supabase = get_supabase_client()

# # A function that creates a question in the Questions table within Supabase, throws an exception if an error occurs
# def create_question(question_data):
#     try:
#         response = supabase.table('Questions').insert(question_data).execute()
#         return response
#     except Exception as e:
#         raise Exception(f"Error creating question: {str(e)}")

# # A function that returns all the questions stored in the Questions table within Supabase, throws an exception if an error occurs
# def get_all_questions():
#     try:
#         response = supabase.table('Questions').select('*').execute()
#         return response
#     except Exception as e:
#         raise Exception(f"Error fetching questions: {str(e)}")

# # A function that returns the question matching the question_id stored in the Questions table within Supabase, throws an exception if an error occurs
# def get_question_by_id(question_id):
#     try:
#         response = supabase.table('Questions').select('*').eq('question_id', question_id).execute()
#         return response
#     except Exception as e:
#         raise Exception(f"Error fetching question: {str(e)}")
