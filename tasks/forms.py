from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'category', 'due_date', 'completed'] # Добавили due_date
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'due_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}), # Календарик
            'completed': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    # Тот самый Шаг 15: Валидация заголовка
    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) < 3:
            # Если название слишком короткое, Django выкинет ошибку прямо в форме
            raise forms.ValidationError("Название слишком короткое! Минимум 3 символа.")
        return title