from django.template.loader import get_template
from django import template

register = template.Library()

from articles.models import *


def prev_post(current_article_id):
    if current_article_id == 1 :
        return None
    else:
        return {
            'article': Article.objects.get(id = current_article_id-1),
            "current_article_id"  : current_article_id
        }


users_template = get_template('prev_post.html')
register.inclusion_tag(users_template)(prev_post)
