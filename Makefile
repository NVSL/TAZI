BLOCKLY_PATH = ./Blockly/*

build:
	true

default:
	git pull
	sudo cp -R $(BLOCKLY_PATH) /var/www/html

test:
	true

clean:
	true