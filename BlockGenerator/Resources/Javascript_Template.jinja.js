<script type="text/javascript">
         {% for block in blocklist %}
         	var {{block[0]}} = {{block[1]}};
         {% endfor %}
         {% for block in blocklist %}
         	Blockly.Blocks['{{block[0]}}'] = {
         	init: function() {
         		this.jsonInit({{block[0]}});
         	}
         };
         {% endfor %}
</script>