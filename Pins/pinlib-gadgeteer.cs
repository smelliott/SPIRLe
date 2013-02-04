using System;
using Microsoft.SPOT;
using Microsoft.SPOT.Hardware;
using Gadgeteer;

namespace SPIRLe {
	public class Pin {
		public static bool set_pin_digital(int socket, int pin, bool v) {
			Cpu.Pin p;
			try {
				p = Socket.GetSocket(socket, true, null, null).CpuPins[pin];
			}
			catch(Socket.InvalidSocketException) {
				return false;
			}
			OutputPort op = new OutputPort(p, v);
			return true;
		}

		public static void set_pin_analog(int socket, int pin, int v) {
			AnalogOutput ao = new AnalogOutput((Cpu.AnalogOutputChannel)pin);
			ao.WriteRaw(v);
		}

		public static bool get_pin_digital(int socket, int pin) {
			InputPort ip = new InputPort((Cpu.Pin)pin, false, Port.ResistorMode.Disabled); //need to check this is right
			return ip.Read();
		}

		public static int get_pin_analog(int socket, int pin) {
			AnalogInput ai = new AnalogInput((Cpu.AnalogChannel)pin);
			return ai.ReadRaw();
		}
	}
}