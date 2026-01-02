from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import User, Contact, SpamMark, GlobalContact
from rest_framework.exceptions import ValidationError
from .serializers import UserSerializer, ContactSerializer, SpamMarkSerializer
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from django.shortcuts import render


class APIVisit(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        # If the client accepts HTML, render template
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'api_home.html')

        # Otherwise return JSON
        return Response({
            "message": "You are on the base URL of the Spam Detection REST API.",
            "info": "This is an API-only backend. Please use Postman or any HTTP client to test the endpoints.",
            "endpoints": [
                "POST /register/",
                "POST /login/",
                "GET /contacts/",
                "POST /mark-spam/",
                "GET /search-by-name/?name=<name>",
                "GET /search-by-phone/?phone_number=<number>"
            ],
            "documentation": "For detailed usage instructions, visit the README:",
            "readme_url": "https://github.com/Akash01012/spam-detection"
        })
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        user = serializer.save()

        global_contact, created = GlobalContact.objects.update_or_create(
            phone_number=user.phone_number,
            defaults={
                'name': user.username,  
                'spam_likelihood': 0.0, 
                'email': user.email if user.email else None 
            }
        )

        global_contact.save()


class ContactListView(generics.ListAPIView):
    serializer_class = ContactSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Contact.objects.filter(user=self.request.user)


class SpamMarkView(generics.CreateAPIView):
    serializer_class = SpamMarkSerializer

    def perform_create(self, serializer):
        phone_number = serializer.validated_data['phone_number']
        user = self.request.user

        if SpamMark.objects.filter(marked_by=user, phone_number=phone_number).exists():
            raise ValidationError({"detail": "You have already marked this number as spam."})

        serializer.save(marked_by=user)

        existing_contact = GlobalContact.objects.filter(phone_number=phone_number).first()

        name = existing_contact.name if existing_contact else "Anonymous"
        email = existing_contact.email if existing_contact else None

        global_contact, created = GlobalContact.objects.update_or_create(
            phone_number=phone_number,
            defaults={
                'name': name,
                'email':email  
            }
        )

        if not created:
            global_contact.spam_likelihood += 0.1 
        else:
            global_contact.spam_likelihood = 0.1 

        global_contact.save()


class SearchByNameView(generics.ListAPIView):
    serializer_class = ContactSerializer

    def get_queryset(self):
        search_query = self.request.query_params.get("name", "").strip()
        if search_query:
            results_start = GlobalContact.objects.filter(name__istartswith=search_query)
            results_contain = GlobalContact.objects.filter(
                Q(name__icontains=search_query) & ~Q(name__istartswith=search_query)
            )

            return results_start | results_contain
        return GlobalContact.objects.none()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        result_data = []
        current_user = request.user

        for contact in queryset:
            contact_info = {
                "name": contact.name,
                "phone_number": contact.phone_number,
                "spam_likelihood": contact.spam_likelihood,
                "email": contact.email
            }
            
            if Contact.objects.filter(user=current_user, phone_number=contact.phone_number).exists():
                contact_info["email"] = contact.email

            result_data.append(contact_info)

        if not result_data:
            return Response({"error": "No search results found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(result_data)


class SearchByPhoneView(generics.ListAPIView):
    serializer_class = ContactSerializer

    def get_queryset(self):
        phone_number = self.request.query_params.get('phone_number', '').strip()
        if phone_number:
            return GlobalContact.objects.filter(phone_number=phone_number)
        return GlobalContact.objects.none()

    def list(self, request, *args, **kwargs):
        phone_number = self.request.query_params.get('phone_number', '').strip()
        if not phone_number:
            return Response({"error": "Phone number is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response({"error": "No search results found"}, status=status.HTTP_404_NOT_FOUND)

        result_data = []
        current_user = request.user

        for contact in queryset:
            contact_info = {
                "name": contact.name,
                "phone_number": contact.phone_number,
                "spam_likelihood": contact.spam_likelihood,
                "email": contact.email
            }

            
            if Contact.objects.filter(user=current_user, phone_number=contact.phone_number).exists():
                contact_info["email"] = contact.email

            result_data.append(contact_info)

        return Response(result_data)
