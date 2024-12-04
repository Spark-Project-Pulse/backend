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
    
class BadgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Badge
        fields = ['badge_id', 'name', 'description', 'image_url']

class BadgeTierSerializer(serializers.ModelSerializer):
    class Meta:
        model = BadgeTier
        fields = ['tier_level', 'name', 'description', 'image_url', 'reputation_threshold']

class UserBadgeSerializer(serializers.ModelSerializer):
    badge_info = BadgeSerializer(source='badge', read_only=True)
    badge_tier_info = BadgeTierSerializer(source='badge_tier', read_only=True)
    is_achieved = serializers.SerializerMethodField()

    class Meta:
        model = UserBadge
        fields = [
            'id',
            'user',
            'badge',
            'badge_info',
            'badge_tier',
            'badge_tier_info',
            'earned_at',
            'is_achieved',
        ]

    def get_is_achieved(self, obj):
        # Retrieve the first tier of the badge
        first_tier = obj.badge.tiers.order_by('reputation_threshold').first()

        if not first_tier:
            return False  # If no tiers exist, the badge can't be achieved

        # Retrieve the progress data for the badge
        try:
            progress = UserBadgeProgress.objects.get(user=obj.user, badge=obj.badge)
            return progress.progress_value >= first_tier.reputation_threshold
        except UserBadgeProgress.DoesNotExist:
            return False  # If no progress record exists, badge is not achieved


class UserBadgeProgressSerializer(serializers.ModelSerializer):
    badge_info = BadgeSerializer(source='badge', read_only=True)
    badge_tier_info = BadgeTierSerializer(source='badge_tier', read_only=True)
    class Meta:
        model = UserBadgeProgress
        fields = '__all__'


class AnswerSerializer(serializers.ModelSerializer):
    # Include expert info
    expert_info = UserSerializer(source='expert', read_only=True)
    # Add expert_badges field
    expert_badges = serializers.SerializerMethodField()
    
    class Meta:
        model = Answers
        fields = '__all__'

    def get_expert_badges(self, obj):
        user = obj.expert
        if user:
            # Fetch global badges
            global_badges = user.userbadge_set.filter(
                badge__is_global=True
            ).select_related('badge', 'badge_tier')

            # Fetch tag-specific badges based on the answer's tags
            answer_tags = obj.question.tags.all()
            tag_specific_badges = user.userbadge_set.filter(
                badge__associated_tag__in=answer_tags,
                badge__is_global=False
            ).select_related('badge', 'badge_tier')

            # Combine both querysets
            all_badges = global_badges.union(tag_specific_badges)

            serializer = UserBadgeSerializer(all_badges, many=True)
            return serializer.data
        return []

        
class CommentSerializer(serializers.ModelSerializer):
    # This allows us to get the user info of the commenter as a dictionary, based on the expert_id (for GET requests)
    expert_info = UserSerializer(source='expert', read_only=True)
    expert_badges = UserBadgeSerializer(source='expert.user_badges.all', many=True, read_only=True)

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