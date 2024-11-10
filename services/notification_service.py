# services/notification_service.py
from typing import Optional, Dict, Any
from django.db import transaction
from pulse.models import Notifications, Questions, Answers, Comments


class NotificationService:
    """Service class to handle all notification-related operations."""
    
    NOTIFICATION_TYPES = {
        'question_answered': 'Your question received a new answer',
        'answer_commented': 'Your answer received a new comment',
        'question_upvoted': 'Your question was upvoted',
        'answer_accepted': 'Your answer was accepted',
        'mention': 'You were mentioned in a {content_type}',
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
            read=False
        )
        
        return notification

    @classmethod
    def handle_new_answer(cls, answer: 'Answers') -> None:
        """Handle notifications for a new answer."""
        question: Questions = answer.question

        # TODO: leaving the following line commented for now (to make it easier for testing notifications)
        # if question.asker != answer.expert:  # Don't notify if user answers their own question
        cls.create_notification(
            recipient_id=question.asker,
            notification_type='question_answered',
            question=question,
            answer=answer,
            actor_id=answer.expert
        )