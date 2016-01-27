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
        .appendField("Pause for ");
    this.appendDummyInput()
        .appendField("milliseconds");
    this.setPreviousStatement(true);
    this.setNextStatement(true);
    this.setColour(210);
    this.setTooltip('');
    this.setHelpUrl('http://www.gadgetron.build/');
  }
};

Blockly.Blocks['millis'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Time in milliseconds");
    this.setOutput(true);
    this.setColour(210);
    this.setTooltip('The length of time since the program has started in milliseconds');
    this.setHelpUrl('http://www.gadgetron.build/');
  }
};
