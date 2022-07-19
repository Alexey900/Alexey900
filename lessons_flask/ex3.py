from jinja2 import Template
from jinja2 import FileSystemLoader, Environment

package = FileSystemLoader("Templates")  # Load folder
env = Environment(loader=package)     # create environment based on folder

tm = env.get_template('main.html')    # receive template from environment

# show template result by substituting values
print(tm.render(name="Petya", age=23, flag=0))
