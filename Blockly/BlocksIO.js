window.requestFileSystem  = window.requestFileSystem || window.webkitRequestFileSystem;

//window.requestFileSystem(type, size, successCallback, opt_errorCallback)



function errorHandler(e) {
  var msg = '';

  switch (e.code) {
    case FileError.QUOTA_EXCEEDED_ERR:
      msg = 'QUOTA_EXCEEDED_ERR';
      break;
    case FileError.NOT_FOUND_ERR:
      msg = 'NOT_FOUND_ERR';
      break;
    case FileError.SECURITY_ERR:
      msg = 'SECURITY_ERR';
      break;
    case FileError.INVALID_MODIFICATION_ERR:
      msg = 'INVALID_MODIFICATION_ERR';
      break;
    case FileError.INVALID_STATE_ERR:
      msg = 'INVALID_STATE_ERR';
      break;
    default:
      msg = 'Unknown Error';
      break;
  };

  console.log('Error: ' + msg);
}


function loadXML( xmlstr ) {
    var xml = Blockly.Xml.textToDom(xmlstr); 
    var workspace = Blockly.getMainWorkspace();
    Blockly.Xml.domToWorkspace( workspace, xml);
};



function readXMLFromFile(evt) {
    //Retrieve the first (and only!) File from the FileList object
    var f = evt.target.files[0];
    if (f) {
        var r = new FileReader();
        r.onload = function (e) {
            var contents = e.target.result;
            var workspace = Blockly.getMainWorkspace();
            console.log(contents);
	    workspace.clear()
            loadXML(contents);
        }
        r.readAsText(f);
    } 
    else { alert("Failed to load file"); }
}

function writeXMLToFile(fs) {
    fs.root.getFile('blockly.xml', {create: true}, function(fileEntry) {
    console.log("hi");

    // Create a FileWriter object for our FileEntry (log.txt).
    fileEntry.createWriter(function(fileWriter) {

      fileWriter.onwriteend = function(e) {
        console.log('Write completed.');
      };

      fileWriter.onerror = function(e) {
        console.log('Write failed: ' + e.toString());
      };

      // Create a new Blob and write it to log.txt.
      var blob = new Blob(['Lorem Ipsum'], {type: 'text/plain'});

      fileWriter.write(blob);

    }, errorHandler);

  }, errorHandler);

}


window.requestFileSystem(window.TEMPORARY, 1024*1024, writeXMLToFile, errorHandler);

document.getElementById('xmlinput').addEventListener('change', readXMLFromFile, false);
document.getElementById('savexml').addEventListener('change', writeXMLToFile, false);
function getXML() {
    var xml = Blockly.Xml.workspaceToDom(Blockly.getMainWorkspace());
    var xmlstr =  Blockly.Xml.domToText(xml);
    return xmlstr.replace("xmlns=\"http://www.w3.org/1999/xhtml\"", "");
}
