import pdfplumber
import re

try:
    import spacy
    nlp = spacy.load('en_core_web_sm')
    SPACY_AVAILABLE = True
except (OSError, ImportError):
    nlp = None
    SPACY_AVAILABLE = False


def extract_text_from_pdf(pdf_file) -> str:
    """Extract all text from a PDF file using pdfplumber."""
    text = ""
    try:
        with pdfplumber.open(pdf_file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        print(f"PDF extraction error: {e}")
    return text.strip()


def extract_topics(text: str) -> list[str]:
    """
    Extract key topics from syllabus text using Gemini API.
    """
    if not text:
        return []

    from ai_tutor.gemini import generate_json
    
    prompt = f"""
    You are an educational AI. Extract the core concepts and topics from the following syllabus text.
    Ignore structural metadata, generic headings, or unit numbers (e.g., "Unit I", "Chapter 2", "Table of strings", "Introduction").
    Provide a JSON array of strings containing up to 20 specific, atomic, and clear educational topics 
    (e.g., ["Variables and Data Types", "Switch Statement", "Recursion", "Pointer Expressions"]).
    
    Syllabus Text:
    {text[:5000]}
    """
    
    try:
        topics = generate_json(prompt)
        if isinstance(topics, list):
            # Clean up and deduplicate while preserving order if possible
            cleaned = []
            for t in topics:
                t_clean = t.strip()
                if t_clean and len(t_clean) <= 60 and t_clean not in cleaned:
                    cleaned.append(t_clean)
            return cleaned[:20]
    except Exception as e:
        print(f"Topic extraction error via Gemini: {e}")
        
    return []
