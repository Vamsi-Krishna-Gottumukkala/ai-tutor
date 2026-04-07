from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Subject, SyllabusTopic
from .forms import SubjectForm
from .utils import extract_text_from_pdf, extract_topics


@login_required
def subject_list(request):
    subjects = Subject.objects.filter(owner=request.user)
    return render(request, 'subjects/subject_list.html', {'subjects': subjects})


@login_required
def create_subject(request):
    if request.method == 'POST':
        form = SubjectForm(request.POST, request.FILES)
        if form.is_valid():
            subject = form.save(commit=False)
            subject.owner = request.user

            # Handle PDF upload: extract text if PDF provided
            pdf_file = request.FILES.get('syllabus_pdf')
            if pdf_file:
                extracted = extract_text_from_pdf(pdf_file)
                if extracted:
                    subject.syllabus_text = extracted

            subject.save()

            # Extract and save topics using NLP
            syllabus_content = subject.syllabus_text
            if syllabus_content:
                topics = extract_topics(syllabus_content)
                for i, topic in enumerate(topics):
                    SyllabusTopic.objects.create(
                        subject=subject,
                        topic_name=topic,
                        order=i
                    )

            messages.success(request, f'Subject "{subject.name}" created successfully!')
            return redirect('subjects:detail', pk=subject.pk)
    else:
        form = SubjectForm()
    return render(request, 'subjects/subject_form.html', {'form': form})


@login_required
def subject_detail(request, pk):
    subject = get_object_or_404(Subject, pk=pk, owner=request.user)
    topics = subject.topics.all()
    latest_attempt = subject.latest_attempt
    has_basic_test = subject.has_basic_test_completed
    return render(request, 'subjects/subject_detail.html', {
        'subject': subject,
        'topics': topics,
        'latest_attempt': latest_attempt,
        'has_basic_test': has_basic_test,
    })


@login_required
def delete_subject(request, pk):
    subject = get_object_or_404(Subject, pk=pk, owner=request.user)
    if request.method == 'POST':
        name = subject.name
        subject.delete()
        messages.success(request, f'Subject "{name}" deleted.')
        return redirect('subjects:list')
    return render(request, 'subjects/subject_confirm_delete.html', {'subject': subject})
