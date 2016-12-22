import xml.etree.ElementTree as ET
import jinja2
import blocklyTranslator
import os

jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader( os.path.dirname( __file__ ) ))
jinja_env.line_comment_prefix = "#//"
jinja_env.line_statement_prefix = "%"

sequence_node = "sequence_node"
selector_node = "selector_node"
action_node = "action_node"
condition_node = "condition_node"
parallel_node = "parallel_node"
root_node = "root_node"
star_nodes  = [ sequence_node, selector_node, parallel_node ]
value_nodes = [ action_node, condition_node ]

class BehaviorNode:
    def __init__( self, name, node_type, children):
        self.name = name if node_type != root_node else "root"
        self.node_type = node_type
        self.children = children
        self.children_array = node_type in star_nodes + [ root_node ]
        self.function = None
        if self.children_array: self.children = ", ".join( children )
        if node_type in value_nodes: self.children = "" 
class BehaviorParser:
    def __init__(self, program_name):
        self.count_action = 0
        self.count_sequence = 0
        self.count_selector = 0
        self.count_condition = 0
        self.nodes = []
        self.program_name = program_name

    # Determines a unique name for node
    # Keeps track of how many nodes of each type we have
    def assign_node_name( self, node, node_type):
        name = node_type  
        # Sequence Nodes
        if node_type == sequence_node: 
            self.count_sequence += 1
            name += str(self.count_sequence)
        # Selector Nodes
        if node_type == selector_node: 
            self.count_selector += 1
            name += str(self.count_selector)
        # Action Nodes
        if node_type == action_node: 
            self.count_action += 1
            name += str(self.count_action)
        # Condition Nodes
        if node_type == condition_node: 
            self.count_condition += 1
            name += str(self.count_condition)
        # Paralell Nodes
        if node_type == parallel_node: 
            self.count_condition += 1
            name += str(self.count_condition)
        return name

    def parse_node( self, node):
        node_type = node.attrib["type"]
        # Determine a unique name for the node
        name = self.assign_node_name( node, node_type )
        children = []

        # If the node is one of these types, then it will have children.
        # Find them and parse them
        if  node_type in [  root_node ] + star_nodes : 
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
        jinja_vars = { "nodes" : self.nodes,
                       "name"  : self.program_name }
        template = jinja_env.get_template("behavior.jinja")
        code = template.render(jinja_vars).encode('ascii', 'ignore')
        print code
        code_file = open("foo.cs", "w")
        code_file.write(code)
        code_file.close()