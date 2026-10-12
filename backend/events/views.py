
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError, transaction
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.utils.text import slugify
from django.views.decorators.http import require_POST

from .forms import EventCreateForm
from .models import (
    Event,
    EventRegistration,
    EventTeam,
    EventTeamMembership,
)


def event_list(request):
    """Display published college events."""
    now = timezone.now()

    events = (
        Event.objects.filter(status=Event.Status.PUBLISHED)
        .annotate(
            registration_count=Count(
                "registrations",
                filter=Q(
                    registrations__status=EventRegistration.Status.REGISTERED
                ),
                distinct=True,
            )
        )
        .order_by("start_date")
    )

    upcoming_events = events.filter(start_date__gte=now)
    ongoing_events = events.filter(start_date__lt=now, end_date__gte=now)
    past_events = events.filter(end_date__lt=now)

    return render(
        request,
        "events/event_list.html",
        {
            "events": events,
            "upcoming_events": upcoming_events,
            "ongoing_events": ongoing_events,
            "past_events": past_events,
        },
    )


@login_required
def event_detail(request, slug):
    """Display event details and the current user's participation status."""
    event = get_object_or_404(
        Event,
        slug=slug,
        status=Event.Status.PUBLISHED,
    )

    registration = EventRegistration.objects.filter(
        event=event,
        user=request.user,
        status=EventRegistration.Status.REGISTERED,
    ).first()

    teams = (
        EventTeam.objects.filter(event=event)
        .annotate(member_count=Count("members", distinct=True))
        .order_by("name")
    )

    user_team = EventTeam.objects.filter(
        event=event,
        memberships__user=request.user,
    ).first()

    return render(
        request,
        "events/event_detail.html",
        {
            "event": event,
            "registration": registration,
            "teams": teams,
            "user_team": user_team,
        },
    )


@login_required
def my_events(request):
    """Show the current user's event registrations and team memberships."""
    registrations = (
        EventRegistration.objects.filter(
            user=request.user,
            status=EventRegistration.Status.REGISTERED,
        )
        .select_related("event")
        .order_by("event__start_date")
    )

    teams = (
        EventTeam.objects.filter(members=request.user)
        .select_related("event", "leader")
        .annotate(member_count=Count("members", distinct=True))
        .order_by("event__start_date")
    )

    return render(
        request,
        "events/my_events.html",
        {
            "registrations": registrations,
            "teams": teams,
        },
    )


@login_required
@require_POST
def register_event(request, slug):
    """Register a student individually for an event."""
    event = get_object_or_404(
        Event,
        slug=slug,
        status=Event.Status.PUBLISHED,
    )

    if event.participation_type == Event.ParticipationType.TEAM:
        messages.info(
            request,
            "This event requires team participation. Create or join a team.",
        )
        return redirect("events:event_detail", slug=event.slug)

    if not event.is_registration_open:
        messages.error(request, "Registration for this event is closed.")
        return redirect("events:event_detail", slug=event.slug)

    if EventRegistration.objects.filter(
        event=event,
        user=request.user,
        status=EventRegistration.Status.REGISTERED,
    ).exists():
        messages.info(request, "You are already registered for this event.")
        return redirect("events:event_detail", slug=event.slug)

    try:
        with transaction.atomic():
            if event.max_participants is not None:
                registered_count = EventRegistration.objects.filter(
                    event=event,
                    status=EventRegistration.Status.REGISTERED,
                ).count()

                if registered_count >= event.max_participants:
                    messages.error(
                        request,
                        "This event has reached its capacity.",
                    )
                    return redirect("events:event_detail", slug=event.slug)

            EventRegistration.objects.update_or_create(
                event=event,
                user=request.user,
                defaults={
                    "registration_type": (
                        EventRegistration.RegistrationType.INDIVIDUAL
                    ),
                    "status": EventRegistration.Status.REGISTERED,
                },
            )

        messages.success(request, "You have registered successfully!")

    except IntegrityError:
        messages.info(request, "You may already be registered for this event.")

    return redirect("events:event_detail", slug=event.slug)


@login_required
@require_POST
def cancel_registration(request, slug):
    """Cancel registration and clean up the user's team if they lead it."""
    event = get_object_or_404(
        Event,
        slug=slug,
        status=Event.Status.PUBLISHED,
    )

    registration = EventRegistration.objects.filter(
        event=event,
        user=request.user,
        status=EventRegistration.Status.REGISTERED,
    ).first()

    if registration is None:
        messages.error(request, "You do not have an active registration.")
        return redirect("events:event_detail", slug=event.slug)

    with transaction.atomic():
        team = EventTeam.objects.filter(
            event=event,
            memberships__user=request.user,
        ).first()

        if team and team.leader_id == request.user.pk:
            team_members = list(team.members.all())

            EventRegistration.objects.filter(
                event=event,
                user__in=team_members,
                registration_type=EventRegistration.RegistrationType.TEAM,
                status=EventRegistration.Status.REGISTERED,
            ).update(status=EventRegistration.Status.CANCELLED)

            team.delete()

        elif team:
            EventTeamMembership.objects.filter(
                team=team,
                user=request.user,
            ).delete()

            registration.status = EventRegistration.Status.CANCELLED
            registration.save(update_fields=["status"])

        else:
            registration.status = EventRegistration.Status.CANCELLED
            registration.save(update_fields=["status"])

    messages.success(request, "Your registration has been cancelled.")
    return redirect("events:event_detail", slug=event.slug)


