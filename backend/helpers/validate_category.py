from .shared.common_validations import validate_empty, validate_format_name
from categories.models import Category

messages = {
    'name': 'The name is required',
    'name_duplicated': 'The category is not available',
    'invalid_name': 'invalid name'
}

def validate_fields_create(name):
    if validate_empty(name):
        return { 'status': True, 'message': messages['name'] }
    elif not validate_format_name(name):
        return { 'status': True, 'message': messages['invalid_name'] }
    return (
        { 'status': True, 'message': messages['name_duplicated'] }
        if Category.objects.filter(name=name).exists()
        else { 'status': False, 'message': '' }
    )