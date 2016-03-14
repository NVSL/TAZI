BLOCKLY_PATH = ./Blockly/*

build:
	make -C GCGF
	make -C Blockly copy

default:
	git pull
	sudo cp -R $(BLOCKLY_PATH) /var/www/html

test:
	true

clean:
	make -C GCGF clean
	make -C Blockly clean
