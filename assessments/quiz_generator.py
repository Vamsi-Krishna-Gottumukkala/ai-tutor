import json
from ai_tutor.gemini import generate_json
from .models import Quiz, Question


QUIZ_PROMPT = """You are an expert educational quiz designer.

Subject: {subject_name}
Syllabus Topics: {topics}
Difficulty: {difficulty}
Number of Questions: {num_questions}

Generate exactly {num_questions} multiple-choice questions that test understanding of the subject above.

Return a JSON object in this exact format (no extra text, no markdown):
{{
  "questions": [
    {{
      "question": "Clear question text here?",
      "option_a": "First option",
      "option_b": "Second option",
      "option_c": "Third option",
      "option_d": "Fourth option",
      "correct_answer": "a",
      "topic": "Topic name this question covers"
    }}
  ]
}}

Rules:
- correct_answer must be ONE of: "a", "b", "c", "d"
- All 4 options must be plausible, only one is correct
- Questions must cover different topics from the syllabus
- Return ONLY valid JSON
"""


def generate_quiz(subject, user, quiz_type='basic', num_questions=10, difficulty='mixed'):
    """
    Generate quiz questions using Gemini AI and save to database.
    Returns the created Quiz object, or None on failure.
    """
    topics = subject.topic_list
    topics_str = ', '.join(topics) if topics else subject.syllabus_text[:500]

    prompt = QUIZ_PROMPT.format(
        subject_name=subject.name,
        topics=topics_str,
        difficulty=difficulty,
        num_questions=num_questions,
    )

    try:
        data = generate_json(prompt)
        questions_data = data.get('questions', [])

        if not questions_data:
            return None

        # Create Quiz record
        quiz = Quiz.objects.create(
            subject=subject,
            user=user,
            quiz_type=quiz_type,
        )

        # Save Questions
        for i, q in enumerate(questions_data):
            Question.objects.create(
                quiz=quiz,
                question_text=q.get('question', ''),
                option_a=q.get('option_a', ''),
                option_b=q.get('option_b', ''),
                option_c=q.get('option_c', ''),
                option_d=q.get('option_d', ''),
                correct_answer=q.get('correct_answer', 'a').lower(),
                topic_tag=q.get('topic', ''),
                order=i,
            )

        return quiz

    except Exception as e:
        print(f"Quiz generation error: {e}")
        return None
