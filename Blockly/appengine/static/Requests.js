function testPost() {
    var xml = getXML();
    $.post("/compile",  xml , function(data) {});
}
