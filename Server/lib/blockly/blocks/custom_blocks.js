Blockly.Blocks['variable_declarations'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Put variable definitions here");
    this.setNextStatement(true);
    this.setTooltip('');
    this.setHelpUrl('http://www.gadgetron.build/');
  }
};

Blockly.Blocks['main_loop'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Put your repeating code here");
    this.setNextStatement(true);
    this.setTooltip('');
    this.setHelpUrl('http://www.gadgetron.build/');
  }
};

Blockly.Blocks['delay'] = {
  init: function() {
    this.appendValueInput("NAME")
		.setCheck("Number")
        .appendField("Pause for ");
    this.appendDummyInput()
        .appendField("milliseconds");
    this.setPreviousStatement(true);
    this.setNextStatement(true);
    this.setColour(17);
    this.setTooltip('');
    this.setHelpUrl('http://www.gadgetron.build/');
  }
};

Blockly.Blocks['delaySeconds'] = {
  init: function() {
    this.appendValueInput("NAME")
		.setCheck("Number")
        .appendField("Pause for ");
    this.appendDummyInput()
        .appendField("seconds");
    this.setPreviousStatement(true);
    this.setNextStatement(true);
    this.setColour(17);
    this.setTooltip('');
    this.setHelpUrl('http://www.gadgetron.build/');
  }
};

Blockly.Blocks['main'] = {
  init: function() {
    this.appendStatementInput("variable_declarations")
        .appendField("Setup");
    this.appendStatementInput("main_loop")
        .appendField("Loop forever and ever");
    this.setColour(105);
    this.setTooltip('Make sure you put all your blocks in here!');
    this.setHelpUrl('http://www.gadgetron.build/');
    //this.setDeletable(false)
  }
};



Blockly.Blocks['millis'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Time in milliseconds");
    this.setOutput(true, "Number");
    this.setColour(17);
    this.setTooltip('The length of time since the program has started in milliseconds');
    this.setHelpUrl('http://www.gadgetron.build/');
  }
};


Blockly.Blocks['c_main'] = {
  init: function() {
    this.appendStatementInput("main_body")
        .appendField("C++ Main Function");
    this.setColour(330);
    this.setTooltip('');
    this.setHelpUrl('http://www.example.com/');
  }
};

