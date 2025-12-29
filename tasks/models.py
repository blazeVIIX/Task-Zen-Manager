from django.db import models
from django.contrib.auth.models import User # Это нам понадобится для шага с регистрацией

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название категории")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

class Task(models.Model):
    # Добавляем связь с пользователем (для будущего шага с регистрацией)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Категория")
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    description = models.TextField(blank=True, verbose_name="Описание")
    
    # ВОТ ОН, ШАГ 26: ПОЛЕ ДЛЯ ДЕДЛАЙНА
    due_date = models.DateTimeField(null=True, blank=True, verbose_name="Дедлайн")
    
    completed = models.BooleanField(default=False, verbose_name="Выполнено")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title