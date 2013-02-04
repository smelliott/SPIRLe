#include "Arduino.h"

void set_pin_digital(int pin, bool v) {
	pinMode(pin, OUTPUT);
	if(v) {
		digitalWrite(pin, HIGH);
	}
	else {
		digitalWrite(pin, LOW);
	}
}

void set_pin_analog(int pin, int v) {
	pinMode(pin, OUTPUT);
	analogWrite(pin, v % 256); //brute force the value to < 256
}

bool get_pin_digital(int pin) {
	pinMode(pin, INPUT);
	return ((digitalRead(pin) == HIGH) ? true : false);
}

int get_pin_analog(int pin) {
	pinMode(pin, INPUT);
	return analogRead(pin);
}