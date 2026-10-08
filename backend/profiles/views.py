from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from handshake.models import Handshake
from users.models import User

from .forms import ProfileForm


@login_required
def my_profile(request):
    profile = request.user.profile

    return render(
        request,
        'profiles/my_profile.html',
        {
            'profile': profile,
        }
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

        form = ProfileForm(
            instance=profile
        )

    return render(
        request,
        'profiles/edit_profile.html',
        {
            'form': form,
        }
    )


def public_profile(request, username):

    profile_user = get_object_or_404(
        User,
        username=username
    )

    profile = profile_user.profile

    # Default Handshake state.
    handshake_status = 'none'
    handshake_id = ''

    # -----------------------------------------------------
    # HANDSHAKE STATE FOR LOGGED-IN USERS
    # -----------------------------------------------------

    if (
        request.user.is_authenticated
        and request.user != profile_user
    ):

        sent_handshake = (
            Handshake.objects
            .filter(
                sender=request.user,
                receiver=profile_user
            )
            .first()
        )

        received_handshake = (
            Handshake.objects
            .filter(
                sender=profile_user,
                receiver=request.user
            )
            .first()
        )

        # Accepted relationship has highest priority.
        if (
            sent_handshake
            and sent_handshake.status
            == Handshake.Status.ACCEPTED
        ):

            handshake_status = 'accepted'
            handshake_id = sent_handshake.id

        elif (
            received_handshake
            and received_handshake.status
            == Handshake.Status.ACCEPTED
        ):

            handshake_status = 'accepted'
            handshake_id = received_handshake.id

        # Incoming pending request.
        elif (
            received_handshake
            and received_handshake.status
            == Handshake.Status.PENDING
        ):

            handshake_status = 'pending_received'
            handshake_id = received_handshake.id

        # Outgoing pending request.
        elif (
            sent_handshake
            and sent_handshake.status
            == Handshake.Status.PENDING
        ):

            handshake_status = 'pending_sent'
            handshake_id = sent_handshake.id

        # A rejected outgoing request can be sent again.
        elif (
            sent_handshake
            and sent_handshake.status
            == Handshake.Status.REJECTED
        ):

            handshake_status = 'rejected'
            handshake_id = sent_handshake.id


    # -----------------------------------------------------
    # PROFILE CONNECTION COUNTS
    # -----------------------------------------------------

    connection_count = (
        Handshake.objects
        .filter(
            Q(sender=profile_user)
            | Q(receiver=profile_user),
            status=Handshake.Status.ACCEPTED
        )
        .count()
    )


    handshake_count = (
        Handshake.objects
        .filter(
            Q(sender=profile_user)
            | Q(receiver=profile_user)
        )
        .count()
    )


    return render(
        request,
        'profiles/public_profile.html',
        {
            'profile': profile,
            'profile_user': profile_user,
            'handshake_status': handshake_status,
            'handshake_id': handshake_id,
            'connection_count': connection_count,
            'handshake_count': handshake_count,
        }
    )