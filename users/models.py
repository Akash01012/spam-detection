from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Count

class User(AbstractUser):
    phone_number = models.CharField(unique=True, max_length=15)
    email = models.EmailField(blank=True, null=True)

class GlobalContact(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15, unique=True)
    spam_likelihood = models.FloatField(default=0.0)  
    email = models.EmailField(blank=True, null=True)

    def update_spam_likelihood(self):
        spam_count = SpamMark.objects.filter(phone_number=self.phone_number).count()
        self.spam_likelihood = min(spam_count / 10, 1.0)
        self.save()

    def __str__(self):
        return f"{self.name} - {self.phone_number}"


class Contact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="contacts")
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(blank=True, null=True)

    @property
    def spam_likelihood(self):
        total_users = User.objects.count()
        spam_count = SpamMark.objects.filter(phone_number=self.phone_number).count()
        return spam_count / total_users if total_users > 0 else 0
    
    

class SpamMark(models.Model):
    phone_number = models.CharField(max_length=15)
    marked_by = models.ForeignKey(User, on_delete=models.CASCADE)
    marked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.phone_number} marked as spam by {self.marked_by.username} on {self.marked_at}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        try:
            contact = GlobalContact.objects.get(phone_number=self.phone_number)
            contact.update_spam_likelihood()
        except GlobalContact.DoesNotExist:
            pass
