from django.shortcuts import render

# Create your views here.

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import VibeCreateForm
from .models import Vibe


@login_required
def create_vibe(request):
    if request.method == "POST":
        form = VibeCreateForm(
            request.POST,
            request.FILES,
        )

        if form.is_valid():
            vibe = form.save(commit=False)
            vibe.author = request.user
            vibe.save()

            messages.success(
                request,
                "Your Vibe has been published!",
            )

            return redirect("vibespace:detail", pk=vibe.pk)
    else:
        form = VibeCreateForm()

    return render(
        request,
        "vibespace/create.html",
        {"form": form},
    )


def explore_vibes(request):
    vibes = (
        Vibe.objects
        .filter(is_public=True)
        .select_related("author")
    )

    return render(
        request,
        "vibespace/explore.html",
        {"vibes": vibes},
    )


@login_required
def my_vibes(request):
    vibes = (
        Vibe.objects
        .filter(author=request.user)
        .select_related("author")
    )

    return render(
        request,
        "vibespace/my_vibes.html",
        {"vibes": vibes},
    )


def vibe_detail(request, pk):
    vibe = get_object_or_404(
        Vibe.objects.select_related("author"),
        pk=pk,
    )

    if not vibe.is_public and vibe.author_id != request.user.id:
        from django.http import Http404
        raise Http404("Vibe not found.")

    return render(
        request,
        "vibespace/detail.html",
        {"vibe": vibe},
    )
