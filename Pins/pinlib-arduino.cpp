#include "Arduino.h"

class Pin {
public:
	static void set(const int pin, const int v);
	static int get(const int pin);
};

class DigitalPin : public Pin {
public:
	static inline void set(const int pin, const int v) {
		pinMode(pin, OUTPUT);
		if(v == 1) {
			digitalWrite(pin, HIGH);
		}
		else {
			digitalWrite(pin, LOW);
		}
	}

	static inline int get(const int pin) {
		pinMode(pin, INPUT);
		return ((digitalRead(pin) == HIGH) ? 1 : 0);
	}
};

class AnalogPin : public Pin {
public:
	static inline void set(const int pin, const int v) {
		//analogWrite() on true analog pins (A0-An)
		pinMode(pin, OUTPUT);
		analogWrite(pin, v % 256); //brute force the value to < 256
	}

	static inline int get(const int pin) {
		pinMode(pin, INPUT);
		return analogRead(pin);
	}
};

class PwmPin : public Pin {
public:
	static inline void set(const int pin, const int v) {
		//analogWrite() on PWMs (certain digital pins)
		pinMode(pin, OUTPUT);
		analogWrite(pin, v % 256); //brute force the value to < 256
	}

	static inline int get(const int pin) {
		return -1;
	}
};
