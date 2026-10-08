from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from users.models import User

from .models import Handshake


@login_required
def send_handshake(request, username):

    if request.method != "POST":
        return JsonResponse(
            {
                "success": False,
                "error": "POST request required."
            },
            status=405
        )

    receiver = get_object_or_404(
        User,
        username=username
    )

    # -----------------------------------------------------
    # PREVENT SELF-HANDSHAKE
    # -----------------------------------------------------

    if receiver == request.user:
        return JsonResponse(
            {
                "success": False,
                "error": "You cannot send a handshake to yourself."
            },
            status=400
        )

    # -----------------------------------------------------
    # CHECK CURRENT DIRECTION
    # -----------------------------------------------------

    existing = (
        Handshake.objects
        .filter(
            sender=request.user,
            receiver=receiver
        )
        .first()
    )

    if existing:

        # Already pending.
        if existing.status == Handshake.Status.PENDING:

            return JsonResponse(
                {
                    "success": False,
                    "error": "Handshake request already pending.",
                    "status": existing.status,
                    "handshake_id": existing.id,
                },
                status=400
            )

        # Already connected.
        if existing.status == Handshake.Status.ACCEPTED:

            return JsonResponse(
                {
                    "success": False,
                    "error": "You are already connected.",
                    "status": existing.status,
                    "handshake_id": existing.id,
                },
                status=400
            )

        # Previously rejected.
        # Allow the sender to send the request again.
        if existing.status == Handshake.Status.REJECTED:

            existing.status = Handshake.Status.PENDING

            existing.save(
                update_fields=[
                    "status",
                    "updated_at"
                ]
            )

            return JsonResponse(
                {
                    "success": True,
                    "status": Handshake.Status.PENDING,
                    "handshake_id": existing.id,
                    "message": "Handshake request sent again."
                }
            )

    # -----------------------------------------------------
    # CHECK REVERSE DIRECTION
    # -----------------------------------------------------

    reverse = (
        Handshake.objects
        .filter(
            sender=receiver,
            receiver=request.user
        )
        .first()
    )

    if reverse:

        # The other person already sent us a pending request.
        # Sending one back means accepting that request.
        if reverse.status == Handshake.Status.PENDING:

            reverse.status = Handshake.Status.ACCEPTED

            reverse.save(
                update_fields=[
                    "status",
                    "updated_at"
                ]
            )

            return JsonResponse(
                {
                    "success": True,
                    "status": Handshake.Status.ACCEPTED,
                    "handshake_id": reverse.id,
                    "message": "Handshake accepted."
                }
            )

        # Already connected.
        if reverse.status == Handshake.Status.ACCEPTED:

            return JsonResponse(
                {
                    "success": False,
                    "error": "You are already connected.",
                    "status": reverse.status,
                    "handshake_id": reverse.id,
                },
                status=400
            )

        # -------------------------------------------------
        # REVERSE REQUEST WAS REJECTED
        # -------------------------------------------------
        #
        # Do NOT automatically accept it.
        # We allow a completely new request in the
        # opposite direction.
        #

        if reverse.status == Handshake.Status.REJECTED:

            handshake = Handshake.objects.create(
                sender=request.user,
                receiver=receiver,
                status=Handshake.Status.PENDING
            )

            return JsonResponse(
                {
                    "success": True,
                    "status": Handshake.Status.PENDING,
                    "handshake_id": handshake.id,
                    "message": "New handshake request sent."
                }
            )

    # -----------------------------------------------------
    # BRAND NEW REQUEST
    # -----------------------------------------------------

    handshake = Handshake.objects.create(
        sender=request.user,
        receiver=receiver,
        status=Handshake.Status.PENDING
    )

    return JsonResponse(
        {
            "success": True,
            "status": Handshake.Status.PENDING,
            "handshake_id": handshake.id,
            "message": "Handshake request sent."
        }
    )


@login_required
def accept_handshake(request, handshake_id):

    if request.method != "POST":
        return JsonResponse(
            {
                "success": False,
                "error": "POST request required."
            },
            status=405
        )

    handshake = get_object_or_404(
        Handshake,
        id=handshake_id
    )

    # Only the receiver can accept.
    if handshake.receiver != request.user:

        return JsonResponse(
            {
                "success": False,
                "error": "You are not allowed to accept this request."
            },
            status=403
        )

    if handshake.status != Handshake.Status.PENDING:

        return JsonResponse(
            {
                "success": False,
                "error": "This handshake is no longer pending.",
                "status": handshake.status,
            },
            status=400
        )

    handshake.status = Handshake.Status.ACCEPTED

    handshake.save(
        update_fields=[
            "status",
            "updated_at"
        ]
    )

    return JsonResponse(
        {
            "success": True,
            "status": Handshake.Status.ACCEPTED,
            "handshake_id": handshake.id,
            "message": "Handshake accepted."
        }
    )


@login_required
def reject_handshake(request, handshake_id):

    if request.method != "POST":
        return JsonResponse(
            {
                "success": False,
                "error": "POST request required."
            },
            status=405
        )

    handshake = get_object_or_404(
        Handshake,
        id=handshake_id
    )

    # Only the receiver can reject.
    if handshake.receiver != request.user:

        return JsonResponse(
            {
                "success": False,
                "error": "You are not allowed to reject this request."
            },
            status=403
        )

    if handshake.status != Handshake.Status.PENDING:

        return JsonResponse(
            {
                "success": False,
                "error": "This handshake is no longer pending.",
                "status": handshake.status,
            },
            status=400
        )

    handshake.status = Handshake.Status.REJECTED

    handshake.save(
        update_fields=[
            "status",
            "updated_at"
        ]
    )

    return JsonResponse(
        {
            "success": True,
            "status": Handshake.Status.REJECTED,
            "handshake_id": handshake.id,
            "message": "Handshake rejected."
        }
    )


@login_required
def cancel_handshake(request, handshake_id):

    if request.method != "POST":
        return JsonResponse(
            {
                "success": False,
                "error": "POST request required."
            },
            status=405
        )

    handshake = get_object_or_404(
        Handshake,
        id=handshake_id
    )

    # Only the sender can cancel.
    if handshake.sender != request.user:

        return JsonResponse(
            {
                "success": False,
                "error": "You are not allowed to cancel this request."
            },
            status=403
        )

    if handshake.status != Handshake.Status.PENDING:

        return JsonResponse(
            {
                "success": False,
                "error": "Only pending requests can be cancelled.",
                "status": handshake.status,
            },
            status=400
        )

    handshake.delete()

    return JsonResponse(
        {
            "success": True,
            "status": "cancelled",
            "message": "Handshake request cancelled."
        }
    )