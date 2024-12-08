# services/notification_service.py
from typing import Optional
from django.db import transaction
from pulse.models import Notifications, Questions, Answers, Comments, Hives
from uuid import UUID


class NotificationService:
    """Service class to handle all notification-related operations."""
    
    NOTIFICATION_TYPES = {
        'question_answered': 'Your question received a new answer',
        'answer_commented': 'Your answer received a new comment',
        'question_upvoted': 'Your question was upvoted',
        'answer_accepted': 'Your answer was accepted',
        'mention': 'You were mentioned in a {content_type}',
        'hive_accepted': 'Your hive application was accepted',
        'hive_rejected': 'Your hive application was rejected',
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
        hive: Optional['Hives'] = None,
        hive_title: Optional[str] = None,
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
            hive: Related hive (optional)
            hive_title: Title of the hive (optional)
            actor_id: ID of the user who triggered the notification (optional)
            message: Custom message (optional, will use default if not provided)
        """
        if not recipient_id:
            # gracefully return if no recipient
            return
        
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
            hive=hive,
            hive_title=hive_title,
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
    def handle_hive_accepted(cls, hive: 'Hives') -> None:
        """Handle notifications for a hive application being accepted."""
        cls.create_notification(
            recipient_id=hive.owner,
            notification_type='hive_accepted',
            hive=hive
        )
        
    @classmethod
    def handle_hive_rejected(cls, user_id: str, hive_title: str) -> None:
        """Handle notifications for a hive application being rejected.
        Cannot include the hive object since it was deleted."""
        cls.create_notification(
            recipient_id=user_id,
            notification_type='hive_rejected',
            hive_title=hive_title
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