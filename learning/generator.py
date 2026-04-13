from ai_tutor.gemini import generate_json, generate_text

RECOMMENDATIONS_PROMPT = """
You are an expert academic tutor. A student just completed a quiz on "{subject_name}".

Student Performance:
- Score: {score}/{total} ({percentage}%)
- Skill Level: {skill_level}
- Weak Topics: {weak_topics}

Generate a personalized study plan in JSON format:
{{
  "recommendations": [
    "Specific actionable study tip 1",
    "Specific actionable study tip 2",
    "Specific actionable study tip 3",
    "Specific actionable study tip 4",
    "Specific actionable study tip 5"
  ],
  "important_questions": [
    "Important practice question 1?",
    "Important practice question 2?",
    "Important practice question 3?",
    "Important practice question 4?",
    "Important practice question 5?"
  ],
  "study_tips": [
    "General study tip 1",
    "General study tip 2",
    "General study tip 3"
  ]
}}

Focus the recommendations specifically on the weak topics. Return ONLY valid JSON.
"""

FLASHCARD_PROMPT = """
You are an educational content creator. Generate 8 flashcards for the subject "{subject_name}".

Topics to cover: {topics}

Return JSON in this exact format:
{{
  "flashcards": [
    {{
      "topic": "Topic name",
      "front": "Concept or question",
      "back": "Clear, concise explanation with an example if helpful"
    }}
  ]
}}

Make the flashcards educational, clear, and suitable for revision. Return ONLY valid JSON.
"""


def generate_learning_path(user, subject):
    """
    Generate personalized learning path after a quiz attempt.
    Called automatically after quiz submission.
    """
    from assessments.models import QuizAttempt, WeakTopic
    from .models import LearningPath, Flashcard

    # Get latest attempt for this subject
    latest = QuizAttempt.objects.filter(
        user=user, quiz__subject=subject
    ).order_by('-attempt_date').first()

    if not latest:
        return

    weak_topics = list(
        WeakTopic.objects.filter(user=user, subject=subject)
        .values_list('topic_name', flat=True)[:5]
    )

    # 1. Generate learning path / recommendations
    rec_prompt = RECOMMENDATIONS_PROMPT.format(
        subject_name=subject.name,
        score=latest.score,
        total=latest.total_questions,
        percentage=latest.percentage,
        skill_level=latest.skill_level,
        weak_topics=', '.join(weak_topics) if weak_topics else 'None identified',
    )

    try:
        rec_data = generate_json(rec_prompt)
        LearningPath.objects.update_or_create(
            user=user,
            subject=subject,
            defaults={
                'recommendations': rec_data.get('recommendations', []),
                'important_questions': rec_data.get('important_questions', []),
                'study_tips': rec_data.get('study_tips', []),
            }
        )
    except Exception as e:
        print(f"Learning path generation error: {e}")


def generate_flashcards(user, subject):
    """
    Generate dynamic flashcards based on the user's weak topics.
    Called Just-In-Time when the user visits the flashcards page.
    """
    from assessments.models import WeakTopic
    from .models import Flashcard

    weak_topics = list(
        WeakTopic.objects.filter(user=user, subject=subject)
        .values_list('topic_name', flat=True)[:5]
    )

    # Generate flashcards (Dynamic: update based on current weak topics)
    try:
        topics_to_flash = weak_topics if weak_topics else subject.topic_list
        flash_prompt = FLASHCARD_PROMPT.format(
            subject_name=subject.name,
            topics=', '.join(topics_to_flash[:10]) if topics_to_flash else subject.name,
        )
        flash_data = generate_json(flash_prompt)
        
        if flash_data and flash_data.get('flashcards'):
            # Clear old flashcards only if we successfully generated new ones
            Flashcard.objects.filter(user=user, subject=subject).delete()
            
            for card in flash_data.get('flashcards', []):
                Flashcard.objects.create(
                    user=user,
                    subject=subject,
                    topic=card.get('topic', ''),
                    front_text=card.get('front', ''),
                    back_text=card.get('back', ''),
                )
    except Exception as e:
        print(f"Flashcard generation error: {e}")
