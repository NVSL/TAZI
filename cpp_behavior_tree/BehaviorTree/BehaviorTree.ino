/*
 Name:		BehaviorTree.ino
 Created:	1/1/2017 12:04:56 PM
 Author:	Michael Gonzalez
 Editor:	http://www.visualmicro.com
*/

#include "RootNode.h"
#include "SelectorNode.h"
#include "InternalNode.h"
#include "BehaviorNode.h"
#include "ConditionNode.h"
#include <Gadgetron_Libraries/utility/MomentaryButton.h>

NodeList selectionList; 
SelectorNode * firstSelector; 
RootNode * root;
MomentaryButton button(9);
// the setup function runs once when you press reset or power the board
const int status_led = 13;
void setup() {
	selectionList = 
	MAKE_NODE_LIST(3) //new BehaviorNode*[3]
	{ 
		new ConditionNode<BehaviorNode>(foo),
		new ConditionNode<MomentaryButton>(&MomentaryButton::isPressed, button),
		new ConditionNode<BehaviorNode>(bar) 
	};
	firstSelector = new SelectorNode(selectionList, 3);
	root = new RootNode(firstSelector);
	Serial.begin(9600);
	pinMode(status_led,  OUTPUT);
}

// the loop function runs over and over again until power down or reset
void loop() {
	root->tick();
}

bool foo() {
	Serial.println("Inside foo!");
	digitalWrite(status_led, LOW);
	return false;
}
bool bar() {
	digitalWrite(status_led, HIGH);
	Serial.println("Inside bar!");
	return true;
}