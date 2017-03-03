var node_types = ["state", "transition"];
var help_url = "http://robots.gadgetron.build/TAZI/help.html"
var blockColor = 260;

/* 
 * This defines the state block with a string input replace
 */

var stateBlock = function ( name, color )  {
    return {
		init: function() {
			this.appendDummyInput()
				.appendField("state")
				.appendField(new Blockly.FieldTextInput("name"), "\"\"")
				.appendField("start")
				.appendField(new Blockly.FieldCheckbox("TRUE"), "NAME");
			this.appendStatementInput("NAME")
				.setCheck(null)
				.appendField("action");
			this.setNextStatement(true, null);
			this.setColour(330);
			this.setTooltip('');
		}
	}  
}

var transitionBlock = function ( name, color )  {
    return {
		 init: function() {
			this.appendDummyInput()
				.appendField("Transition");
			this.appendValueInput("Condition")
				.setCheck(null)
				.setAlign(Blockly.ALIGN_RIGHT)
				.appendField("If");
			this.appendValueInput("State")
				.setCheck("String")
				.setAlign(Blockly.ALIGN_RIGHT)
				.appendField("State");
			this.setPreviousStatement(true, null);
			this.setNextStatement(true,null);
			this.setColour(330);
			this.setTooltip('');
			this.setHelpUrl('http://www.example.com/');
		 }
	}
}

Blockly.Blocks['state'] = stateBlock(); 
Blockly.Blocks['transition'] = transitionBlock();
























/**
  * Label for the mutator of the state block
  * 
var mutator_label = "Transition"

/** 
  * Mutator block for the if container representing a transition
  * 
var transitionMutatorBlock = function() {
return {
	init: function() {
		  this.setColour(blockColor)
          this.appendDummyInput()
        .appendField("Transition: If");
    this.appendValueInput("NAME")
        .setCheck(null);
    this.appendStatementInput("NAME")
        .setCheck(null)
        .appendField("Then");
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    }
  }
};

/**
  * Defines the beginning block located in the mutator
  *
var transtionStartBlock = function() {
return {
	  init: function() {
        this.setColour(blockColor);
        this.appendDummyInput()
            .appendField("Transition Definitions");	
        this.setNextStatement(true);
        this.setPreviousStatement(false);
        this.contextMenu = false;
    }
  }
};

/**
  *  Represents the node that represents a state. 
  *  It also includes a button where the state can be extended by 
  *    adding more transitions.
  *  This is the block located in the state machine category that the 
  *    user will choose
  *
var stateNode = function ( name, color )  {
    return {
	  /* This defines the initial state block  *
	  init: function() {
		this.appendDummyInput()
          .appendField("State")
          .appendField(new Blockly.FieldTextInput("Name"), "State");
        this.appendStatementInput("Action")
          .setCheck(null)
          .appendField("Action");
		this.setColour(blockColor);
		this.setTooltip('');
		this.setNextStatement(true);
		this.setPreviousStatement(true);
		this.setMutator(new Blockly.Mutator(['extra_transition']));
        this.children_count = 0;
	 },
	/* This allows a mutator to be added and drawn  *
	mutationToDom: function() {
        var container = document.createElement('mutation');

        container.setAttribute('children_count', this.children_count);
        
        return container;
    },
    domToMutation: function(xmlElement) {
        this.children_count = parseInt(xmlElement.getAttribute('children_count'), 10) || 0;
        this.updateShape_();
    },
    decompose: function(workspace) {
        var containerBlock = workspace.newBlock('transition_start');
        containerBlock.initSvg();
        var connection = containerBlock.nextConnection;
        for (var i = 1; i <= this.children_count; i++) {
            var childBlock= workspace.newBlock('extra_transition');
            childBlock.initSvg();
            connection.connect(childBlock.previousConnection);
            connection = childBlock.nextConnection;
        }
        return containerBlock;
        },
    compose: function(containerBlock) {
		var clauseBlock = containerBlock.nextConnection.targetBlock();
		// Count number of inputs.
		this.children_count = 0;
		var valueConnections = [null];
		var statementConnections = [null];
		while (clauseBlock) {
		  switch (clauseBlock.type) {
			case 'extra_transition':
			  this.children_count++;
			  statementConnections.push(clauseBlock.statementConnection_);
			  break;
			default:
			  throw 'Unknown block type.';
		  }
		  clauseBlock = clauseBlock.nextConnection && clauseBlock.nextConnection.targetBlock();
		}
		this.updateShape_();
		// Reconnect any child blocks.
		for (var i = 1; i <= this.children_count; i++) {
		  Blockly.Mutator.reconnect(statementConnections[i], this, mutator_label + i);
		}
	},
	saveConnections: function(containerBlock) {
		var clauseBlock = containerBlock.nextConnection.targetBlock();
		var i = 1;
		while (clauseBlock) {
		  switch (clauseBlock.type) {
			case 'extra_transition':
			  var inputDo = this.getInput(mutator_label + i);
				clauseBlock.statementConnection_ =
				inputDo && inputDo.connection.targetConnection;
			  i++;
			  break;
			default:
			  throw 'Unknown block type.';
		  }
		  clauseBlock = clauseBlock.nextConnection &&
			  clauseBlock.nextConnection.targetBlock();
		}
	},
	updateShape_: function() {
		// Delete everything.
		var i = 1;
		while (this.getInput(mutator_label + i)) {
		  this.removeInput(mutator_label + i);
		  i++;
		}
		// Rebuild block.
		for (var i = 1; i <= this.children_count; i++) {
		  this.appendStatementInput(mutator_label + i)
			  .appendField(mutator_label);
		}
	}
    }
}; 

/* Adding the block to the IDE *
Blockly.Blocks['state'] = stateNode(); 
Blockly.Blocks['transition_start'] = transtionStartBlock() ;
Blockly.Blocks['extra_transition'] = transitionMutatorBlock() ; */