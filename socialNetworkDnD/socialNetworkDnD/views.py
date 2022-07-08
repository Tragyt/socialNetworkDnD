from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.views.generic import ListView, UpdateView, CreateView

from campaigns.models import Campaign
from characters.models import Character
from dnd.models import Friendship, Profile


def new_requests(id):
    return Friendship.objects.filter(user2_id=id, status="not yet").count()


def list_friends(id):
    friends = Friendship.objects.filter(user2_id=id, status="Friends").values("user1_id")
    profiles = Profile.objects.filter(user_id__in=friends).values("user_id")
    return User.objects.filter(id__in=profiles).values("username")


def list_characters(id):
    characters = Character.objects.filter(user_id=id)
    return characters


def list_campaigns(id):
    campaigns = Campaign.objects.filter(master__user_id=id) | Campaign.objects.filter(characters__user_id=id)
    return campaigns.distinct()


def get_context(self, context):
    context["requests"] = new_requests(self.request.user.pk)
    context["friends"] = list_friends(self.request.user.pk)
    context["characters"] = list_characters(self.request.user.pk)
    context["campaigns"] = list_campaigns(self.request.user.pk)
    return context


class ListBaseView(LoginRequiredMixin, ListView):
    template_name = "dnd/searchlist.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return get_context(self, context)


class UpdateBaseView(LoginRequiredMixin, UpdateView):
    template_name = "formsTemplate.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return get_context(self, context)


class CreateBaseView(LoginRequiredMixin, CreateView):
    template_name = "formsTemplate.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return get_context(self, context)
