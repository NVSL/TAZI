%- macro class_name(node_type)
%- if node_type == "selector_node": 
SelectorNode  
%- elif node_type == "sequence_node": 
SequenceNode	
%- elif node_type == "parallel_node": 
ParallelNode
%- elif node_type == "action_node": 
ActionNode
%- elif node_type == "condition_node": 
ConditionNode
%- elif node_type == "inverter": 
Inverter
%- elif node_type == "root_node": 
RootNode
%- endif
%- endmacro


%- macro constructor_input(n)
%- endmacro

// Internal Nodes
% for node in nodes
{{class_name(node.node_type)}} * {{node.name}}; // id: {{node.id}}
% endfor
	

// Action Node Functions
% for n in nodes if n.node_type == "action_node"
void _action_function_{{n.id}}() {
	% for stmt in n.stmts:
	{{stmt}};
	% endfor
}
% endfor
// Condition Node Functions
% for n in condition_functions
bool {{n}}();
% endfor
void setup() {
	% for n in nodes
        {{n.name}} = new {{class_name(n.node_type)}} ( 
        %- if n.node_type == "action_node"
 _action_function_{{n.id}}
        %- elif n.node_type == "action_node"
        {{n.function}}
        %- else
 new BehaviorNode*[{{ n.real_children | length }}] {
            {{n.children}} 
        } 
        %- endif 
);

		% if n.holds_state:
		{{ n.name}}.starred = true;
		% endif
	% endfor
	}
}


/**
 * Digraph Code
 *
 include "behavior.dot.jinja"
 *
 */
