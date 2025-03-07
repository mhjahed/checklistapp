from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone 


class Task(models.Model):
    NOTIFICATION_CHOICES = [
        (0, 'At time of task'),
        (5, '5 minutes before'),
        (15, '15 minutes before'),
        (30, '30 minutes before'),
        (60, '1 hour before'),
        (1440, '1 day before'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    due_date = models.DateTimeField()
    notify_before = models.IntegerField(choices=NOTIFICATION_CHOICES, default=0)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    
    
    class Meta:
        ordering = ['due_date']
    
    def _str_(self):
        return self.title

    @property
    def is_past_due(self):
     return self.due_date < timezone.now() and not self.completed
 
    @property
    def notification_time(self):
       if self.notify_before == 0:
           return self.due_date
       return self.due_date - timezone.timedelta(minutes=self.notify_before)