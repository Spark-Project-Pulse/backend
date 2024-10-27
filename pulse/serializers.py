from rest_framework import serializers
from .models import Answers, Questions, Projects, Users, Comments, Tags

# NOTE: Each model should have a corresponding serializer to handle validation and
# conversion of incoming data, as well as serializing outgoing data to be
# returned in responses.

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'
        
class AnswerSerializer(serializers.ModelSerializer):
    # This allows us to get the user info of the answerer as a dictionary, based on the expert_id (for GET requests)
    expert_info = UserSerializer(source='expert', read_only=True)
    
    class Meta:
        model = Answers
        fields = '__all__'  # or specify the fields you want
        
class CommentSerializer(serializers.ModelSerializer):
    # This allows us to get the user info of the commenter as a dictionary, based on the expert_id (for GET requests)
    expert_info = UserSerializer(source='expert', read_only=True)
    
    class Meta:
        model = Comments
        fields = '__all__' 
        
class ProjectSerializer(serializers.ModelSerializer):
   # This allows us to get the user info of the owner as a dictionary, based on the owner_id (for GET requests)
    owner_info = UserSerializer(source='owner', read_only=True)
    
    class Meta:
        model = Projects
        fields = '__all__'

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = '__all__'

class QuestionSerializer(serializers.ModelSerializer):
    # This allows us to get the user info of the asker as a dictionary, based on the asker_id (for GET requests)
    asker_info = UserSerializer(source='asker', read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    rank = serializers.FloatField(read_only=True)
    
    class Meta:
        model = Questions
        fields = '__all__'

