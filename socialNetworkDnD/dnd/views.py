from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.urls import reverse_lazy

from .forms import UpdateUserForm, UpdateProfileForm
from .models import Profile, Character, Friendship
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, UpdateView
from django.contrib import messages

app_name = 'dnd'


def new_requests(id):
    return Friendship.objects.filter(user2_id=id, status="not yet").count()


def list_friends(id):
    friends = Friendship.objects.filter(user2_id=id, status="Friends").values("user1_id")
    profiles = Profile.objects.filter(user_id__in=friends).values("user_id")
    return User.objects.filter(id__in=profiles).values("username")


@login_required
def home_page(request):
    profile = get_object_or_404(Profile, user=request.user.pk)
    if request.method == 'POST':
        profile_name = request.POST["name"]
        return redirect("user_profile", profile_name, profile.user_id)

    ctx = {"utente": profile.user.username, "email": profile.user.email, "description": profile.bio, "pk": profile.pk,
           "img": profile.img, "last_name": profile.user.last_name, "first_name": profile.user.first_name,
           "user_pk": profile.user.pk, "requests": new_requests(profile.user_id),
           "friends": list_friends(profile.user_id)}
    return render(request, "profile.html", context=ctx)


@login_required
def search(request):
    if request.method == 'POST':
        searched = request.POST["Search"]
        if searched == "":
            return redirect("search_list", " ")
        return redirect("search_list", searched)

    return redirect("search_list", " ")


class SearchUserList(LoginRequiredMixin, ListView):
    model = Profile, User
    template_name = "dnd/searchlist.html"

    def get_queryset(self):
        search_string = self.request.resolver_match.kwargs["search_string"]

        results = Profile.objects.select_related("user").filter(user__username__icontains=search_string)
        return results

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["requests"] = new_requests(self.request.user.pk)
        context["friends"] = list_friends(self.request.user.pk)
        return context


class UserProfile(LoginRequiredMixin, ListView):
    model = Profile
    template_name = "profile.html"
    pk = 0

    def get_queryset(self):
        username = self.request.resolver_match.kwargs["profile"]
        result = Profile.objects.get(user__username=username)
        self.pk = result.user_id
        return result

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mypk = self.request.resolver_match.kwargs["mypk"]
        is_friend = Friendship.objects.filter(user1_id=mypk, user2_id=self.pk)

        if is_friend.count() == 0:
            context["friendship"] = "None"
        else:
            context["friendship"] = is_friend[0].status

        context["requests"] = new_requests(self.request.user.pk)
        context["friends"] = list_friends(self.request.user.pk)
        return context


class CharacterCreate(LoginRequiredMixin, CreateView):
    model = Character
    template_name = "formsTemplate.html"
    fields = "__all__"
    success_url = "home"

    # form = CharacterForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["requests"] = new_requests(self.request.user.pk)
        context["friends"] = list_friends(self.request.user.pk)
        return context


class ProfileSettings(LoginRequiredMixin, UpdateView):
    model = Profile
    template_name = "formsTemplate.html"
    form_class = UpdateProfileForm
    success_url = reverse_lazy("home")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["requests"] = new_requests(self.request.user.pk)
        context["friends"] = list_friends(self.request.user.pk)
        return context


class UserSettings(LoginRequiredMixin, UpdateView):
    model = User
    template_name = "formsTemplate.html"
    form_class = UpdateUserForm
    success_url = reverse_lazy("home")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["requests"] = new_requests(self.request.user.pk)
        context["friends"] = list_friends(self.request.user.pk)
        return context


@login_required
def friend_request(request, **kwargs):
    user1 = get_object_or_404(Profile, user_id=request.user.pk)
    user2 = request.resolver_match.kwargs["profile"]
    action = request.resolver_match.kwargs["action"]

    if action == "request":
        try:
            reverse = Friendship.objects.get(user1_id=user2, user2_id=user1.user_id, status="not yet")
            reverse.status = "Friends"
            reverse.save()
            Friendship.objects.create(user1_id=user1.user_id, user2_id=user2, status="Friends")
            messages.info(request, 'Friendship accepted')
        except:
            Friendship.objects.create(user1_id=user1.user_id, user2_id=user2, status="not yet")
            messages.info(request, 'Friendship request sent')

    else:
        try:
            Friendship.objects.get(user1_id=user1.user_id, user2_id=user2).delete()
            Friendship.objects.get(user1_id=user2, user2_id=user1.user_id).delete()
            messages.info(request, 'Friendship cancelled')
        except:
            messages.info(request, 'Friendship cancelled')

    username = Profile.objects.get(user_id=user2).user.username
    return redirect("user_profile", username, user1.user.id)


class FriendRequests(LoginRequiredMixin, ListView):
    model = Friendship, Profile
    template_name = "searchlist.html"

    def get_queryset(self):
        requests = Friendship.objects.filter(user2_id=self.request.user.pk, status="not yet").values_list("user1")
        results = Profile.objects.filter(user_id__in=requests)
        return results

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["requests"] = new_requests(self.request.user.pk)
        context["friends"] = list_friends(self.request.user.pk)
        return context
