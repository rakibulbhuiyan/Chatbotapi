import os
from django.shortcuts import render
import google.generativeai as genai
from grpc import Status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import ChatMessage,ChatSession
from django.conf import settings
import google.generativeai as genai

# Configure Gemini with the key from settings
genai.configure(api_key=settings.GEMINI_API_KEY)

# Load the Gemini Pro model
model = genai.GenerativeModel("gemini-2.5-flash")
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

@api_view(["POST"])
def chatbot(request):
    message = request.data.get("message")
    if not message:
        return Response({"error": "No message provided."}, status=400)

    # Check if user is authenticated
    user = request.user if request.user.is_authenticated else None

    # Create or get ongoing session for this user (or anonymous)
    session, created = ChatSession.objects.get_or_create(
        user=user,
        end_time__isnull=True,
        defaults={"user": user}
    )

    # Save user message
    ChatMessage.objects.create(
        session=session,
        sender='user',
        content=message
    )

    try:
        # Call Gemini API
        response = model.generate_content(message)
        bot_reply = response.text

        # Save bot reply
        ChatMessage.objects.create(
            session=session,  
            sender='bot',
            content=bot_reply
        )

        return Response({"response": bot_reply})
    except Exception as e:
        return Response({
            "error": "Gemini API error",
            "details": str(e)
        }, status=500)




def chat_history_view(request):
    if request.user.is_authenticated:
        
        session = ChatSession.objects.filter(user=request.user).order_by('-start_time').first()
    else:
       
        session = ChatSession.objects.filter(user__isnull=True).order_by('-start_time').first()

    chats = session.messages.all() if session else []

    return render(request, 'chat_history.html', {'chats': chats})



from .serializers import ChatMessageSerializer
from rest_framework import status


@api_view(["GET"])
def chat_history_api(request):
    if request.user.is_authenticated:
        session = ChatSession.objects.filter(user=request.user).order_by('-start_time').first()
    else:
        session = ChatSession.objects.filter(user__isnull=True).order_by('-start_time').first()

    chats = session.messages.all() if session else []

    serializer = ChatMessageSerializer(chats, many=True)

    response_data = {
        "success": True,
        "status": status.HTTP_200_OK,
        "message": "Successfully retrieved chat messages",
        "data": serializer.data
    }

    return Response(response_data, status=status.HTTP_200_OK)
    