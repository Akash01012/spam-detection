

import random
from django.core.management.base import BaseCommand
from users.models import User, Contact, SpamMark, GlobalContact
from django.utils import timezone


class Command(BaseCommand):
    help = 'Populates database with sample data'

    def handle(self, *args, **kwargs):
        User.objects.all().delete()
        Contact.objects.all().delete()
        SpamMark.objects.all().delete()
        GlobalContact.objects.all().delete()

        
        for i in range(10):
            user = User.objects.create_user(
                username=f'user{i}', password='password', 
                phone_number=f'123456789{i}', 
                email=f'user{i}@example.com' 
            )

            
            global_contact, created = GlobalContact.objects.update_or_create(
                phone_number=user.phone_number,
                defaults={
                    'name': user.username,
                    'spam_likelihood': 0.0,
                    'email': user.email if user.email else None  
                }
            )

            if random.choice([True, False]):
                SpamMark.objects.create(
                    phone_number=user.phone_number,
                    marked_by=user,
                    marked_at=timezone.now()
                )

                global_contact.update_spam_likelihood()

            for j in range(5):
                contact = Contact.objects.create(
                    user=user,
                    name=f'user{i}_contact{j}',
                    phone_number=f'639674321{j}',
                    email=f'contact{j}@example.com'
                )

                global_contact, created = GlobalContact.objects.update_or_create(
                    phone_number=contact.phone_number,
                    defaults={
                        'name': contact.name,
                        'spam_likelihood': 0.0,
                        'email': contact.email if contact.email else None
                    }
                )

                if random.choice([True, False]):
                    SpamMark.objects.create(
                        phone_number=contact.phone_number,
                        marked_by=user,
                        marked_at=timezone.now()
                    )
                    
                    global_contact.update_spam_likelihood()

        self.stdout.write(self.style.SUCCESS('Successfully populated database with sample data'))