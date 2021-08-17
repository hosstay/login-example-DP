import json

def print_queryset_as_json(queryset):
    for q in queryset.values():
        print(json.dumps(q, indent=4, sort_keys=True, default=str))