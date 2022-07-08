from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView

from campaigns.forms import NewPostForm
from campaigns.models import Campaign, Post, Evaluation, Comment
from characters.models import Character
from dnd.models import Profile, Friendship
from socialNetworkDnD.views import CreateBaseView, get_context, list_friends, list_characters, \
    list_campaigns, new_requests, ListBaseView


class CreateCampaign(CreateBaseView):
    model = Campaign
    fields = ("name", "description")

    def form_valid(self, form):
        obj = form.save(commit=False)
        profile = Profile.objects.get(user_id=self.request.user)
        obj.master = profile

        obj.save()
        return HttpResponseRedirect("/dnd/home")


class CampaingView(LoginRequiredMixin, ListView):
    model = Campaign
    template_name = "campaign.html"
    pk = None

    def get_queryset(self):
        self.pk = self.request.resolver_match.kwargs["pk"]
        result = Campaign.objects.get(pk=self.pk)
        return result

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = get_context(self, context)

        context["posts"] = Post.objects.filter(campaign_id=self.pk).order_by("-date")

        return context


class choice_list(LoginRequiredMixin, ListView):
    model = Campaign
    template_name = "choiceCharacter.html"
    pk = None

    def get_queryset(self):
        self.pk = self.request.resolver_match.kwargs["pk"]
        result = Campaign.objects.get(pk=self.pk)
        return result

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = get_context(self, context)

        profile = get_object_or_404(Profile, user=self.request.user.pk)
        campaing = Campaign.objects.get(pk=self.pk)
        friends = Friendship.objects.filter(user1_id=profile.user_id, status="Friends")
        characters = Character.objects.filter(user_id__in=friends.values("user2_id")).exclude(
            id__in=campaing.characters.all())

        context["Friends"] = friends
        context["Characters"] = characters
        context["id_campaign"] = self.pk

        return context


'''
@login_required
def choice_list(request, pk):
    profile = get_object_or_404(Profile, user=request.user.pk)
    campaing = Campaign.objects.get(pk=pk)
    friends = Friendship.objects.filter(user1_id=profile.user_id, status="Friends")
    characters = Character.objects.filter(user_id__in=friends.values("user2_id")).exclude(
        id__in=campaing.characters.all())

    ctx = {"Friends": friends, "Characters": characters, "requests": new_requests(profile.user_id), "id_campaign": pk,
           "friends": list_friends(profile.user_id),
           "characters": list_characters(profile.user_id),
           "campaigns": list_campaigns(profile.user_id)}

    return render(request, "choiceCharacter.html", context=ctx)
'''


@login_required
def add_character(request, id_character, id_campaing):
    character = Character.objects.get(id=id_character)
    campaign = Campaign.objects.get(id=id_campaing)

    campaign.characters.add(character)
    campaign.save()

    return redirect('campaign_view', id_campaing)


@login_required
def rm_character(request, id_character, id_campaing):
    Campaign.objects.get(id=id_campaing).characters.get(id=id_character).delete()
    return redirect('campaign_view', id_campaing)


class NewPost(CreateBaseView):
    model = Post
    form_class = NewPostForm
    template_name = "formsTemplate.html"
    success_url = 'campaign_view'

    def form_valid(self, form):
        obj = form.save(commit=False)

        pk = self.request.resolver_match.kwargs["pk"]
        campaing = Campaign.objects.get(id=pk)
        obj.campaign = campaing
        obj.date = datetime.now()

        obj.save()
        return redirect(self.success_url, pk)


@login_required
def delete_post(request, post, campaign):
    Post.objects.get(id=post).delete()
    return redirect('campaign_view', campaign)


@login_required
def upvote(request, post_id, campaign):
    post = Post.objects.get(id=post_id)
    try:
        vote = Evaluation.objects.get(post_id=post_id, user=request.user)

        if vote.value == 0:
            post.upvote += -1
            vote.value = 2
        elif vote.value == 1:
            post.upvote += 1
            post.downvote += -1
            vote.value = 0
        else:
            post.upvote += 1
            vote.value = 0

        vote.save()

    except:
        Evaluation.objects.create(post_id=post_id, user=request.user, value=0).save()
        post.upvote += 1

    post.save()
    return redirect('campaign_view', campaign)


@login_required
def downvote(request, post_id, campaign):
    post = Post.objects.get(id=post_id)
    try:
        vote = Evaluation.objects.get(post_id=post_id, user=request.user)

        if vote.value == 1:
            post.downvote += -1
            vote.value = 2
        elif vote.value == 0:
            post.downvote += 1
            post.upvote += -1
            vote.value = 1
        else:
            post.downvote += 1
            vote.value = 1

        vote.save()

    except:
        Evaluation.objects.create(post_id=post_id, user=request.user, value=0).save()
        post.upvote += 1

    post.save()
    return redirect('campaign_view', campaign)


class CommentsSection(LoginRequiredMixin, ListView):
    model = Comment
    template_name = "comments.html"
    pk = None

    def get_queryset(self):
        self.pk = self.request.resolver_match.kwargs["pk"]
        comments = Comment.objects.filter(post_id=self.pk).order_by("-time")
        return comments

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = get_context(self, context)

        context["post_id"] = self.pk

        return context


def new_comment(request, id):
    profile = get_object_or_404(Profile, user=request.user.pk)
    post = get_object_or_404(Post, id=id)

    if request.method == 'POST':
        text = request.POST["text"]
        Comment.objects.create(text=text, Profile=profile, post=post, time=datetime.now())

    return redirect("comments", id)
