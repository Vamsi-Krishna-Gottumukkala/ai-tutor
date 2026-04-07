import json
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from subjects.models import Subject
from .models import ChatSession, ChatMessage
from ai_tutor.gemini import generate_text

SYSTEM_PROMPT = """You are an expert and friendly AI tutor helping a student learn "{subject}".
Your job is to:
- Explain concepts clearly with examples
- Answer questions patiently and thoroughly
- Break down complex topics into simple parts
- Encourage the student when they struggle
- Stay focused on the subject topic

Subject context: {syllabus_snippet}

Always respond in a helpful, educational, and encouraging tone. Keep answers concise but complete.
"""


@login_required
def chat_page(request, subject_id=None):
    subjects = Subject.objects.filter(owner=request.user)
    current_subject = None

    if subject_id:
        current_subject = get_object_or_404(Subject, pk=subject_id, owner=request.user)

    # Get or create session
    session = None
    history = []
    if current_subject:
        session, _ = ChatSession.objects.get_or_create(
            user=request.user, subject=current_subject
        )
        history = session.messages.all()

    return render(request, 'chatbot/chatbot.html', {
        'subjects': subjects,
        'current_subject': current_subject,
        'session': session,
        'history': history,
    })


@login_required
@require_POST
def send_message(request):
    data = json.loads(request.body)
    user_message = data.get('message', '').strip()
    subject_id = data.get('subject_id')

    if not user_message:
        return JsonResponse({'error': 'Empty message'}, status=400)

    subject = None
    session = None
    if subject_id:
        try:
            subject = Subject.objects.get(pk=subject_id, owner=request.user)
            session, _ = ChatSession.objects.get_or_create(user=request.user, subject=subject)
        except Subject.DoesNotExist:
            pass

    if not session:
        session, _ = ChatSession.objects.get_or_create(
            user=request.user,
            subject=None,
        )

    # Save user message
    ChatMessage.objects.create(session=session, role='user', content=user_message)

    # Build context-aware prompt
    subject_name = subject.name if subject else 'General Topics'
    syllabus = (subject.syllabus_text[:300] if subject and subject.syllabus_text else '') or 'Not specified'

    # Include last 5 exchanges for context
    recent = list(session.messages.order_by('-timestamp')[:10])[::-1]
    history_text = '\n'.join([
        f"{'Student' if m.role == 'user' else 'Tutor'}: {m.content}"
        for m in recent[:-1]  # exclude the message we just added
    ])

    full_prompt = SYSTEM_PROMPT.format(
        subject=subject_name,
        syllabus_snippet=syllabus,
    )
    if history_text:
        full_prompt += f"\n\nConversation so far:\n{history_text}"
    full_prompt += f"\n\nStudent: {user_message}\nTutor:"

    try:
        ai_response = generate_text(full_prompt)
    except Exception as e:
        ai_response = "Sorry, I'm having trouble connecting to the AI service. Please check your API key."
        print(f"Chatbot error: {e}")

    # Save AI response
    ChatMessage.objects.create(session=session, role='assistant', content=ai_response)

    return JsonResponse({'response': ai_response})
