%- macro class_name(node_type)
%- if node_type == "selector_node":
SelectorNode
%- elif node_type == "sequence_node" :
SequenceNode
%- elif node_type == "parallel_node" :
ParallelNode
%- elif node_type == "action_node" :
ActionNode
%- elif node_type == "condition_node" :
ConditionNode
%- elif node_type == "inverter" :
Inverter
%- elif node_type == "root_node" :
RootNode
%- endif
%- endmacro

// Internal Nodes

// Action Node Functions
% for n in nodes if n.node_type == "action_node"
void _action_function_{{n.id}}() {
}
% endfor
// Condition Node Functions
% for n in condition_functions
bool {{n}}();
% endfor
void setup() {
	
	}
}


/**
 * Digraph Code
 *
 include "behavior.dot.jinja"
 *
 */
