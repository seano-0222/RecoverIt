from django import forms
from .models import Item, Message


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['item_name', 'category', 'description', 'type', 'location', 'date_reported', 'image']
        widgets = {
            'item_name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'type': forms.Select(attrs={'class': 'form-select'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'date_reported': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        item_name = cleaned_data.get('item_name')
        item_type = cleaned_data.get('type')

        if self.user and item_name and item_type:
            duplicates = Item.objects.filter(
                user=self.user,
                item_name__iexact=item_name,
                type=item_type,
            ).exclude(status='resolved')

            if self.instance.pk:
                duplicates = duplicates.exclude(pk=self.instance.pk)

            if duplicates.exists():
                raise forms.ValidationError(
                    f"You already have an active '{item_type}' report for \"{item_name}\". "
                    "Edit your existing report instead of creating a duplicate."
                )

        return cleaned_data


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Type a message...'}),
        }