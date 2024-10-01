# views/question_views.py
from django.http import JsonResponse
from ..repositories import question_repository

# A function that calls the repository layer to create a question and returns a JsonResponse based on the result
def createQuestion(request):
    if request.method == 'POST':
        try:
            question_data = request.POST.dict()
            response = question_repository.create_question(question_data)
            return JsonResponse({"status": "success", "data": response.data})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)
    else:
        return JsonResponse({"status": "error", "message": "Only POST requests are allowed."}, status=400)
        
# A function that calls the repository layer to get all questions and returns a JsonResponse based on the result
def getAllQuestions(request):
    try:
        response = question_repository.get_all_questions()
        return JsonResponse({"status": "success", "data": response.data})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)
