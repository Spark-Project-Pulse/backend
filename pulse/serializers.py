from rest_framework import serializers
from .models import Questions
from .models import Answers
from .models import Questions, Projects

# NOTE: Each model should have a corresponding serializer to handle validation and
# conversion of incoming data, as well as serializing outgoing data to be
# returned in responses.

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Questions
        fields = '__all__'  # or specify the fields you want


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answers
        fields = '__all__'  # or specify the fields you want
class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projects
        fields = '__all__'
