
from urllib.parse import urlencode

from django.contrib.auth.decorators import login_required
from django.db.models import Case, IntegerField, Q, Value, When
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.http import require_POST

from events.models import Event
from posts.models import Post
from users.models import User

from .models import SearchHistory


def search(request):
    query = request.GET.get("q", "").strip()[:200]
    search_type = request.GET.get("type", "all")

    if search_type not in ("all", "people", "posts", "events"):
        search_type = "all"

    people = User.objects.none()
    posts = Post.objects.none()
    events = Event.objects.none()

    if query:
        # Save this query only for authenticated users.
        if request.user.is_authenticated:
            SearchHistory.objects.create(
                user=request.user,
                query=query,
            )

        if search_type in ("all", "people"):
            people = (
                User.objects
                .filter(
                    Q(username__icontains=query)
                    | Q(first_name__icontains=query)
                    | Q(last_name__icontains=query)
                    | Q(profile__bio__icontains=query)
                    | Q(profile__college__icontains=query)
                    | Q(profile__course__icontains=query)
                    | Q(profile__skills__icontains=query)
                    | Q(profile__interests__icontains=query)
                )
                .annotate(
                    relevance=Case(
                        When(username__iexact=query, then=Value(1)),
                        When(first_name__iexact=query, then=Value(2)),
                        When(last_name__iexact=query, then=Value(2)),
                        When(username__istartswith=query, then=Value(3)),
                        default=Value(4),
                        output_field=IntegerField(),
                    )
                )
                .select_related("profile")
                .distinct()
                .order_by("relevance", "username")
            )

        if search_type in ("all", "posts"):
            posts = (
                Post.objects
                .filter(
                    Q(content__icontains=query)
                    | Q(author__username__icontains=query)
                )
                .annotate(
                    relevance=Case(
                        When(author__username__iexact=query, then=Value(1)),
                        When(content__istartswith=query, then=Value(2)),
                        default=Value(3),
                        output_field=IntegerField(),
                    )
                )
                .select_related("author", "author__profile")
                .order_by("relevance", "-created_at")
            )

        if search_type in ("all", "events"):
            events = (
                Event.objects
                .filter(status=Event.Status.PUBLISHED)
                .filter(
                    Q(title__icontains=query)
                    | Q(description__icontains=query)
                    | Q(organizer__icontains=query)
                    | Q(venue__icontains=query)
                )
                .order_by("start_date", "title")
            )

    recent_searches = []
    if request.user.is_authenticated:
        recent_searches = (
            SearchHistory.objects
            .filter(user=request.user)
            .order_by("-created_at")[:10]
        )

    context = {
        "query": query,
        "search_type": search_type,
        "people": people,
        "posts": posts,
        "events": events,
        "recent_searches": recent_searches,
    }

    return render(request, "search/results.html", context)


def search_suggestions(request):
    query = request.GET.get("q", "").strip()[:200]

    if len(query) < 2:
        return JsonResponse({"results": []})

    people = (
        User.objects
        .filter(
            Q(username__icontains=query)
            | Q(first_name__icontains=query)
            | Q(last_name__icontains=query)
            | Q(profile__college__icontains=query)
            | Q(profile__course__icontains=query)
            | Q(profile__skills__icontains=query)
            | Q(profile__interests__icontains=query)
        )
        .select_related("profile")
        .distinct()
        .order_by("username")[:5]
    )

    posts = (
        Post.objects
        .filter(
            Q(content__icontains=query)
            | Q(author__username__icontains=query)
        )
        .select_related("author", "author__profile")
        .order_by("-created_at")[:5]
    )

    events = (
        Event.objects
        .filter(status=Event.Status.PUBLISHED)
        .filter(
            Q(title__icontains=query)
            | Q(description__icontains=query)
            | Q(organizer__icontains=query)
            | Q(venue__icontains=query)
        )
        .order_by("start_date", "title")[:5]
    )

    results = []

    for person in people:
        title = person.get_full_name() or person.username
        subtitle = (
            f"@{person.username} · {person.profile.college}"
            if person.profile.college
            else f"@{person.username}"
        )

        results.append({
            "type": "person",
            "title": title,
            "subtitle": subtitle,
            "url": f"/profile/u/{person.username}/",
            "avatar": (
                person.profile.avatar.url
                if person.profile.avatar
                else ""
            ),
        })

    for post in posts:
        content = post.content.strip().replace("\n", " ")
        if len(content) > 80:
            content = content[:80] + "..."

        results.append({
            "type": "post",
            "title": f"@{post.author.username}",
            "subtitle": content,
            "url": (
                 f"{reverse('search')}?"
                 f"{urlencode({'q': query, 'type': 'posts'})}"
),
            "avatar": (
                post.author.profile.avatar.url
                if hasattr(post.author, "profile")
                and post.author.profile.avatar
                else ""
            ),
        })

    for event in events:
        results.append({
            "type": "event",
            "title": event.title,
            "subtitle": f"{event.organizer} · {event.venue or 'Online / venue TBA'}",
            "url": reverse("events:event_detail", kwargs={"slug": event.slug}),
            "avatar": event.banner.url if event.banner else event.image or "",
        })

    # Include the user's own recent searches in autocomplete.
    if request.user.is_authenticated:
        history = (
            SearchHistory.objects
            .filter(user=request.user, query__icontains=query)
            .order_by("-created_at")
            .values_list("query", flat=True)
            .distinct()[:3]
        )

        for previous_query in history:
            results.append({
                "type": "history",
                "title": previous_query,
                "subtitle": "Recent search",
                "url": (
                    f"{reverse('search')}?"
                    f"{urlencode({'q': previous_query})}"
                ),
                "avatar": "",
            })

    return JsonResponse({"results": results[:10]})


@login_required
@require_POST
def clear_search_history(request):
    SearchHistory.objects.filter(user=request.user).delete()
    return JsonResponse({"success": True})


@login_required
@require_POST
def delete_search_history_item(request):
    query = request.POST.get("query", "").strip()[:200]

    SearchHistory.objects.filter(
        user=request.user,
        query=query,
    ).delete()

    return JsonResponse({"success": True})
