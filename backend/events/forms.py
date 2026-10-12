
from django import forms
from django.utils import timezone

from .models import Event


class EventCreateForm(forms.ModelForm):
    class DateTimeInput(forms.DateTimeInput):
        input_type = "datetime-local"
        format = "%Y-%m-%dT%H:%M"

    start_date = forms.DateTimeField(
        widget=DateTimeInput(
            format="%Y-%m-%dT%H:%M",
            attrs={"class": "form-input"},
        ),
        input_formats=["%Y-%m-%dT%H:%M"],
    )

    end_date = forms.DateTimeField(
        widget=DateTimeInput(
            format="%Y-%m-%dT%H:%M",
            attrs={"class": "form-input"},
        ),
        input_formats=["%Y-%m-%dT%H:%M"],
    )

    registration_deadline = forms.DateTimeField(
        widget=DateTimeInput(
            format="%Y-%m-%dT%H:%M",
            attrs={"class": "form-input"},
        ),
        input_formats=["%Y-%m-%dT%H:%M"],
    )

    class Meta:
        model = Event
        fields = [
            "title",
            "description",
            "organizer",
            "venue",
            "start_date",
            "end_date",
            "registration_deadline",
            "participation_type",
            "max_participants",
            "min_team_size",
            "max_team_size",
            "image",
            "banner",
            "poster",
            "registration_link",
        ]

        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-input",
                    "placeholder": "e.g. BxB Hackathon 2026",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-input",
                    "rows": 6,
                    "placeholder": (
                        "Describe the event, activities, and eligibility."
                    ),
                }
            ),
            "organizer": forms.TextInput(
                attrs={
                    "class": "form-input",
                    "placeholder": "Club, society, or organising team",
                }
            ),
            "venue": forms.TextInput(
                attrs={
                    "class": "form-input",
                    "placeholder": "Campus, auditorium, online, etc.",
                }
            ),
            "participation_type": forms.Select(
                attrs={"class": "form-input"}
            ),
            "max_participants": forms.NumberInput(
                attrs={
                    "class": "form-input",
                    "min": 1,
                    "placeholder": "Leave blank for unlimited",
                }
            ),
            "min_team_size": forms.NumberInput(
                attrs={"class": "form-input", "min": 1}
            ),
            "max_team_size": forms.NumberInput(
                attrs={"class": "form-input", "min": 1}
            ),
            "image": forms.URLInput(
                attrs={
                    "class": "form-input",
                    "placeholder": "https://example.com/event-banner.jpg",
                }
            ),
            "banner": forms.ClearableFileInput(
                attrs={
                    "class": "form-input",
                    "accept": "image/*",
                }
            ),
            "poster": forms.ClearableFileInput(
                attrs={
                    "class": "form-input",
                    "accept": "image/*",
                }
            ),
            "registration_link": forms.URLInput(
                attrs={
                    "class": "form-input",
                    "placeholder": "Optional external registration URL",
                }
            ),
        }

    def clean(self):
        cleaned_data = super().clean()

        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")
        deadline = cleaned_data.get("registration_deadline")
        participation_type = cleaned_data.get("participation_type")
        min_team_size = cleaned_data.get("min_team_size")
        max_team_size = cleaned_data.get("max_team_size")

        now = timezone.now()

        if start_date and start_date <= now:
            self.add_error(
                "start_date",
                "The event must start in the future.",
            )

        if start_date and end_date and end_date <= start_date:
            self.add_error(
                "end_date",
                "The end date must be after the start date.",
            )

        if deadline and start_date and deadline >= start_date:
            self.add_error(
                "registration_deadline",
                "The registration deadline must be before the event starts.",
            )

        if deadline and deadline <= now:
            self.add_error(
                "registration_deadline",
                "The registration deadline must be in the future.",
            )

        if (
            participation_type
            in [
                Event.ParticipationType.TEAM,
                Event.ParticipationType.BOTH,
            ]
            and min_team_size is not None
            and max_team_size is not None
        ):
            if min_team_size < 1:
                self.add_error(
                    "min_team_size",
                    "A team must have at least one member.",
                )

            if max_team_size < min_team_size:
                self.add_error(
                    "max_team_size",
                    "Maximum team size cannot be smaller than minimum team size.",
                )

        return cleaned_data
