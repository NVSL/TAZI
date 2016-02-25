BLOCKLY_PATH = ./Blockly/*
default:
	git pull
	sudo cp -R $(BLOCKLY_PATH) /var/www/html

test:
	true
