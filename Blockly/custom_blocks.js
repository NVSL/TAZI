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
    this.setHelpUrl('http://www.example.com/');
  }
};
