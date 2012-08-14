from django.template import Library
from ..models import Metadata


register = Library()


@register.assignment_tag
def get_metadata_for(obj):
    try:
        return Metadata.objects.get_for_content_object(obj)
    except Metadata.DoesNotExist:
        return None
