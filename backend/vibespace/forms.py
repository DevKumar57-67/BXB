
from django import forms

from .models import Vibe


class VibeCreateForm(forms.ModelForm):
    class Meta:
        model = Vibe
        fields = ["media", "caption"]

        widgets = {
            "media": forms.ClearableFileInput(
                attrs={
                    "accept": (
                        "image/jpeg,image/png,image/webp,"
                        "image/gif,video/mp4,video/webm,"
                        "video/quicktime"
                    ),
                    "class": "vibe-file-input",
                }
            ),
            "caption": forms.Textarea(
                attrs={
                    "placeholder": "What's the vibe? ✨",
                    "rows": 3,
                    "maxlength": 500,
                    "class": "vibe-caption-input",
                }
            ),
        }

    def clean_media(self):
        media = self.cleaned_data.get("media")

        if not media:
            raise forms.ValidationError(
                "Please select an image, GIF, or video."
            )

        return media
