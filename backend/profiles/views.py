'''

from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import ProfileForm


@login_required
def edit_profile(request):
    profile = request.user.profile

    if request.method == 'POST':
        form = ProfileForm(
            request.POST,
            request.FILES,
            instance=profile
        )

        if form.is_valid():
            form.save()
            return redirect('my_profile')

    else:
        form = ProfileForm(instance=profile)

    return render(
        request,
        'profiles/edit_profile.html',
        {'form': form}
    )

    '''

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .forms import ProfileForm
from users.models import User


@login_required
def my_profile(request):
    profile = request.user.profile

    return render(
        request,
        'profiles/my_profile.html',
        {'profile': profile}
    )


@login_required
def edit_profile(request):
    profile = request.user.profile

    if request.method == 'POST':
        form = ProfileForm(
            request.POST,
            request.FILES,
            instance=profile
        )

        if form.is_valid():
            form.save()
            return redirect('my_profile')

    else:
        form = ProfileForm(instance=profile)

    return render(
        request,
        'profiles/edit_profile.html',
        {'form': form}
    )


def public_profile(request, username):
    user = get_object_or_404(User, username=username)
    profile = user.profile

    return render(
        request,
        'profiles/public_profile.html',
        {
            'profile': profile,
            'profile_user': user,
        }
    )