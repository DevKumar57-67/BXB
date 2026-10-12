'''

from django.urls import path

from .views import (
    send_handshake,
    accept_handshake,
    reject_handshake,
    cancel_handshake,
)


urlpatterns = [

    path(
        "send/<str:username>/",
        send_handshake,
        name="send_handshake"
    ),

    path(
        "accept/<int:handshake_id>/",
        accept_handshake,
        name="accept_handshake"
    ),

    path(
        "reject/<int:handshake_id>/",
        reject_handshake,
        name="reject_handshake"
    ),

    path(
        "cancel/<int:handshake_id>/",
        cancel_handshake,
        name="cancel_handshake"
    ),

]

'''

from django.urls import path

from .views import (
    collaboration_submit,
    send_handshake,
    accept_handshake,
    reject_handshake,
    cancel_handshake,
)

urlpatterns = [
    path(
        "collaborate/<str:username>/",
        collaboration_submit,
        name="collaboration_submit",
    ),
    path("send/<str:username>/", send_handshake, name="send_handshake"),
    path("accept/<int:handshake_id>/", accept_handshake, name="accept_handshake"),
    path("reject/<int:handshake_id>/", reject_handshake, name="reject_handshake"),
    path("cancel/<int:handshake_id>/", cancel_handshake, name="cancel_handshake"),
]