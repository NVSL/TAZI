/** ############################# Robot Name ############################## **\
|** ~~~~~~~~~~~~~~~~~~~~~~~~~~~*****************~~~~~~~~~~~~~~~~~~~~~~~~~~~ **|
|** ~~~~~~~~~~~~~~~~~~~~~~~~~~/                 \~~~~~~~~~~~~~~~~~~~~~~~~~~ **|
|** ========================={ TAZI_Stress_Board }========================= **|
|** ~~~~~~~~~~~~~~~~~~~~~~~~~~\                 /~~~~~~~~~~~~~~~~~~~~~~~~~~ **|
|** ~~~~~~~~~~~~~~~~~~~~~~~~~~~*****************~~~~~~~~~~~~~~~~~~~~~~~~~~~ **|
\** ##########################[[[[[[[[^_^]]]]]]]]########################## **/


/** ======================================================================= **\
|** ------------------------------ Libraries ------------------------------ **|
\** ======================================================================= **/

#include "TAZI_Stress_Board.h"
#include <Gadgetron.h>
#include <BehaviorTree.h>
ActionNode *action_node1; // id: 1
ConditionNode *condition_node1; // id: 1
ActionNode *action_node2; // id: 2
SelectorNode *selector_node2; // id: 2
SelectorNode *selector_node1; // id: 1
RootNode *root; // id: 1
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
    button.setup();
    drive.setup();
    action_node1 = new ActionNode ([]() -> void {
			drive.forward(255);
			delay( (int) ( 1000 * (1)));
			drive.backward();
		});

    condition_node1 = new ConditionNode ([]() -> bool { return !(button.isPressed()); });

    action_node2 = new ActionNode ([]() -> void {
			drive.backward();
			delay( (int) ( 1000 * (1)));
		});

    selector_node2 = new SelectorNode ( new BehaviorNode*[1] {
			action_node2
	  } , 1);

    selector_node1 = new SelectorNode ( new BehaviorNode*[3] {
			action_node1, condition_node1, selector_node2
	  } , 3);

    root = new RootNode (			selector_node1);

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
	root->tick();
;
}
