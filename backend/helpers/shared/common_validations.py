import re

suportted_images = [
    'image/apng',
    'image/avif',
    'image/gif',
    'image/jpeg',
    'image/png',
    'image/svg',
    'image/bmp',
    'image/webp'
]

def validate_empty(value):
    return value == None or not value

def validate_email(value:str):
    return re.match(r'^[\w\.-]+@[\w\.-]+\.\w{2,}$', value) is not None

def validate_phone(value:str):
    return re.match(r'^\+?[\d\s\-\(\)]{7,20}$', value) is not None

def validate_format_name(value:str):
    return re.match(r'^[A-Za-zÁÉÍÓÚáéíóúÑñÜü\s\-]{2,50}$', value) is not None