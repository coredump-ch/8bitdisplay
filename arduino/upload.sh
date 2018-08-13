/bin/avrdude -C/etc/avrdude.conf -v -patmega328p -carduino -P/dev/ttyUSB0 -b57600 -D -Uflash:w:./build/mainloop.ino.hex:i 