@login_required
@require_POST
def create_team(request, slug):
    """Create a team and register its leader for a team event."""
    event = get_object_or_404(
        Event,
        slug=slug,
        status=Event.Status.PUBLISHED,
    )

    if event.participation_type == Event.ParticipationType.INDIVIDUAL:
        messages.error(
            request,
            "This event only allows individual participation.",
        )
        return redirect("events:event_detail", slug=event.slug)

    if not event.is_registration_open:
        messages.error(request, "Registration for this event is closed.")
        return redirect("events:event_detail", slug=event.slug)

    team_name = request.POST.get("team_name", "").strip()

    if not team_name:
        messages.error(request, "Please enter a team name.")
        return redirect("events:event_detail", slug=event.slug)

    if len(team_name) > 100:
        messages.error(request, "Team names must be 100 characters or fewer.")
        return redirect("events:event_detail", slug=event.slug)

    if event.min_team_size < 1 or event.max_team_size < event.min_team_size:
        messages.error(request, "The event's team-size settings are invalid.")
        return redirect("events:event_detail", slug=event.slug)

    if EventRegistration.objects.filter(
        event=event,
        user=request.user,
        status=EventRegistration.Status.REGISTERED,
    ).exists():
        messages.error(
            request,
            "You are already registered for this event. "
            "Cancel that registration before creating a team.",
        )
        return redirect("events:event_detail", slug=event.slug)

    if EventTeam.objects.filter(event=event, name__iexact=team_name).exists():
        messages.error(
            request,
            "A team with that name already exists for this event.",
        )
        return redirect("events:event_detail", slug=event.slug)

    try:
        with transaction.atomic():
            if event.max_participants is not None:
                registered_count = EventRegistration.objects.filter(
                    event=event,
                    status=EventRegistration.Status.REGISTERED,
                ).count()

                if registered_count >= event.max_participants:
                    messages.error(
                        request,
                        "This event has reached its capacity.",
                    )
                    return redirect("events:event_detail", slug=event.slug)

            team = EventTeam.objects.create(
                event=event,
                name=team_name,
                leader=request.user,
            )

            EventTeamMembership.objects.create(
                team=team,
                user=request.user,
            )

            EventRegistration.objects.create(
                event=event,
                user=request.user,
                registration_type=EventRegistration.RegistrationType.TEAM,
                status=EventRegistration.Status.REGISTERED,
            )

        messages.success(
            request,
            f"Team '{team_name}' created successfully. You are its leader.",
        )

    except IntegrityError:
        messages.error(
            request,
            "The team could not be created. Check whether its name is "
            "already in use.",
        )

    return redirect("events:event_detail", slug=event.slug)


@login_required
@require_POST
def join_team(request, slug, team_id):
    """Join an existing team if its event and team-size rules allow it."""
    event = get_object_or_404(
        Event,
        slug=slug,
        status=Event.Status.PUBLISHED,
    )

    team = get_object_or_404(
        EventTeam.objects.select_related("event"),
        id=team_id,
        event=event,
    )

    if event.participation_type == Event.ParticipationType.INDIVIDUAL:
        messages.error(
            request,
            "This event only allows individual participation.",
        )
        return redirect("events:event_detail", slug=event.slug)

    if not event.is_registration_open:
        messages.error(request, "Registration for this event is closed.")
        return redirect("events:event_detail", slug=event.slug)

    if EventRegistration.objects.filter(
        event=event,
        user=request.user,
        status=EventRegistration.Status.REGISTERED,
    ).exists():
        messages.error(request, "You are already registered for this event.")
        return redirect("events:event_detail", slug=event.slug)

    if team.members.filter(pk=request.user.pk).exists():
        messages.info(request, "You are already a member of this team.")
        return redirect("events:event_detail", slug=event.slug)

    try:
        with transaction.atomic():
            member_count = EventTeamMembership.objects.filter(
                team=team,
            ).count()

            if member_count >= event.max_team_size:
                messages.error(request, "This team is already full.")
                return redirect("events:event_detail", slug=event.slug)

            if event.max_participants is not None:
                registered_count = EventRegistration.objects.filter(
                    event=event,
                    status=EventRegistration.Status.REGISTERED,
                ).count()

                if registered_count >= event.max_participants:
                    messages.error(
                        request,
                        "This event has reached its capacity.",
                    )
                    return redirect("events:event_detail", slug=event.slug)

            EventTeamMembership.objects.create(
                team=team,
                user=request.user,
            )

            EventRegistration.objects.create(
                event=event,
                user=request.user,
                registration_type=EventRegistration.RegistrationType.TEAM,
                status=EventRegistration.Status.REGISTERED,
            )

        messages.success(
            request,
            f"You have joined '{team.name}' successfully!",
        )

    except IntegrityError:
        messages.error(request, "You could not join this team. Please try again.")

    return redirect("events:event_detail", slug=event.slug)


# =====================================================
# CREATE EVENT
# =====================================================

@login_required
def create_event(request):
    """Create an event, including optional uploaded banner and poster images."""
    if request.method == "POST":
        # request.FILES is required for uploaded images.
        form = EventCreateForm(request.POST, request.FILES)

        if form.is_valid():
            event = form.save(commit=False)

            # Generate a unique URL slug from the event title.
            base_slug = slugify(event.title) or "event"
            unique_slug = base_slug
            counter = 2

            while Event.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{base_slug}-{counter}"
                counter += 1

            event.slug = unique_slug
            event.created_by = request.user
            event.status = Event.Status.PUBLISHED
            event.save()

            messages.success(
                request,
                "Your event has been published successfully!",
            )

            return redirect(
                "events:event_detail",
                slug=event.slug,
            )

    else:
        form = EventCreateForm()

    return render(
        request,
        "events/create_event.html",
        {"form": form},
    )
