from django.db import models


class Plant:  # Note that parens are optional if not inheriting from another class
    def __init__(self, name, breed, description, age):
        self.name = name
        self.breed = breed
        self.description = description
        self.age = age


plants = [
    Plant('Lolo', 'tabby', 'foul little demon', 3),
    Plant('Sachi', 'tortoise shell', 'diluted tortoise shell', 0),
    Plant('Raven', 'black tripod', '3 legged cat', 4)
]
