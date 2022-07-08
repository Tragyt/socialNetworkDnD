from django import template

from campaigns.models import Evaluation

register = template.Library()


@register.filter
def upvote(id_post, id_user):
    try:
        vote = Evaluation.objects.get(post_id=id_post, user_id=id_user)
    except:
        return False
    return vote.value == 0


@register.filter
def downvote(id_post, id_user):
    try:
        vote = Evaluation.objects.get(post_id=id_post, user_id=id_user)
    except:
        return False
    return vote.value == 1
