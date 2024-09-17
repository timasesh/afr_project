# courses/views.py
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import StudentRegistrationForm, LessonCreationForm, ModuleCreationForm, CourseCreationForm
from .models import User, Lesson, Module, Course, StudentProgress

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_admin:
                return redirect('admin_page')
            elif user.is_student:
                return redirect('student_page')
        else:
            return render(request, 'courses/login.html', {'error': 'Invalid credentials'})
    return render(request, 'courses/login.html')

@login_required
def admin_page(request):
    student_form = StudentRegistrationForm()
    lesson_form = LessonCreationForm()
    module_form = ModuleCreationForm()
    course_form = CourseCreationForm()

    if request.method == 'POST':
        if 'add_student' in request.POST:
            student_form = StudentRegistrationForm(request.POST)
            if student_form.is_valid():
                student_form.save()
                return redirect('admin_page')
        elif 'add_lesson' in request.POST:
            lesson_form = LessonCreationForm(request.POST, request.FILES)
            if lesson_form.is_valid():
                lesson_form.save()
                return redirect('admin_page')
        elif 'add_module' in request.POST:
            module_form = ModuleCreationForm(request.POST)
            if module_form.is_valid():
                module_form.save()
                return redirect('admin_page')
        elif 'add_course' in request.POST:
            course_form = CourseCreationForm(request.POST)
            if course_form.is_valid():
                course_form.save()
                return redirect('admin_page')
        elif 'delete_course' in request.POST:
            course_id = request.POST['course_id']
            Course.objects.filter(id=course_id).delete()
            return redirect('admin_page')

    students = User.objects.filter(is_student=True)
    lessons = Lesson.objects.all()
    modules = Module.objects.all()
    courses = Course.objects.all()

    context = {
        'student_form': student_form,
        'lesson_form': lesson_form,
        'module_form': module_form,
        'course_form': course_form,
        'students': students,
        'lessons': lessons,
        'modules': modules,
        'courses': courses,
    }
    return render(request, 'courses/admin_page.html', context)

@login_required
def student_page(request):
    if not request.user.is_student:
        return redirect('login')
    courses = Course.objects.all()
    return render(request, 'courses/student_page.html', {'courses': courses})

@login_required
def profile_page(request):
    progress = StudentProgress.objects.filter(student=request.user)
    return render(request, 'courses/profile.html', {'progress': progress})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    return render(request, 'courses/course_detail.html', {'course': course})

def delete_student(request, student_id):
    student = get_object_or_404(User, id=student_id, is_student=True)
    if request.method == 'POST':
        student.delete()
        return redirect('admin_page')  # Предполагается, что у вас есть URL 'admin_page'
    return render(request, 'courses/delete_student.html', {'student': student})

@login_required
def delete_lesson(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    if request.method == 'POST':
        lesson.delete()
        return redirect('admin_page')  # Предполагается, что у вас есть URL 'admin_page'
    return render(request, 'courses/delete_lesson.html', {'lesson': lesson})

@login_required
def delete_module(request, module_id):
    module = get_object_or_404(Module, id=module_id)
    if request.method == 'POST':
        module.delete()
        return redirect('admin_page')  # Предполагается, что у вас есть URL 'admin_page'
    return render(request, 'courses/delete_module.html', {'module': module})


from django.shortcuts import render, redirect, get_object_or_404
from .models import Question, Answer
from .forms import QuestionForm, AnswerForm
from django.forms import modelformset_factory

@login_required

def create_quiz(request):
    AnswerFormSet = modelformset_factory(Answer, form=AnswerForm, extra=4)

    if request.method == 'POST':
        question_form = QuestionForm(request.POST)
        formset = AnswerFormSet(request.POST)

        if question_form.is_valid() and formset.is_valid():
            question = question_form.save()
            answers = formset.save(commit=False)
            for answer in answers:
                answer.question = question
                answer.save()
            return redirect('quiz_list')

    else:
        question_form = QuestionForm()
        formset = AnswerFormSet(queryset=Answer.objects.none())

    return render(request, 'courses/create_quiz.html', {
        'question_form': question_form,
        'formset': formset
    })

@login_required
def quiz_list(request):
    quizzes = Question.objects.all()
    return render(request, 'courses/quiz_list.html', {'quizzes': quizzes})

@login_required
def edit_quiz(request, pk):
    question = get_object_or_404(Question, pk=pk)
    AnswerFormSet = modelformset_factory(Answer, form=AnswerForm, extra=0)

    if request.method == 'POST':
        question_form = QuestionForm(request.POST, instance=question)
        formset = AnswerFormSet(request.POST, queryset=question.answers.all())

        if question_form.is_valid() and formset.is_valid():
            question_form.save()
            formset.save()
            return redirect('quiz_list')

    else:
        question_form = QuestionForm(instance=question)
        formset = AnswerFormSet(queryset=question.answers.all())

    return render(request, 'courses/edit_quiz.html', {
        'question_form': question_form,
        'formset': formset
    })


from django.shortcuts import render, redirect
from .forms import QuizForm, QuestionForm, AnswerFormSet
from .models import Quiz


@login_required
def create_quiz(request):
    if request.method == 'POST':
        quiz_form = QuizForm(request.POST)

        if quiz_form.is_valid():
            quiz = quiz_form.save()
            return redirect('add_question', quiz_id=quiz.id)
    else:
        quiz_form = QuizForm()

    return render(request, 'courses/create_quiz.html', {
        'quiz_form': quiz_form,
    })


@login_required
def add_question(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)

    if request.method == 'POST':
        question_form = QuestionForm(request.POST)
        formset = AnswerFormSet(request.POST)

        if question_form.is_valid() and formset.is_valid():
            question = question_form.save(commit=False)
            question.quiz = quiz
            question.save()

            answers = formset.save(commit=False)
            for answer in answers:
                answer.question = question
                answer.save()

            return redirect('add_question', quiz_id=quiz.id)  # Для добавления еще одного вопроса
    else:
        question_form = QuestionForm()
        formset = AnswerFormSet(queryset=Answer.objects.none())

    return render(request, 'courses/add_question.html', {
        'question_form': question_form,
        'formset': formset,
        'quiz': quiz,
    })
from .forms import QuizToModuleForm


def bind_quiz_to_module(request):
    if request.method == 'POST':
        form = QuizToModuleForm(request.POST)
        if form.is_valid():
            course = form.cleaned_data['course']
            module = form.cleaned_data['module']
            quiz = form.cleaned_data['quiz']

            # Привязка квиза к модулю
            module.quizzes.add(quiz)

            return redirect('success')  # Перенаправление после успешного сохранения
    else:
        form = QuizToModuleForm()

    return render(request, 'courses/choose.html', {'form': form})

def success_view(request):
    return render(request, 'courses/success.html')