from jinja2 import Environment, FileSystemLoader, ModuleLoader
from markupsafe import escape

persons = [
    {"name": "Alexei", "old": 18, "weight": 75.8},
    {"name": "Nikolai", "old": 28, "weight": 82.3},
    {"name": "Ivan", "old": 33, "weight": 94.0}
]

# file_loader = FileSystemLoader("Templates")
file_loader = ModuleLoader(r"Templates\main.py")
env = Environment(loader=file_loader)
print(*dir(file_loader), sep="\n")

tm = env.get_template(tm1)
msg = tm.render(users=persons)

print(msg)
