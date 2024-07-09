from django.shortcuts import render, get_object_or_404, redirect
from quiz.models import Question, Choice, UserTestResult, UserAnswer, Test
from django.contrib.auth.decorators import login_required

from django.views.decorators.csrf import csrf_exempt

import sweetify

# Create your views here.

def test_view(request):
    quiz = Question.objects.all()
    user_test_result = None
    all_questions_answered = False

    if request.user.is_authenticated:
        user_test_result = UserTestResult.objects.filter(user=request.user).order_by('-id').first()
        
        if user_test_result:
            answered_questions_count = UserAnswer.objects.filter(user_test_result=user_test_result).count()
            all_questions_answered = (answered_questions_count == quiz.count())

    context = {
        'quiz': quiz,
        'user_test_result': user_test_result,
        'all_questions_answered': all_questions_answered
    }
    return render(request, 'test.html', context)

@csrf_exempt
@login_required
def quiz_single(request, qid):
    quests = Question.objects.all()
    quiz = get_object_or_404(quests, pk=qid)
    next_quiz = quests.filter(id__gt=qid).first()
    prev_quiz = quests.filter(id__lt=qid).last()
    user = request.user

    test = quiz.test


    if qid == 1 and not request.session.get('test_started', False):
        UserTestResult.objects.filter(user=user, test=test).delete()
        user_test_result = UserTestResult.objects.create(user=user, test=test)
        request.session['test_started'] = True  # تست شروع شده
        sweetify.toast(request, type='success', title='راهنما', text='برای شنیدن فایل صوتی راهنمای سوالات، بر روی علامت پخش صدا در بالا سمت چپ تصویر کلیک کنید.', timer=4000)
    else:
        user_test_result, created = UserTestResult.objects.get_or_create(user=user, test=test)


    if request.method == 'POST':
        selected_choice_id = request.POST.get('choice')
        if selected_choice_id:
            selected_choice = get_object_or_404(Choice, id=selected_choice_id)
            user_answer, created = UserAnswer.objects.update_or_create(
                user_test_result=user_test_result,
                question=quiz,
                defaults={'choice': selected_choice}
            )
            if next_quiz:
                return redirect('quiz:single', qid=next_quiz.id)
            else:
                return redirect('quiz:result', result_id=user_test_result.id)

    # بازیابی انتخاب کاربر
    try:
        user_answer = UserAnswer.objects.get(user_test_result=user_test_result, question=quiz)
        selected_choice = user_answer.choice
    except UserAnswer.DoesNotExist:
        selected_choice = None



    category_colors = {
        '1': '#094ae3',
        '2': '#e30949',
        '3': '#09e357',
        '4': '#f39c12',
        '5': '#6f42c1',
        # دسته‌بندی‌ها و رنگ‌های دیگر را در اینجا اضافه کنید
    }
    quiz_category = str(quiz.category.id)

    # دریافت رنگ مرتبط با دسته‌بندی فعلی
    category_color = category_colors.get(quiz_category)  # رنگ پیش‌فرض سفید


    choices = quiz.choices.all()
    content = {
        'quiz': quiz,
        'next': next_quiz,
        'prev': prev_quiz,
        'all_quiz': quests.count(),
        'number': list(quests).index(quiz) + 1,
        'choices': choices,
        'selected_choice': selected_choice,  # افزودن انتخاب کاربر به تمپلیت
        'user_test_result': user_test_result,
        'category_color':category_color,
    }
    return render(request, 'quiz/quiz-single.html', content)

@csrf_exempt
@login_required
def quiz_result(request, result_id):
    user_test_result = get_object_or_404(UserTestResult, id=result_id, user=request.user)
    answers = user_test_result.answers.all()

    analysis = {}
    for answer in answers:
        question_category = answer.question.category
        category_name = question_category.name
        if category_name not in analysis:
            analysis[category_name] = {
                'weights': [],
                'category': question_category
            }
        analysis[category_name]['weights'].append(answer.choice.weight)

    category_averages = {category: sum(data['weights']) for category, data in analysis.items()}

    context = {
        'user_test_result': user_test_result,
        'category_averages': category_averages,
        'analysis': analysis,
    }

    return render(request, 'quiz/reports-details.html', context)

