from .shared.common_validations import validate_empty, validate_email, validate_phone, validate_format_name
from contact.models import Contact

messages = {
    'name': 'The name is required',
    'invalid_name': 'invalid name',
    'contact_duplicated': 'The contact is not available',
    'email': 'The email is required',
    'phone': 'The phone is required',
    'message': 'The message is required',
    'invalid_email': 'invalid email',
    'invalid_phone': 'invalid phone',
    'image_not_supported': 'File format not supported'
}

def validate_name(value:str):
    if validate_empty(value):
        return { 'status': True, 'message': messages['name'] }
    elif not validate_format_name(value):
        return { 'status': True, 'message': messages['invalid_name'] }
    return (
        { 'status': True, 'message': messages['contact_duplicated'] }
        if Contact.objects.filter(name=value).exists()
        else { 'status': False, 'message': '' }
    )

def validate_contact_mail(value:str):
    if validate_empty(value):
        return { 'status': True, 'message': messages['email'] }
    if not validate_email(value):
        return { 'status': True, 'message': messages['invalid_email'] }
    return (
        { 'status': True, 'message': messages['contact_duplicated'] }
        if Contact.objects.filter(email=value).exists()
        else { 'status': False, 'message': '' }
    )

def validate_contact_phone(value:str):
    if validate_empty(value):
        return { 'status': True, 'message': messages['phone'] }
    return (
        { 'status': True, 'message': messages['invalid_phone'] }
        if not validate_phone(value)
        else { 'status': False, 'message': '' }
    )

def validate_contact_message(value:str):
    if validate_empty(value):
        return { 'status': True, 'message': messages['phone'] }
    return { 'status': False, 'message': '' }

def validate_fields_create(name:str, email:str, phone:str, message:str):
    name_validation = validate_name(name)
    mail_validation = validate_contact_mail(email)
    phone_validation = validate_contact_phone(phone)
    message_validation = validate_contact_message(message)
    if name_validation['status'] == True:
        return name_validation
    elif mail_validation['status'] == True:
        return mail_validation
    elif phone_validation['status'] == True:
        return name_validation
    return message_validation