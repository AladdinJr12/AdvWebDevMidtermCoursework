from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    # """----Accessing dictionary keys dynamically---"""
    #--This is because inside views.py the '_' symbol was removed by verbose_name--#
    key = key.replace(" ", "_")
    return dictionary.get(key)

