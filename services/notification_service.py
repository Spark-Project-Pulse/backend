# services/notification_service.py
from typing import Optional
from django.db import transaction
from pulse.models import Notifications, Questions, Answers, Comments, Communities
from uuid import UUID


class NotificationService:
    """Service class to handle all notification-related operations."""
    
    NOTIFICATION_TYPES = {
        'question_answered': 'Your question received a new answer',
        'answer_commented': 'Your answer received a new comment',
        'question_upvoted': 'Your question was upvoted',
        'answer_accepted': 'Your answer was accepted',
        'mention': 'You were mentioned in a {content_type}',
        'community_accepted': 'Your community application was accepted',
        'community_rejected': 'Your community application was rejected',
    }

    @classmethod
    @transaction.atomic
    def create_notification(
        cls,
        recipient_id: str,
        notification_type: str,
        question: Optional['Questions'] = None,
        answer: Optional['Answers'] = None,
        comment: Optional['Comments'] = None,
        community: Optional['Communities'] = None,
        community_title: Optional[str] = None,
        actor_id: Optional[str] = None,
        message: Optional[str] = None,
    ) -> Notifications:
        """
        Create a new notification.
        
        Args:
            recipient_id: ID of the user receiving the notification
            notification_type: Type of notification (from model's NOTIFICATION_TYPES)
            question: Related question (optional)
            answer: Related answer (optional)
            comment: Related comment (optional)
            community: Related community (optional)
            community_title: Title of the community (optional)
            actor_id: ID of the user who triggered the notification (optional)
            message: Custom message (optional, will use default if not provided)
        """
        if notification_type not in dict(Notifications.NOTIFICATION_TYPES):
            raise ValueError(f"Invalid notification type: {notification_type}")

        if message is None:
            message = cls.NOTIFICATION_TYPES[notification_type]
            if '{content_type}' in message:
                content_type = 'question' if question else 'answer' if answer else 'comment'
                message = message.format(content_type=content_type)

        notification = Notifications.objects.create(
            recipient=recipient_id,
            actor=actor_id,
            notification_type=notification_type,
            message=message,
            question=question,
            answer=answer,
            comment=comment,
            community=community,
            community_title=community_title,
            read=False
        )
        
        return notification

    @classmethod
    def handle_new_answer(cls, answer: 'Answers') -> None:
        """Handle notifications for a new answer."""
        question: Questions = answer.question

        if question.asker != answer.expert:  # Don't notify if user answers their own question
            cls.create_notification(
                recipient_id=question.asker,
                notification_type='question_answered',
                question=question,
                answer=answer,
                actor_id=answer.expert
            )
        
    @classmethod
    def handle_community_accepted(cls, community: 'Communities') -> None:
        """Handle notifications for a community application being accepted."""
        cls.create_notification(
            recipient_id=community.owner,
            notification_type='community_accepted',
            community=community
        )
        
    @classmethod
    def handle_community_rejected(cls, user_id: str, community_title: str) -> None:
        """Handle notifications for a community application being rejected.
        Cannot include the community object since it was deleted."""
        cls.create_notification(
            recipient_id=user_id,
            notification_type='community_rejected',
            community_title=community_title
        )
        

    @classmethod
    def mark_as_read(cls, user_id: UUID, notification_id: UUID) -> bool:
        """Handles marking a notification as read for a given user.

        Args:
            user_id (UUID): id of recipient of notification
            notification_id (UUID): id of notification being altered

        Returns:
            bool: True if operation successful, False otherwise
        """
        try:
            # Get the notification and verify the recipient matches the user
            notification = Notifications.objects.get(
                notification_id=notification_id,
                recipient_id=user_id
            )
            
            # Mark as read and save
            notification.read = True
            notification.save()
            
            return True
            
        except Notifications.DoesNotExist:
            # Either notification doesn't exist or user isn't authorized
            return False


    @classmethod
    def mark_as_unread(cls, user_id: UUID, notification_id: UUID) -> bool:
        """Handles marking a notification as unread for a given user.

        Args:
            user_id (UUID): id of recipient of notification
            notification_id (UUID): id of notification being altered

        Returns:
            bool: True if operation successful, False otherwise
        """
        try:
            # Get the notification and verify the recipient matches the user
            notification = Notifications.objects.get(
                notification_id=notification_id,
                recipient_id=user_id
            )
            
            # Mark as read and save
            notification.read = False
            notification.save()
            
            return True
            
        except Notifications.DoesNotExist:
            # Either notification doesn't exist or user isn't authorized
            return False


    @classmethod
    def delete(cls, user_id: UUID, notification_id: UUID) -> bool:
        """Handles deleting a notification for a given user.

        Args:
            user_id (UUID): id of recipient of notification
            notification_id (UUID): id of notification being deleted

        Returns:
            bool: True if operation successful, False otherwise
        """
        try:
            # Get the notification and verify the recipient matches the user
            notification = Notifications.objects.get(
                notification_id=notification_id,
                recipient_id=user_id
            )
            
            # Delete notification
            notification.delete()
            
            return True
            
        except Notifications.DoesNotExist:
            # Either notification doesn't exist or user isn't authorized
            return False