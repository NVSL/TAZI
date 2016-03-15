import jinja2
import os

JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))
def render_workspace( xmlpath, jinja_file):
    xml_str = open(xmlpath).read().replace("\n", "").replace('"', '\\"')
    jinja_vars = {"defaultBlocks" : xml_str }
    return render_template( jinja_file, jinja_vars)

def render_template( jinja_file, jinja_vars ):
    template = JINJA_ENVIRONMENT.get_template(jinja_file)
    return template.render(jinja_vars).encode('ascii', 'ignore')
