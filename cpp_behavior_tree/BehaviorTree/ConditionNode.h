// ConditionNode.h

#ifndef _CONDITIONNODE_h
#define _CONDITIONNODE_h
#include "BehaviorNode.h"


/**
 Heavier templating use may generalize Action/Condition Nodes
 Member Function Pointer Info/Typedef info: 
 https://isocpp.org/wiki/faq/pointers-to-members
 */

#define CALL_MEMBER_FN(object,ptrToMember)  ((*object).*(ptrToMember))
#define DEFINE_MEMBER_FN typedef bool (T::*MemberFunction)();  // Please do this!

#if defined(ARDUINO) && ARDUINO >= 100
	#include "arduino.h"
#else
	#include "WProgram.h"
#endif
template <typename T>
class ConditionNode : public BehaviorNode {
DEFINE_MEMBER_FN
public:
	ConditionNode(bool(*func)());
	ConditionNode(MemberFunction func, T & object);
	uint8_t tick(); 
private:
	bool(*c_like_func)();
	MemberFunction member_function;
	T * object;
};
template<typename T>
ConditionNode<T>::ConditionNode(MemberFunction func, T & object)
{
	this->object = &object;
	this->member_function = func;
}
template<class T>
uint8_t ConditionNode<T>::tick()
{
	if (c_like_func) return c_like_func();
	return CALL_MEMBER_FN(object, member_function)();
}
template<class T>
ConditionNode<T>::ConditionNode(bool(*func)())
{
	this->c_like_func = func;
};


#endif
