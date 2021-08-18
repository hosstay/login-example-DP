import json
from django.utils.html import mark_safe
from markdown import markdown

def print_queryset_as_json(queryset):
    for q in queryset.values():
        print(json.dumps(q, indent=4, sort_keys=True, default=str))

def queryset_to_list_of_dict(queryset):
    list = []

    for q in queryset.values():
        list.append(json.loads(json.dumps(q, indent=4, sort_keys=True, default=str)))

    return list

def get_text_as_markdown(text):
    return mark_safe(markdown(text, safe_mode='escape'))