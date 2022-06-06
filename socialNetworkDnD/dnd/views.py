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


@login_required
def home_page(request):
    profile = get_object_or_404(Profile, user=request.user.pk)
    if request.method == 'POST':
        profile_name = request.POST["name"]
        return redirect("user_profile", profile_name, profile.user_id)

    ctx = {"utente": profile.user.username, "email": profile.user.email, "description": profile.bio, "pk": profile.pk,
           "img": profile.img, "last_name": profile.user.last_name, "first_name": profile.user.first_name,
           "user_pk": profile.user.pk}
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
        if not results.exists():
            return "0"
        return results


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

        return context


class CharacterCreate(LoginRequiredMixin, CreateView):
    model = Character
    template_name = "formsTemplate.html"
    fields = "__all__"
    success_url = "home"
    # form = CharacterForm


class ProfileSettings(LoginRequiredMixin, UpdateView):
    model = Profile
    template_name = "formsTemplate.html"
    form_class = UpdateProfileForm
    success_url = reverse_lazy("home")


class UserSettings(LoginRequiredMixin, UpdateView):
    model = User
    template_name = "formsTemplate.html"
    form_class = UpdateUserForm
    success_url = reverse_lazy("home")


@login_required
def friend_request(request, **kwargs):
    user1 = get_object_or_404(Profile, user=request.user.pk)
    user2 = request.resolver_match.kwargs["profile"]
    action = request.resolver_match.kwargs["action"]

    if action == "request":
        r = Friendship.objects.create(user1_id=user1.user_id, user2_id=user2, status="not yet")
        messages.info(request, 'Friendship request sent')
    else:
        Friendship.objects.get(user1_id=user1.user_id, user2_id=user2).delete()
        messages.info(request, 'Friendship cancelled')

    username = Profile.objects.get(user_id=user2).user.username
    return redirect("user_profile", username, user1.user.id)
