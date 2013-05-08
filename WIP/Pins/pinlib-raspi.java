//potential java functions for rpi using the http://github.com/jkransen/framboos lib

public class Pin {
	boolean get_pin_digital(int pin) {
		InPin i = new InPin(pin);
		boolean ret = i.getValue();
		i.close();
		return ret;
	}

	void set_pin_digital(int pin, boolean v) {
		OutPin o = new OutPin(pin);
		o.setValue(v);
		o.close();
		return;
	}
}