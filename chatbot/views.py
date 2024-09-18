# chatbot/views.py
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

@csrf_exempt
def chatbot_response(request):
    if request.method == "POST":
        user_message = request.POST.get('message')

        # Basic chatbot logic
        if "service" in user_message.lower():
            bot_response = "We offer various home services including cleaning, plumbing, and electrical repairs."
        elif "price" in user_message.lower():
            bot_response = "Our service prices vary depending on the job. Please provide more details."
        else:
            bot_response = "I'm here to help with your home service needs. How can I assist you today?"

        return JsonResponse({"response": bot_response})
    return JsonResponse({"response": "Sorry, I can only respond to POST requests."})

def chatbot_page(request):
    return render(request, 'chatbot.html')
