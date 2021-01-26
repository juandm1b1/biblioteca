import os
import time
import django,random as rd

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "biblioteca.settings")

django.setup()

from apps.libro.models import Autor

vocals = ['A','a','E','e','I','i','O','o','U','u']

consonants = ['B','b','C','c','D','d','F','f','G','g','H','h','J','j','K','k','L','l',
            'M','m','N','n','P','p','Q','q','R','r','S','s','T','t','V','v','W','w','X','x','Y','y','Z','z']


def generate_string(length):
    if length <= 0:
        return False

    random_string = ''

    for i in range(length):
        decision = rd.choice(('vocals', 'consonants'))

        if random_string[-1:].lower() in vocals:
            decision = 'consonants'
        if random_string[-1:].lower() in consonants:
            decision = 'vocals'

        if decision == 'vocals':
            character = rd.choice(vocals)
        else:
            character = rd.choice(consonants)

        random_string += character

    return random_string


def generate_number():
    return int(rd.random() * 10 + 1)


def generate_autor(count):
    for j in range(count):
        random_name = generate_string(generate_number())
        random_lastname = generate_string(generate_number())
        random_country = generate_string(generate_number())
        random_description = generate_string(generate_number())

        Autor.objects.create(
            nombre = random_name,
            apellido = random_lastname,
            pais = random_country,
            descripcion = random_description
        )




    
if __name__ == "__main__":
    print("Inicio de creación de población")
    print("Por favor espere...")
    start = time.strftime("%c")
    print(f'Fecha y hora de inicio: {start}')
    generate_autor(10)
    end = time.strftime("%c")
    print(f'Fecha y hora de finalización: {end}')
    print(Autor.objects.count())