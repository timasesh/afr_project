from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models


class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_permissions_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )


class Lesson(models.Model):
    title = models.CharField(max_length=100)
    video = models.FileField(upload_to='videos/')
    pdf = models.FileField(upload_to='pdfs/', blank=True, null=True)

    def __str__(self):
        return self.title


class Quiz(models.Model):
    title = models.CharField(max_length=255)  # Название квиза

    def __str__(self):
        return self.title

    def questions(self):
        return self.question_set.all()


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, related_name='questions', on_delete=models.CASCADE)
    text = models.CharField(max_length=255)

    def __str__(self):
        return self.text


class Answer(models.Model):
    text = models.CharField(max_length=255)  # Текст ответа
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    is_correct = models.BooleanField(default=False)  # Правильный ли ответ

    def __str__(self):
        return f'{self.text} ({"Правильный" if self.is_correct else "Неправильный"})'


class Module(models.Model):
    title = models.CharField(max_length=100)
    lessons = models.ManyToManyField(Lesson)
    description = models.TextField(null=True, blank=True, default="")
    quizzes = models.ManyToManyField(Quiz, blank=True)  # Связь с квизами

    def __str__(self):
        return self.title


class Course(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    modules = models.ManyToManyField(Module, blank=True)

    def __str__(self):
        return self.title


class StudentProgress(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    progress = models.IntegerField(default=0)  # Прогресс в процентах

    def clean(self):
        if not (0 <= self.progress <= 100):
            raise ValidationError("Progress must be between 0 and 100.")

    def __str__(self):
        return f'{self.student.username} - {self.course.title} ({self.progress}%)'

