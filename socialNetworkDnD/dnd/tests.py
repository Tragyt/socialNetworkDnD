from django.contrib.auth.models import User
from django.db.models import QuerySet
from django.test import TestCase

from dnd.models import Friendship
from dnd.views import friend_request
from socialNetworkDnD.views import new_requests, list_friends


class FriendRequestTest(TestCase):
    def test_new_request(self):
        """
            new_request should return first 0 then 1 then 0
        """

        friend = User.objects.create(username="friend")
        test = User.objects.create(username="test")
        self.assertEqual(new_requests(friend.id), 0)

        friendship = Friendship.objects.create(user1=test, user2=friend, status="not yet")
        self.assertEqual(new_requests(friend.id), 1)

        friendship.status = "Friends"
        friendship.save()
        self.assertEqual(new_requests(friend.id), 0)

    def test_list_friends(self):
        """
            list_friends should be empty and contain the user test then
            deleting friend should return empty again
        """

        friend = User.objects.create(username="friend")
        test = User.objects.create(username="test")

        self.assertEqual(list_friends(friend.id).count(), 0)

        friend = Friendship.objects.create(user1=test, user2=friend, status="Friends")
        self.assertEqual(list_friends(friend.id)[0], {'username': 'test'})

        friend.delete()
        self.assertEqual(list_friends(friend.id).count(), 0)
