from django import template

from dnd.models import Friendship

register = template.Library()


@register.filter
def friend(me, he):
    if (Friendship.objects.filter(user1_id=me, user2_id=he, status="Friends") | Friendship.objects.filter(user1_id=he, user2_id=me, status="Friends")).count() > 0:
        return True
    return False
