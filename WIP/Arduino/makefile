CORES=./lib/hardware/arduino/cores/arduino
STDVARIANT=./lib/hardware/arduino/variants/standard
AVRD_CONF=./lib/avrdude.conf

MMU=atmega328p
CPUCLOCK=16000000L
ARDUINOVER=103
SERIALPORT=/dev/ttyACM0
BAUDRATE=115200

CODENAME=mycode

GC_HWOPTS=-mmcu=$(MMU) -DF_CPU=$(CPUCLOCK) -DARDUINO=$(ARDUINOVER)
GC_STDINC=-I$(CORES) -I$(STDVARIANT)
GPP_OPTS=-c -g -Os -Wall -fno-exceptions -ffunction-sections -fdata-sections $(GC_HWOPTS) $(GC_STDINC)
GCC_OPTS=-c -g -Os -Wall -ffunction-sections -fdata-sections $(GC_HWOPTS) $(GC_STDINC)
GCC_LINKOPTS=-Os -Wl,--gc-sections -L. -lm -mmcu=$(MMU)
OBJCPY_EEPOPTS=-O ihex -j .eeprom --set-section-flags=.eeprom=alloc,load --no-change-warnings --change-section-lma .eeprom=0
OBJCPY_HEXOPTS=-O ihex -R .eeprom
AVRD_OPTS=-C$(AVRD_CONF) -p$(MMU) -carduino -P$(SERIALPORT) -b$(BAUDRATE) -D -Uflash:w:./$(CODENAME).hex:i

build:
	#avr-g++ $(GPP_OPTS) -ointerface.o ./interface.cpp
	avr-g++ $(GPP_OPTS) -ostring.o string.cpp
	avr-g++ $(GPP_OPTS) -ohardserial.o hardserial.cpp
	avr-g++ $(GPP_OPTS) -o$(CODENAME).o $(CODENAME).cpp
	avr-gcc $(GCC_OPTS) -owiring_analog.o $(CORES)/wiring_analog.c
	avr-gcc $(GCC_OPTS) -owiring_digital.o $(CORES)/wiring_digital.c
	avr-gcc $(GCC_OPTS) -owiring_pulse.o $(CORES)/wiring_pulse.c
	avr-gcc $(GCC_OPTS) -owiring_shift.o $(CORES)/wiring_shift.c
	avr-gcc $(GCC_OPTS) -owiring.o $(CORES)/wiring.c
	avr-gcc $(GCC_OPTS) -oWInterrupts.o $(CORES)/WInterrupts.c
	avr-g++ $(GPP_OPTS) -oCDC.o $(CORES)/CDC.cpp
	avr-g++ $(GPP_OPTS) -oHardwareSerial.o $(CORES)/HardwareSerial.cpp
	avr-g++ $(GPP_OPTS) -oHID.o $(CORES)/HID.cpp
	avr-g++ $(GPP_OPTS) -oIPAddress.o $(CORES)/IPAddress.cpp
	avr-g++ $(GPP_OPTS) -onew.o $(CORES)/new.cpp
	avr-g++ $(GPP_OPTS) -oPrint.o $(CORES)/Print.cpp
	avr-g++ $(GPP_OPTS) -oStream.o $(CORES)/Stream.cpp
	avr-g++ $(GPP_OPTS) -oTone.o $(CORES)/Tone.cpp
	avr-g++ $(GPP_OPTS) -oUSBCore.o $(CORES)/USBCore.cpp
	avr-g++ $(GPP_OPTS) -oWString.o $(CORES)/WString.cpp
	avr-g++ $(GPP_OPTS) -oWMath.o $(CORES)/WMath.cpp
	avr-ar rcs ./core.a ./wiring_analog.o
	avr-ar rcs ./core.a ./wiring_digital.o
	avr-ar rcs ./core.a ./wiring_pulse.o
	avr-ar rcs ./core.a ./wiring_shift.o
	avr-ar rcs ./core.a ./wiring.o
	avr-ar rcs ./core.a ./WInterrupts.o
	avr-ar rcs ./core.a ./CDC.o
	avr-ar rcs ./core.a ./HardwareSerial.o
	avr-ar rcs ./core.a ./HID.o
	avr-ar rcs ./core.a ./IPAddress.o
	avr-ar rcs ./core.a ./new.o
	avr-ar rcs ./core.a ./Print.o
	avr-ar rcs ./core.a ./Stream.o
	avr-ar rcs ./core.a ./Tone.o
	avr-ar rcs ./core.a ./USBCore.o
	avr-ar rcs ./core.a ./WString.o
	avr-ar rcs ./core.a ./WMath.o
	avr-gcc $(GCC_LINKOPTS) -o$(CODENAME).elf $(CODENAME).o string.o hardserial.o core.a
	avr-objcopy $(OBJCPY_EEPOPTS) $(CODENAME).elf $(CODENAME).eep
	avr-objcopy $(OBJCPY_HEXOPTS) $(CODENAME).elf $(CODENAME).hex
	avrdude $(AVRD_OPTS)

clean:
	-rm -f *.o *.hex *.eep *.elf core.a

rebuild: clean build