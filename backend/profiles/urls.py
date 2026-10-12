'''

from django.urls import path

from .views import edit_profile, my_profile, public_profile

urlpatterns = [
    path("", my_profile, name="my_profile"),
    path("edit/", edit_profile, name="edit_profile"),
    path("u/<str:username>/", public_profile, name="public_profile"),
]



from django.urls import path

from .views import (
    edit_profile,
    my_profile,
    public_profile,
    follow_user,
    unfollow_user,
)

urlpatterns = [
    path("", my_profile, name="my_profile"),
    path("edit/", edit_profile, name="edit_profile"),
    path("u/<str:username>/", public_profile, name="public_profile"),

    path("follow/<str:username>/", follow_user, name="follow_user"),
    path("unfollow/<str:username>/", unfollow_user, name="unfollow_user"),
]



from django.urls import path

from .views import (
    edit_profile,
    my_profile,
    public_profile,
    follow_user,
    unfollow_user,
    followers_list,
    following_list,
    connections_list,
    user_posts,
)

urlpatterns = [
    path("", my_profile, name="my_profile"),
    path("edit/", edit_profile, name="edit_profile"),

    path("u/<str:username>/", public_profile, name="public_profile"),

    path(
        "u/<str:username>/followers/",
        followers_list,
        name="followers_list",
    ),
    path(
        "u/<str:username>/following/",
        following_list,
        name="following_list",
    ),

    path("follow/<str:username>/", follow_user, name="follow_user"),
    path("unfollow/<str:username>/", unfollow_user, name="unfollow_user"),
    path("u/<str:username>/connections/", connections_list, name="connections_list"),
    path("u/<str:username>/posts/", user_posts, name="user_posts"),
]
'''


from django.urls import path

from .views import (
    edit_profile,
    my_profile,
    public_profile,
    follow_user,
    unfollow_user,
    followers_list,
    following_list,
    connections_list,
    user_posts,
)

urlpatterns = [
    path("", my_profile, name="my_profile"),
    path("edit/", edit_profile, name="edit_profile"),

    # Profile pages
    path("u/<str:username>/followers/", followers_list, name="followers_list"),
    path("u/<str:username>/following/", following_list, name="following_list"),
    path("u/<str:username>/connections/", connections_list, name="connections_list"),
    path("u/<str:username>/posts/", user_posts, name="user_posts"),
    path("u/<str:username>/", public_profile, name="public_profile"),

    # Follow actions
    path("follow/<str:username>/", follow_user, name="follow_user"),
    path("unfollow/<str:username>/", unfollow_user, name="unfollow_user"),
]
