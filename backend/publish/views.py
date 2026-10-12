from django.shortcuts import render

# Create your views here.

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils import timezone

from .forms import ProjectForm


@login_required
def create_project(request):
    if request.method == "POST":
        form = ProjectForm(
            request.POST,
            request.FILES,
        )

        if form.is_valid():
            project = form.save(commit=False)
            project.creator = request.user

            action = request.POST.get("action", "publish")

            if action == "draft":
                project.status = project.Status.DRAFT
                project.published_at = None
                message = "Your project has been saved as a draft."
            else:
                project.status = project.Status.PUBLISHED
                project.published_at = timezone.now()
                message = "Your project has been published to Studio!"

            project.save()

            messages.success(request, message)
            return redirect("publish:create")

    else:
        form = ProjectForm()

    return render(
        request,
        "publish/project_form.html",
        {"form": form},
    )
