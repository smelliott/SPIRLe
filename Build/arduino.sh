avr-g++ -c -g -Os -Wall -fno-exceptions -ffunction-sections -fdata-sections -mmcu=%MMU% -DF_CPU=%CLOCK% -DARDUINO=%ARDUINOVER% -I./lib/hardware/arduino/cores/arduino -I./lib/hardware/arduino/variants/standard %USERCODE%.cpp -o%USERCODE%.o
# avr-gcc -c -g -Os -Wall -ffunction-sections -fdata-sections -mmcu=atmega328p -DF_CPU=16000000L -DARDUINO=100 -I./hardware/arduino/cores/arduino -I./lib/hardware/arduino/variants/standard ./lib/hardware/arduino/cores/arduino/wiring_analog.c -o./wiring_analog.o
avr-ar rcs ./core.a ./wiring_analog.o
avr-gcc -Os -Wl,--gc-sections -mmcu=atmega328p -o./%USERCODE%.elf ./%USERCODE%.o ./core.a -L. -lm
avr-objcopy -O ihex -j .eeprom --set-section-flags=.eeprom=alloc,load --no-change-warnings --change-section-lma .eeprom=0 ./%USERCODE%.elf ./%USERCODE%.eep
avr-objcopy -O ihex -R .eeprom ./%USERCODE%.elf ./%USERCODE%.hex
avrdude -C/usr/share/arduino/hardware/tools/avrdude.conf -v -v -v -v -p%atmega328p% -carduino -P%/dev/ttyACM0% -b%115200% -D -Uflash:w:./%USERCODE%.hex:i
