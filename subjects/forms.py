from django import forms
from .models import Subject


class SubjectForm(forms.ModelForm):
    syllabus_input_type = forms.ChoiceField(
        choices=[('text', 'Paste Text'), ('pdf', 'Upload PDF')],
        widget=forms.RadioSelect(attrs={'class': 'radio-option'}),
        initial='text',
        required=False,
        label='Syllabus Input Method'
    )

    class Meta:
        model = Subject
        fields = ['name', 'description', 'syllabus_text', 'syllabus_pdf']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'e.g. Machine Learning, Data Structures...'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-input',
                'rows': 2,
                'placeholder': 'Brief description of this subject (optional)'
            }),
            'syllabus_text': forms.Textarea(attrs={
                'class': 'form-input',
                'rows': 8,
                'placeholder': 'Paste your syllabus here...\n\nUnit 1: Introduction\n- Topic 1\n- Topic 2\n\nUnit 2: ...'
            }),
            'syllabus_pdf': forms.FileInput(attrs={'class': 'file-input', 'accept': '.pdf'}),
        }
        labels = {
            'name': 'Subject Name',
            'description': 'Description',
            'syllabus_text': 'Syllabus Text',
            'syllabus_pdf': 'Upload PDF',
        }
