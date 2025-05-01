import os

def remove_image(image:str):
    if image != '':
        path = get_image(image)
        os.remove(path) if os.path.exists(path) else print('image not found')

def get_image(image: str):
    return f'files/recipe/{image}'

def format_image(image: str):
    return f'{os.getenv('BASE_URL')}{get_image(image)}'
