from django import template
from django.http import HttpResponseRedirect
from member.jwt import verify_token

register = template.Library()

@register.filter(name='decode')
def decode(value):
    payload = verify_token(value)

    if payload is False:
        response = HttpResponseRedirect('/')
        response.delete_cookie(key='refresh_token')
        return response
    
    user_id = payload['user_id']
    return user_id
