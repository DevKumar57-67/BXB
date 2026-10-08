from django.db.models import Case, IntegerField, Q, Value, When
from django.http import JsonResponse
from django.shortcuts import render

from posts.models import Post
from users.models import User


def search(request):
    query = request.GET.get("q", "").strip()
    search_type = request.GET.get("type", "all")

    people = User.objects.none()
    posts = Post.objects.none()

    if query:
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
                        When(
                            username__iexact=query,
                            then=Value(1)
                        ),
                        When(
                            first_name__iexact=query,
                            then=Value(2)
                        ),
                        When(
                            last_name__iexact=query,
                            then=Value(2)
                        ),
                        When(
                            username__istartswith=query,
                            then=Value(3)
                        ),
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
                        When(
                            author__username__iexact=query,
                            then=Value(1)
                        ),
                        When(
                            content__istartswith=query,
                            then=Value(2)
                        ),
                        default=Value(3),
                        output_field=IntegerField(),
                    )
                )
                .select_related("author", "author__profile")
                .order_by("relevance", "-created_at")
            )

    context = {
        "query": query,
        "search_type": search_type,
        "people": people,
        "posts": posts,
    }

    return render(
        request,
        "search/results.html",
        context
    )


def search_suggestions(request):
    query = request.GET.get("q", "").strip()

    if len(query) < 2:
        return JsonResponse({
            "results": []
        })

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

    results = []

    for person in people:
        if person.get_full_name():
            title = person.get_full_name()
        else:
            title = person.username

        if person.profile.college:
            subtitle = f"@{person.username} · {person.profile.college}"
        else:
            subtitle = f"@{person.username}"

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
                f"/search/?q="
                f"{query}&type=posts"
            ),
            "avatar": (
                post.author.profile.avatar.url
                if post.author.profile.avatar
                else ""
            ),
        })

    return JsonResponse({
        "results": results[:8]
    })