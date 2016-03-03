function loadXML( xmlstr ) {
    var xml = Blockly.Xml.textToDom(xmlstr); 
    var workspace = Blockly.getMainWorkspace();
    Blockly.Xml.domToWorkspace( workspace, xml);
};


window.onload = function() { 
		var defaultBlocks = "<xml><block type=\"main\" x=\"88\" y=\"72\"></block></xml>";
        loadXML( defaultBlocks );	
};

