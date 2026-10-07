from django import forms

from .models import Post


class PostForm(forms.ModelForm):

    class Meta:
        model = Post

        fields = [
            'content',
            'image',
        ]

        widgets = {
            'content': forms.Textarea(
                attrs={
                    'placeholder': 'What is happening in your BxB community?',
                    'rows': 5,
                }
            ),
        }