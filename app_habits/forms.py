from django import forms

from app_habits.models import Habit


class HabitForm(forms.ModelForm):
    class Meta:
        fields = '__all__'
        model = Habit

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['linked_habit'].queryset = Habit.objects.filter(
            # Q(is_public=True) | Q(owner=self.instance.owner),
            is_pleasantly=True
        )
