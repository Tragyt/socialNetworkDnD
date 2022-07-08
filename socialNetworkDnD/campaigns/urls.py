from django.urls import path

from campaigns.views import CreateCampaign, CampaingView, choice_list, add_character, rm_character, NewPost, \
    delete_post, upvote, downvote, CommentsSection, new_comment

urlpatterns = [
    path("create/", CreateCampaign.as_view(), name="create_campaign"),
    path("campaign/<pk>/", CampaingView.as_view(), name="campaign_view"),
    path("choice/<pk>/", choice_list.as_view(), name="choice_character"),
    path("addcharacter/<id_character><id_campaing>/", add_character, name="add_character"),
    path("removecharacter/<id_character><id_campaing>", rm_character, name="remove_character"),
    path("newpost/<pk>", NewPost.as_view(), name="new_post"),
    path("deletepost/<post><campaign>", delete_post, name="delete_post"),
    path("upvote/<post_id><campaign>", upvote, name="upvote"),
    path("downvote/<post_id><campaign>", downvote, name="downvote"),
    path("comments/<pk>", CommentsSection.as_view(), name="comments"),
    path("newcomment/<id>", new_comment, name="new_comment"),
]
