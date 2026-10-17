from django.shortcuts import render

# Create your views here.

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import VibeCreateForm
from .models import Vibe
from .forms import VibeCreateForm
from .models import Vibe, VibeComment, VibeLike
from django.views.decorators.http import require_POST

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
            form.save_tags(vibe)

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


@login_required
@require_POST
def toggle_vibe_like(request, pk):
    vibe = get_object_or_404(Vibe, pk=pk, is_public=True)

    like = VibeLike.objects.filter(
        vibe=vibe,
        user=request.user,
    )

    if like.exists():
        like.delete()
    else:
        VibeLike.objects.get_or_create(
            vibe=vibe,
            user=request.user,
        )

    return redirect("vibespace:detail", pk=pk)


@login_required
@require_POST
def add_vibe_comment(request, pk):
    vibe = get_object_or_404(Vibe, pk=pk, is_public=True)
    text = request.POST.get("text", "").strip()

    if not text:
        messages.error(request, "Please write a comment first.")
    elif len(text) > 1000:
        messages.error(
            request,
            "Comments must be 1,000 characters or fewer.",
        )
    else:
        VibeComment.objects.create(
            vibe=vibe,
            user=request.user,
            text=text,
        )
        messages.success(request, "Comment added.")

    return redirect("vibespace:detail", pk=pk)
