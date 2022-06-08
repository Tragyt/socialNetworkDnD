from django.urls import path, re_path

from .views import home_page, search, SearchUserList, UserProfile, CharacterCreate, ProfileSettings, UserSettings, \
    friend_request, FriendRequests

urlpatterns = [
    re_path(r"^home/[<str:name>]?$|^$", home_page, name="home"),
    path("search/", search, name="search"),
    path('searchresults/<str:search_string>/', SearchUserList.as_view(), name="search_list"),
    path("userprofile/<str:profile>/<mypk>", UserProfile.as_view(), name="user_profile"),
    path("createcharacter/", CharacterCreate.as_view(), name="character_create"),
    path("updateprofile/<pk>/", ProfileSettings.as_view(), name="profile_update"),
    path("updateuser/<pk>/", UserSettings.as_view(), name="user_update"),
    path("friendrequest/<profile>/<action>", friend_request, name="friend_request"),
    path("listfriendrequest/", FriendRequests.as_view(), name="list_requests"),

]
