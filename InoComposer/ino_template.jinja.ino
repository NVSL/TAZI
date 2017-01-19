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

{{header}}


/** ======================================================================= **\
|** ------------------------------ Libraries ------------------------------ **|
\** ======================================================================= **/

#include "{{custom_header_file}}"
#include <Gadgetron.h>
% if bt
#include <BehaviorTree.h>
% endif
% for v in variable_declarations:
% if loop.first

/** Variable Declarations **/

% endif
{{v}}
% endfor
% for f in function_declarations:
% if loop.first



/** ======================================================================= **\
|** --------------------- User Functions Declarations --------------------- **|
\** ======================================================================= **/

% endif
{{f}}
% endfor

% for node in bt.nodes
{{ class_name(node.node_type) }} *{{node.name}}; // id: {{node.id}}
% endfor

% for f in function_definitions:
% if loop.first

/** ======================================================================= **\
|** --------------------- User Functions Definitions ---------------------- **|
\** ======================================================================= **/

% endif
{{f}}
% endfor 


/** ======================================================================= **\
|** --------------------------- Setup Function ---------------------------- **|
|** %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% **|
|** ............................. Description ............................. **|
|** The setup() function runs --ONCE-- when the Arduino boots up. As the    **|
|** name implies, it's useful to add code that 'sets up' your Gadget to     **|
|** run correctly.                                                          **|
|** %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% **|
\** ======================================================================= **/

void setup () {
% for o in gadgetron_objs:
    {{o}}.setup();
% endfor
% for n in bt.nodes
    {{n.name}} = new {{class_name(n.node_type)}} ( 
    %- if n.node_type == "action_node"
[]() -> void {
		% for stmt in n.stmts:
			{{stmt}};
		% endfor
		}
    %- elif n.node_type == "condition_node"
[]() -> bool { return {{n.stmts}}; }
    %- elif n.node_type == "root_node"
			{{n.children}} 
    %- else
 new BehaviorNode*[{{ n.real_children | length }}] {
			{{n.children}}
	  } , {{ n.real_children | length }}
        %- endif 
);

		% if n.holds_state:
		{{ n.name}}.starred = true;
		% endif
% endfor
}

/** ======================================================================= **\
|** ---------------------------- Loop Function ---------------------------- **|
|** %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% **|
|** ............................. Description ............................. **|
|** The loop() function runs continuously after the setup() function        **|
|** finishes and while the Arduino is running. In other words, this         **|
|** function is called repeatly over and over again when it reaches the     **|
|** end of the function. This function is where the majority of your        **|
|** program's logic should go.                                              **|
|** %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% **|
\** ======================================================================= **/

void loop () {
	% if bt:
	root->tick();
	% endif
	% for l in loop_body:
{{l}}
	% endfor
}