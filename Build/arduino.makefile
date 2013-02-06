CORES=./lib/hardware/arduino/cores/arduino
STDVARIANT=./lib/hardware/arduino/variants/standard
AVRD_CONF=./avrdude.conf

MMU=atmega328p
CPUCLOCK=16000000L
ARDUINOVER=100
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
	avr-g++ $(GPP_OPTS) -o$(CODENAME).o $(CODENAME).cpp
	avr-gcc $(GCC_OPTS) -owiring_analog.o $(CORES)/wiring_analog.c
	#...
	avr-ar rcs ./core.a ./wiring_analog.o
	#...
	avr-gcc $(GCC_LINKOPTS) -o$(CODENAME).elf ./core.a $(CODENAME).o
	avr-objcopy $(OBJCPY_EEPOPTS) $(CODENAME).elf $(CODENAME).eep
	avr-objcopy $(OBJCPY_HEXOPTS) $(CODENAME).elf $(CODENAME).hex
	avrdude $(AVRD_OPTS)

clean:
	-rm -f *.o *.hex *.eep core.a

rebuild: clean, build
