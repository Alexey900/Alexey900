from jinja2 import Template
from pathlib import Path

tpl = """CREATE table countries(
area FLOAT NOT NULL,
name VARCHAR(50) NOT NULL,
id BIGINT,
population BIGINT NOT NULL
);
{% macro input(a, n, i, p) -%}
    INSERT INTO countries(area, name, id, population) VALUES({{a}}, '{{n}}', {{i}}, {{p}});
{%- endmacro -%}
{{input(17_125, 'Russia', 1, 144)}}
{{input(9_525, 'USA', 2, 329)}}
{{input(0.2, 'UK', 3, 67)}}
{{input(3_287, 'India', 4, 1380)}}
{{input(9_598, 'China', 5, 1402)}}
{{input(0.6, 'Ukraine', 6, 41)}}"""

output = Template(tpl)
sql_f = open("countries.sql", "w+")
sql_f.write(output.render())
sql_f.seek(0)
print(sql_f.read() + '\n', f"Your is path to file {sql_f.name}:\n", f"\t{str(Path.cwd())}/{sql_f.name}")
# #! Python
# """
# This module runs the test code
# """
# from jinja2 import Template

# data = {
#     'LADA': 'priora', 'Ford': 'mustang', 'LADA': 'niva',
#     'Mercedes': 'gtr'
# }  # create a dictionary for testing

# link = """  
# {%- for elem in car_brand -%}
#     {%- if not car_brand[elem] == 'niva'%}
# Car brand -> {{ elem }} : model -> {{car_brand[elem]}}
#     {%- endif %}

# {%- endfor %}
# """  # it's a source for Template

# msg = Template(link)  # create template
# print(msg.render(car_brand=data))  # output
