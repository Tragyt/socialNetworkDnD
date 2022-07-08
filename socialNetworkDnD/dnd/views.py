from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.urls import reverse_lazy

from characters.models import Character
from socialNetworkDnD.views import new_requests, list_friends, list_characters, ListBaseView, UpdateBaseView, \
    list_campaigns, get_context
from .forms import UpdateUserForm, UpdateProfileForm
from .models import Profile, Friendship
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
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
           "user_pk": profile.user.pk, "requests": new_requests(profile.user_id), "experience": profile.experience,
           "friends": list_friends(profile.user_id), "characters": list_characters(profile.user_id),
           "campaigns": list_campaigns(profile.user_id)}
    return render(request, "profile.html", context=ctx)


@login_required
def search(request):
    if request.method == 'POST':
        searched = request.POST["Search"]
        if searched == "":
            return redirect("search_list", " ")
        return redirect("search_list", searched)

    return redirect("search_list", " ")


class SearchUserList(ListBaseView):
    model = Profile, User

    def get_queryset(self):
        search_string = self.request.resolver_match.kwargs["search_string"]
        this_user = self.request.user.username

        results = (Profile.objects.select_related("user").filter(
            user__username__icontains=search_string)
                   | Profile.objects.select_related("user").filter(user__email__icontains=search_string)
                   | Profile.objects.select_related("user").filter(user__last_name__icontains=search_string)
                   | Profile.objects.select_related("user").filter(user__first_name__icontains=search_string)) \
            .exclude(user__username=this_user)
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

        context = get_context(self, context)

        context["his_friends"] = Friendship.objects.filter(user2_id=self.pk, status="Friends")
        context["his_characters"] = Character.objects.filter(user_id=self.pk)

        return context


class ProfileSettings(UpdateBaseView):
    model = Profile
    form_class = UpdateProfileForm
    success_url = reverse_lazy("home")


class UserSettings(UpdateBaseView):
    model = User
    form_class = UpdateUserForm
    success_url = reverse_lazy("home")


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


class FriendRequests(ListBaseView):
    model = Friendship, Profile

    def get_queryset(self):
        requests = Friendship.objects.filter(user2_id=self.request.user.pk, status="not yet").values_list("user1")
        results = Profile.objects.filter(user_id__in=requests)
        return results
