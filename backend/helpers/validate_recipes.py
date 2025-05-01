import os
from datetime import datetime
from recipe.models import Recipe
from categories.models import Category
from django.core.files.storage import FileSystemStorage
from .shared.common_validations import validate_empty, suportted_images
from interfaces.shared.responses import Response
from interfaces.file_interface import FileResponse
from .validate_image import remove_image

messages = {
    'name': 'The name is required',
    'name_duplicated': 'The recipe is not available',
    'category': 'The category id to relate the new recipe is mandatory',
    'category_exists': 'The category is not available',
    'image_not_supported': 'File format not supported'
}

def validate_name(value:str):
    if validate_empty(value):
        return { 'status': True, 'message': messages['name'] }
    return (
        { 'status': True, 'message': messages['name_duplicated'] }
        if Recipe.objects.filter(name=value).exists()
        else { 'status': False, 'message': '' }
    )

def validate_category_exists(id):
    return (
        { 'status': False, 'message': '' }
        if Category.objects.filter(pk=id).exists()
        else { 'status': True, 'message': messages['category_exists'] }
    )

def validate_category(value:str):
    if validate_empty(value):
        return { 'status': True, 'message': messages['name'] }
    return validate_category_exists(value)

def validate_fields_create(name, category, **args) -> Response:
    name_validation = validate_name(name[0])
    category_validation = validate_category(category[0])
    if name_validation['status']:
        return { 'status': True, 'message': name_validation['message'] }
    elif category_validation['status']:
        return  { 'status': True, 'message': category_validation['message'] }
    return { 'status': False, 'message': '' }

def save_file(file, old_image = '') -> FileResponse:
    try:
        # validate the image format by its MIME type
        if not validate_empty(file):
            if not any(file.content_type == content for content in suportted_images):
                return { 'status': False, 'path': '', 'message': messages['image_not_supported'] }
            fs = FileSystemStorage()
            date = datetime.now()
            image = f'{datetime.timestamp(date)}{os.path.splitext(str(file))[1]}'
            fs.save(f'recipe/{image}', file)
            remove_image(old_image)
            return { 'status': True, 'path': image, 'message': 'saved' }
        return { 'status': True, 'path': '', 'message': '' }
    except Exception as error:
        return { 'status': False,'path': '', 'message': f'{error}' }

def validate_update_recipe(obj, actual: Recipe):
    return {
        'name': obj['name'] if not validate_empty(obj['name']) else actual.name,
        'time': obj['time'] if not validate_empty(obj['time']) else actual.time,
        'image': obj['image'],
        'description': obj['description'] if not validate_empty(obj['description']) else actual.description,
        'category': obj['category'] if not validate_empty(obj['category']) else actual.category
    }
