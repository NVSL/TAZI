import xml.etree.ElementTree as ET
import jinja2
import blocklyTranslator
import os
from functools import reduce
from operator import add

jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader( os.path.dirname( __file__ ) ))
jinja_env.line_comment_prefix = "#//"
jinja_env.line_statement_prefix = "%"

sequence_node = "sequence_node"
selector_node = "selector_node"
action_node = "action_node"
condition_node = "condition_node"
parallel_node = "parallel_node"
root_node = "root_node"
inverter = "inverter"

labels = {
    sequence_node : "->",
    selector_node : "?",
    parallel_node : "=>",
    root_node : "o",
    inverter : "!"
}

star_nodes  = [ sequence_node, selector_node, parallel_node ]
value_nodes = [ action_node, condition_node ]
decorators = [ inverter ]

class BehaviorNode:
    def __init__( self, name, node_type, children):
        self.name = name if node_type != root_node else "root"
        self.node_type = node_type
        self.children = children
        self.real_children = children
        self.children_array = node_type in star_nodes + [ root_node ] + decorators
        self.function = None
        if self.children_array: self.children = ", ".join( children )
        if node_type in value_nodes: self.children = "" 
        self.label = self.function
        if node_type in labels: self.label = labels[node_type]
    def get_edges( self ):
        if self.children and self.children is not None: 
            return [ self.name + " -> " + child for child in self.real_children]
        return []
class BehaviorParser:
    def __init__(self, program_name):
        self.counts = {}
        self.nodes = []
        self.program_name = program_name

    # Determines a unique name for node
    # Keeps track of how many nodes of each type we have
    def assign_node_name( self, node, node_type):
        name = node_type  
        if name not in self.counts: self.counts[name] = 0
        self.counts[name] += 1
        name += str(self.counts[name])
        return name

    def parse_node( self, node):
        node_type = node.attrib["type"]
        # Determine a unique name for the node
        name = self.assign_node_name( node, node_type )
        children = []

        # If the node is one of these types, then it will have children.
        # Find them and parse them
        if  node_type in [  root_node ] + star_nodes + decorators: 
            children = [ self.parse_node(c[0]) for c in node if len(c) > 0 ] # Indexing at zero takes the block out of its wrapping statement

        # Make an internatl representation to use for code generation
        internal_representation = BehaviorNode( name, node_type, children )

        # If a node is one of the following types, then it should contain some 
        # function like object
        if node_type in value_nodes:
            vs = [ blocklyTranslator.getArgs(c)[1:-1] for c in node if len(c) > 0 ]
            if len(vs):
                internal_representation.function = vs[0]
                print vs[0]
        self.nodes.append( internal_representation)
        if node_type == root_node: self.render()
        return name

    def render( self ):
        edges = reduce( add, [ n.get_edges() for n in self.nodes], [] )
        jinja_vars = { "nodes" : self.nodes,
                       "name"  : self.program_name, 
                       "edges" : edges }
        self.save_to_file( "out_behavior.dot", "behavior.dot.jinja", jinja_vars )
                       
    def save_to_file( self, file_name, template, jinja_vars ):
        template = jinja_env.get_template(template)
        code = template.render(jinja_vars).encode('ascii', 'ignore')
        print code
        #print edges
        code_file = open(file_name, "w")
        code_file.write(code)
        code_file.close()