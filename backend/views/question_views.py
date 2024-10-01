# views/question_views.py
from django.http import JsonResponse
from ..repositories import question_repository

# A function that calls the repository layer to get all questions and returns a JsonResponse based on the result
def getAllQuestions(request):
    try:
        response = question_repository.get_all_questions()
        return JsonResponse({"status": "success", "data": response.data})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)
