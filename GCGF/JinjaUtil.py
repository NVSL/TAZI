import jinja2
import os
slashes = "\\" if os.name == "nt" else "/"
JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(slashes.join(["..",os.path.dirname(__file__)])))
def render_workspace( xmlpath, jinja_file, additional_args={}, jinja_env=JINJA_ENVIRONMENT):
    xml_str = open(xmlpath).read().replace("\n", "").replace('"', '\\"')
    jinja_vars = {"defaultBlocks" : xml_str }
    return render_template( jinja_file, jinja_vars, additional_args)

def render_template( jinja_file, jinja_vars, additional_args={} ):
    template = JINJA_ENVIRONMENT.get_template(jinja_file)
    for k in additional_args: jinja_vars[k] = additional_args[k]
    return template.render(jinja_vars).encode('ascii', 'ignore')
