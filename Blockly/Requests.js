function testPost() {
    var xml = getXML();
    $.post("/compile",  { "xml" : xml } , function(data) {
        console.log(data);
        alert(data);
    });
}
