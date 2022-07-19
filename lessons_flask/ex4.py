from jinja2 import FileSystemLoader, Environment
import os

file_loader = FileSystemLoader("parts")
env = Environment(loader=file_loader)

a = [
    {'name': "dev/nul/chakravirivatel"},
    {'name': "moon1337"},
    {'name': "great deanoners retribution"}
]

tm = env.get_template("content.htm")
msg = tm.render(name="about Jinja2", users=a)

with open("index.html", "w") as file:
    file.write(msg)

os.system("index.html")
os.system("DEL index.html")
