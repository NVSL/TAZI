// Internal Nodes
ActionNode * action_node1; // id: 1
Inverter * inverter1; // id: 1
ActionNode * action_node2; // id: 2
SelectorNode * selector_node2; // id: 2
SelectorNode * selector_node1; // id: 1
RootNode * root; // id: 1
// Action Node Functions
/**
None();
*/
// Condition Node Functions
void setup() {
        action_node1 = new ActionNode ( _action_function_1);

        inverter1 = new Inverter ( new BehaviorNode*[1] {
            action_node1 
        });

        action_node2 = new ActionNode ( _action_function_2);

        selector_node2 = new SelectorNode ( new BehaviorNode*[1] {
            action_node2 
        });

        selector_node1 = new SelectorNode ( new BehaviorNode*[2] {
            inverter1, selector_node2 
        });

        root = new RootNode ( new BehaviorNode*[1] {
            selector_node1 
        });

	}
}


/**
 * Digraph Code
 *
 include "behavior.dot.jinja"
 *
 */