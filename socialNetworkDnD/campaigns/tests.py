from django.contrib.auth.models import User
from django.test import TestCase

# Create your tests here.
from django.urls import reverse

from campaigns.models import Campaign
from characters.models import Character
from dnd.models import Profile, Friendship


class ChoiceCharacterViewTest(TestCase):

    def test_list_no_friends(self):
        """
        no friends = no characters
        """

        user = User.objects.create(username="test")
        user.set_password("test_psw00")
        user.save()
        self.client.login(username="test", password="test_psw00")
        profile = Profile.objects.get(user=user)
        user2 = User.objects.create(username="test2")

        Character.objects.create(name="test_character", user=user2)
        campaign = Campaign.objects.create(name="campaign_test", master=profile)

        response = self.client.get(reverse("choice_character", kwargs={'pk': campaign.id}))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['Characters'], [])

    def test_list_friend_not_in_campaign(self):
        """
        friend -> one character
        """
        user = User.objects.create(username="test")
        user.set_password("test_psw00")
        user.save()
        self.client.login(username="test", password="test_psw00")
        profile = Profile.objects.get(user=user)
        user2 = User.objects.create(username="test2")

        Character.objects.create(name="test_character", user=user2)
        campaign = Campaign.objects.create(name="campaign_test", master=profile)
        Friendship.objects.create(user1=user, user2=user2, status="Friends")

        response = self.client.get(reverse("choice_character", kwargs={'pk': campaign.id}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['Characters'].count(), 1)


    def test_list_friend_in_campaign(self):
        """
        friend but character already in campaign -> empty
        """

        user = User.objects.create(username="test")
        user.set_password("test_psw00")
        user.save()
        self.client.login(username="test", password="test_psw00")
        profile = Profile.objects.get(user=user)
        user2 = User.objects.create(username="test2")

        character = Character.objects.create(name="test_character", user=user2)
        campaign = Campaign.objects.create(name="campaign_test", master=profile)
        Friendship.objects.create(user1=user, user2=user2, status="Friends")

        campaign.characters.add(character)
        campaign.save()

        response = self.client.get(reverse("choice_character", kwargs={'pk': campaign.id}))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['Characters'], [])