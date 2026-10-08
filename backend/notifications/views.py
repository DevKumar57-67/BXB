from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render

from .models import Notification


@login_required
def notification_list(request):
    notifications = (
        Notification.objects
        .filter(recipient=request.user)
        .select_related(
            "actor",
            "post",
            "handshake",
            "comment"
        )
        .order_by("-created_at")
    )

    unread_count = notifications.filter(
        is_read=False
    ).count()

    return render(
        request,
        "notifications/list.html",
        {
            "notifications": notifications,
            "unread_count": unread_count,
        }
    )


@login_required
def unread_count(request):
    count = Notification.objects.filter(
        recipient=request.user,
        is_read=False
    ).count()

    return JsonResponse(
        {
            "success": True,
            "unread_count": count,
        }
    )


@login_required
def mark_as_read(request, notification_id):

    if request.method != "POST":
        return JsonResponse(
            {
                "success": False,
                "error": "POST request required."
            },
            status=405
        )

    notification = (
        Notification.objects
        .filter(
            id=notification_id,
            recipient=request.user
        )
        .first()
    )

    if not notification:
        return JsonResponse(
            {
                "success": False,
                "error": "Notification not found."
            },
            status=404
        )

    notification.is_read = True

    notification.save(
        update_fields=["is_read"]
    )

    unread = Notification.objects.filter(
        recipient=request.user,
        is_read=False
    ).count()

    return JsonResponse(
        {
            "success": True,
            "unread_count": unread,
        }
    )


@login_required
def mark_all_as_read(request):

    if request.method != "POST":
        return JsonResponse(
            {
                "success": False,
                "error": "POST request required."
            },
            status=405
        )

    updated = (
        Notification.objects
        .filter(
            recipient=request.user,
            is_read=False
        )
        .update(is_read=True)
    )

    return JsonResponse(
        {
            "success": True,
            "updated": updated,
            "unread_count": 0,
        }
    )