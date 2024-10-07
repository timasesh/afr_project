# courses/forms.py
# courses/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Lesson, Module, Course
from .models import Question, Answer

class StudentRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'is_student']

class LessonCreationForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['title', 'video', 'pdf']

class ModuleCreationForm(forms.ModelForm):
    class Meta:
        model = Module
        fields = ['title', 'lessons']
        widgets = {
            'lessons': forms.CheckboxSelectMultiple
        }

class CourseCreationForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description', 'modules']
        widgets = {
            'modules': forms.CheckboxSelectMultiple
        }
class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text']

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text']

from django import forms
from django.forms import inlineformset_factory
from .models import Quiz, Question, Answer

class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['title']

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text']

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text', 'is_correct']

# Создание формсета для ответа, чтобы можно было добавлять несколько ответов
AnswerFormSet = inlineformset_factory(Question, Answer, form=AnswerForm, extra=4)

from .models import Course, Module, Quiz, Lesson

class QuizToModuleForm(forms.Form):
    course = forms.ModelChoiceField(queryset=Course.objects.all(), required=True)
    module = forms.ModelChoiceField(queryset=Module.objects.all(), required=True)
    quiz = forms.ModelChoiceField(queryset=Quiz.objects.all(), required=True)

