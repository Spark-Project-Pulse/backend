from rest_framework import serializers
from .models import Questions
from .models import Answers

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Questions
        fields = '__all__'  # or specify the fields you want


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answers
        fields = '__all__'  # or specify the fields you want