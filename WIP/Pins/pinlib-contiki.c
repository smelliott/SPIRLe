#include "hal/micro/micro-common.h"

//partial implementation, need to talk to Steve about Contiki

void set_pin_digital(uint32_t pin, bool v) {
	halGpioConfig(pin, GPIOCFG_IN);
	halGpioSet(pin, v);
}

bool get_pin_digital(uint32_t pin) {

}