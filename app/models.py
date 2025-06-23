from django.db import models
from django.utils import timezone






from django.contrib.auth.models import User # Or a custom User model

class ChatSession(models.Model):
    """
    Represents a single conversation session with a user.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        user_display = self.user.username if self.user else "Anonymous"
        return f"Chat Session for {user_display} - {self.start_time.strftime('%Y-%m-%d %H:%M')}"

class ChatMessage(models.Model):
    """
    Represents a single message within a chat session.
    """
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, null=True,related_name='messages')
    sender = models.CharField(max_length=50, choices=[('user', 'User'), ('bot', 'Bot')],default='user')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"{self.sender}: {self.content[:50]}..."