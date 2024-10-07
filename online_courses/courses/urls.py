from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),  # Страница входа
    path('admin_page/', views.admin_page, name='admin_page'),
    path('student_page/', views.student_page, name='student_page'),
    path('profile/', views.profile_page, name='profile'),
    path('logout/', views.logout_view, name='logout'),
    path('course/<int:course_id>/', views.course_detail, name='course_detail'),
    path('delete/student/<int:student_id>/', views.delete_student, name='delete_student'),
    path('delete/lesson/<int:lesson_id>/', views.delete_lesson, name='delete_lesson'),
    path('create/', views.create_quiz, name='create_quiz'),  # Создание квиза
    path('edit/<int:pk>/', views.edit_quiz, name='edit_quiz'),  # Редактирование квиза
    path('quizzes/', views.quiz_list, name='quiz_list'),  # Список квизов
    path('quiz/<int:quiz_id>/add-question/', views.add_question, name='add_question'),
    path('bind_quiz_to_module/<int:quiz_id>/', views.bind_quiz_to_module, name='bind_quiz_to_module'),
    path('success/', views.success_view, name='success'),
    path('quiz/<int:quiz_id>/', views.quiz_detail, name='quiz_detail'),
    path('delete/quiz/<int:quiz_id>/', views.delete_quiz, name='delete_quiz'),
    path('delete/course/<int:course_id>/', views.delete_course, name='delete_course'),
    path('create_course/', views.create_course, name='create_course'),
    path('module/details/<int:module_id>/', views.module_details, name='module_details'),
    path('show-lessons/', views.show_lessons, name='show_lessons'),
    path('get-lessons/<int:module_id>/', views.get_lessons, name='get_lessons'),
    path('delete/module/<int:module_id>', views.delete_module, name='delete_module'),
    path('create_module/', views.create_module, name='create_module_no_id'),
    path('create_module/<int:module_id>/', views.create_module, name='create_modul'),
]
