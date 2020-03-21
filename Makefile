# That is just some shit to develop with VSCode instead of Arduino IDE
# PS: If someone watch this and know how to launch serial monitor 
# from command line i'd love to hear that

install:
	arduino-cli lib install RF24

arduino:
	arduino-cli compile --fqbn arduino:avr:uno receiever
	arduino-cli upload -p /dev/ttyACM0 --fqbn arduino:avr:uno receiever
	rm -f receiever/*.elf receiever/*.hex

raspberry:
	scp sender/sender.py root@192.168.5.61:~/com_NRF24L01/sender.py
