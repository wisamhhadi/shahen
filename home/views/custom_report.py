from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.utils.decorators import method_decorator

from mandob.models import CustomReport, Question, QuestionChoice, Answer, CustomAnswer
from ..filters import custom_report_filter
from ..forms import CustomReportForm
import json

from ..generics import filter_view_generic


@login_required
def create_custom_report(request):
    """Create new custom report"""

    if request.method == 'POST':
        form = CustomReportForm(request.POST)

        if form.is_valid():
            try:
                with transaction.atomic():
                    # Save the custom report
                    custom_report = form.save()

                    # Process questions
                    questions_data = get_questions_from_request(request)

                    if not questions_data:
                        messages.error(request, 'يجب إضافة سؤال واحد على الأقل')
                        custom_report.delete()
                        return render(request, 'create_custom_report.html', {
                            'form': form
                        })

                    # Create questions and choices
                    for question_data in questions_data:
                        if not question_data['title'].strip():
                            continue

                        # Create question with default type "custom"
                        question = Question.objects.create(
                            custom_report=custom_report,
                            title=question_data['title'],
                            answer_type=question_data['answer_type'],
                            type='custom',  # Default to custom as requested
                        )

                        # Create choices for multiple choice questions
                        if question_data['answer_type'] == 'choice' and question_data['choices']:
                            for order, choice_text in enumerate(question_data['choices']):
                                if choice_text.strip():
                                    QuestionChoice.objects.create(
                                        question=question,
                                        choice_text=choice_text.strip(),
                                        order=order,
                                    )

                    messages.success(request, f'تم إنشاء التقرير "{custom_report.title}" بنجاح')
                    return redirect('list_custom_reports')

            except Exception as e:
                messages.error(request, f'حدث خطأ أثناء إنشاء التقرير: {str(e)}')

        else:
            messages.error(request, 'يرجى تصحيح الأخطاء في النموذج')

    else:
        form = CustomReportForm()

    return render(request, 'create_custom_report.html', {
        'form': form
    })


@login_required
def update_custom_report(request, pk):
    """Update existing custom report"""

    custom_report = get_object_or_404(CustomReport, pk=pk)
    answers = CustomAnswer.objects.all().filter(custom_report=custom_report)

    if request.method == 'POST':
        form = CustomReportForm(request.POST, instance=custom_report)

        if form.is_valid():
            try:
                with transaction.atomic():
                    report_pk = form.instance.pk
                    custom_report = form.save()

                    # Delete existing questions and choices
                    Question.objects.all().filter(custom_report_id=report_pk).delete()

                    # Process new questions
                    questions_data = get_questions_from_request(request)

                    if not questions_data:
                        messages.error(request, 'يجب إضافة سؤال واحد على الأقل')
                        return render(request, 'update_custom_report.html', {
                            'form': form,
                            'custom_report': custom_report
                        })

                    # Create new questions and choices
                    for question_data in questions_data:
                        if not question_data['title'].strip():
                            continue

                        # Create question with default type "custom"
                        question = Question.objects.create(
                            custom_report=custom_report,
                            title=question_data['title'],
                            answer_type=question_data['answer_type'],
                            type='custom',
                        )

                        # Create choices for multiple choice questions
                        if question_data['answer_type'] == 'choice' and question_data['choices']:
                            for order, choice_text in enumerate(question_data['choices']):
                                if choice_text.strip():
                                    QuestionChoice.objects.create(
                                        question=question,
                                        choice_text=choice_text.strip(),
                                        order=order,
                                    )

                    messages.success(request, f'تم تحديث التقرير "{custom_report.title}" بنجاح')
                    return redirect('list_custom_reports')

            except Exception as e:
                messages.error(request, f'حدث خطأ أثناء تحديث التقرير: {str(e)}')

        else:
            messages.error(request, 'يرجى تصحيح الأخطاء في النموذج')

    else:
        form = CustomReportForm(instance=custom_report)

    # Get existing questions for pre-population
    existing_questions = []
    for question in Question.objects.all().filter(custom_report_id=pk).order_by('created'):
        question_data = {
            'title': question.title,
            'answer_type': question.answer_type,
            'choices': [choice.choice_text for choice in question.choices.order_by('order')]
        }
        existing_questions.append(question_data)

    return render(request, 'update_custom_report.html', {
        'form': form,
        'custom_report': custom_report,
        'existing_questions': json.dumps(existing_questions),
        'answers':answers
    })


@login_required
def delete_custom_report(request, pk):
    """Delete custom report"""

    custom_report = get_object_or_404(CustomReport, pk=pk)

    if request.method == 'POST':
        title = custom_report.title
        custom_report.delete()
        messages.success(request, f'تم حذف التقرير "{title}" بنجاح')
        return redirect('list_custom_reports')

    return render(request, 'delete_custom_report.html', {
        'custom_report': custom_report
    })


@method_decorator(login_required(), name="dispatch")
class list_custom_reports(filter_view_generic):
    queryset = CustomReport.objects.all().order_by('-id')
    model = CustomReport
    template_name = "list_custom_report.html"
    paginate_by = 25
    filterset_class = custom_report_filter
    context_object_name = "reports"

def get_questions_from_request(request):
    """Extract questions data from POST request"""
    questions_data = []
    question_index = 1

    while True:
        title_key = f'questions[{question_index}][title]'
        answer_type_key = f'questions[{question_index}][answer_type]'

        if title_key not in request.POST:
            break

        title = request.POST.get(title_key, '').strip()
        answer_type = request.POST.get(answer_type_key, 'text')

        if title:  # Only process non-empty questions
            choices = []

            # Get choices for multiple choice questions
            if answer_type == 'choice':
                # Look for choices in the format: choice_1_0, choice_1_1, etc.
                choice_dict = {}
                for key, value in request.POST.items():
                    if key.startswith(f'choice_{question_index}_') and value.strip():
                        try:
                            choice_index = int(key.split('_')[-1])
                            choice_dict[choice_index] = value.strip()
                        except (ValueError, IndexError):
                            continue

                # Convert to ordered list
                choices = [choice_dict[i] for i in sorted(choice_dict.keys())]

            questions_data.append({
                'title': title,
                'answer_type': answer_type,
                'choices': choices
            })

        question_index += 1

    return questions_data