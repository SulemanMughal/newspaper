from django.template.loader import get_template
from django import template

register = template.Library()

from articles.models import *


def next_post(current_article_id):
    try:
        article = Article.objects.get(id = current_article_id+1)
        return {
            'article': article,
            "current_article_id"  : current_article_id
        }
    except:
        return None

users_template = get_template('next_post.html')
register.inclusion_tag(users_template)(next_post)
