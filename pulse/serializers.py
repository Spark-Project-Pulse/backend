from rest_framework import serializers
from .models import *

# NOTE: Each model should have a corresponding serializer to handle validation and
# conversion of incoming data, as well as serializing outgoing data to be
# returned in responses.

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'
        
    def to_representation(self, instance):
        # Modify the reputation value to be at least 0
        representation = super().to_representation(instance)
        
        # If the reputation is below 0, set it to 0 in the representation
        if representation.get('reputation', 0) < 0:
            representation['reputation'] = 0
        
        return representation
    
class UserRolesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRoles
        fields = '__all__'
        
class AnswerSerializer(serializers.ModelSerializer):
    # This allows us to get the user info of the answerer as a dictionary, based on the expert_id (for GET requests)
    expert_info = UserSerializer(source='expert', read_only=True)
    
    class Meta:
        model = Answers
        fields = '__all__'  # or specify the fields you want

    from rest_framework import serializers
from .models import *
from django.db.models import F

class AnswerSerializer(serializers.ModelSerializer):
    # Include expert info
    expert_info = UserSerializer(source='expert', read_only=True)
    # Add expert_badges field
    expert_badges = serializers.SerializerMethodField()
    
    class Meta:
        model = Answers
        fields = '__all__'  # Ensure 'expert_badges' is included if you're specifying fields explicitly

    def get_expert_badges(self, obj):
        # Get the expert user
        user = obj.expert
        if user:
            # Get the tags associated with the question
            question_tags = obj.question.tags.all()
            # Get the relevant badges associated with those tags
            relevant_badges = user.userbadge_set.filter(
                badge__associated_tag__in=question_tags
            ).select_related('badge')
            # Serialize the badges
            badges = []
            for user_badge in relevant_badges:
                badge = user_badge.badge
                badges.append({
                    'badge_id': badge.badge_id,
                    'name': badge.name,
                    'description': badge.description,
                    'image_url': badge.image_url
                })
            return badges
        return []

        
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
        
class CommunitySerializer(serializers.ModelSerializer):
    rank = serializers.FloatField(read_only=True)
    owner_info = UserSerializer(source='owner', read_only=True)
    
    class Meta:
        model = Communities
        fields = '__all__'

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = '__all__'

class QuestionSerializer(serializers.ModelSerializer):
    # This allows us to get the user info of the asker as a dictionary, based on the asker_id (for GET requests)
    asker_info = UserSerializer(source='asker', read_only=True)
    rank = serializers.FloatField(read_only=True)
    related_project_info = ProjectSerializer(source='related_project', read_only=True)
    related_community_info = CommunitySerializer(source='related_community', read_only=True)
    
    class Meta:
        model = Questions
        fields = '__all__'

class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Votes
        fields = '__all__'
        
class CommunityMemberSerializer(serializers.ModelSerializer):
    # This allows us to get the community info as a dictionary, based on the community_id (for GET requests)
    community_info = CommunitySerializer(source='community', read_only=True)
    # This allows us to get the user info as a dictionary, based on the user_id (for GET requests)
    user_info = UserSerializer(source='user', read_only=True)
    
    class Meta:
        model = CommunityMembers
        fields = '__all__'
    
    def to_representation(self, instance):
        # Modify the community reputation value to be at least 0
        representation = super().to_representation(instance)
        
        # If the community reputation is below 0, set it to 0 in the representation
        if representation.get('community_reputation', 0) < 0:
            representation['community_reputation'] = 0
        
        return representation
    

class NotificationSerializer(serializers.ModelSerializer):
    recipient_info = UserSerializer(source='recipient', read_only=True)
    question_info = QuestionSerializer(source='question', read_only=True)
    answer_info = AnswerSerializer(source='answer', read_only=True)
    comment_info = CommentSerializer(source='comment', read_only=True)
    actor_info = UserSerializer(source='actor', read_only=True)
    community_info = CommunitySerializer(source='community', read_only=True)

    class Meta:
        model = Notifications
        fields = '__all__'

class BadgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Badge
        fields = ['badge_id', 'name', 'description', 'image_url']


class UserBadgeSerializer(serializers.ModelSerializer):
    badge_info = BadgeSerializer(source='badge', read_only=True)

    class Meta:
        model = UserBadge
        fields = '__all__'


class UserBadgeProgressSerializer(serializers.ModelSerializer):
    badge_info = BadgeSerializer(source='badge', read_only=True)
    class Meta:
        model = UserBadgeProgress
        fields = '__all__'