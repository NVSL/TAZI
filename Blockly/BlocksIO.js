function loadXML( xmlstr ) {
    var xml = Blockly.Xml.textToDom(xmlstr); 
    var workspace = Blockly.getMainWorkspace();
    Blockly.Xml.domToWorkspace( workspace, xml);
};


window.onload = function() { 
		var defaultBlocks = "<xml><block type=\"main\" x=\"88\" y=\"72\"></block></xml>";
        loadXML( defaultBlocks );	
};

function readXMLFromFile(evt) {
    //Retrieve the first (and only!) File from the FileList object
    var f = evt.target.files[0];
    if (f) {
        var r = new FileReader();
        r.onload = function (e) {
            var contents = e.target.result;
            console.log(contents);
        }
        loadXML(contents);
        r.readAsText(f);
    } 
    else { alert("Failed to load file"); }
}

document.getElementById('xmlinput').addEventListener('change', readXMLFromFile, false);

