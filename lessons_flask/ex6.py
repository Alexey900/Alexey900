import sys
from jinja2 import FileSystemLoader, Environment


file_system = FileSystemLoader("parts")     # Загрузить каталог с шаблонами
# Отсюда будут братсья данные для шаблонов
env = Environment(loader=file_system)       # Создать окружение

template = env.get_template("main.html")    # get template from environment
message = template.render()                 # message

print(message)


def start_page(page_content):
    """This function creates an html file and runs it."""

    # This module contains the corresponding methods for opening a file
    import os
    with open("page.html", "w+", encoding="utf-8") as file:  # create page.html
        file.write(page_content)           # add contenct
    print(file.closed)
    os.system("page.html")                 # to open
    os.system("del page.html")             # deleate


if sys.argv[-1] == "True":
    start_page(message)                     # run
