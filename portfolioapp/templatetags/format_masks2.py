from django import template
from django.utils.text import Truncator

register = template.Library()


def asset_name_omit(asset_name):
    return Truncator(asset_name).chars(25)


register.filter('asset_name_omit', asset_name_omit)