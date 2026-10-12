
from django import forms
from .models import Project


class ProjectForm(forms.ModelForm):

    class Meta:
        model = Project

        fields = [
            "title",
            "description",
            "category",
            "technologies",
            "cover_image",
            "demo_video_url",
            "project_url",
            "repository_url",
        ]

        widgets = {
            "title": forms.TextInput(attrs={
                "placeholder": "Give your creation a memorable name",
                "maxlength": 120,
            }),

            "description": forms.Textarea(attrs={
                "placeholder": (
                    "What did you build? What problem does it solve? "
                    "What makes it interesting?"
                ),
                "rows": 6,
            }),

            "category": forms.Select(),

            "technologies": forms.TextInput(attrs={
                "placeholder": "Python, Django, PyTorch, Figma...",
            }),

            "demo_video_url": forms.URLInput(attrs={
                "placeholder": "https://...",
            }),

            "project_url": forms.URLInput(attrs={
                "placeholder": "https://your-project.com",
            }),

            "repository_url": forms.URLInput(attrs={
                "placeholder": "https://github.com/username/project",
            }),
        }

    def clean_cover_image(self):
        image = self.cleaned_data.get("cover_image")

        if image:
            if image.size > 5 * 1024 * 1024:
                raise forms.ValidationError(
                    "The cover image must be 5 MB or smaller."
                )

            allowed_types = [
                "image/jpeg",
                "image/png",
                "image/webp",
            ]

            if getattr(image, "content_type", "") not in allowed_types:
                raise forms.ValidationError(
                    "Upload a JPG, PNG, or WebP image."
                )

        return image
