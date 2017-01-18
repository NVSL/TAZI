{{header}}


/** ======================================================================= **\
|** ------------------------------ Libraries ------------------------------ **|
\** ======================================================================= **/

#include "{{custom_header_file}}"
#include <Gadgetron.h>
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
\** ======================================================================= **//

% endif
{{f}}
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
% for l in loop_body:
{{l}}
% endfor
}