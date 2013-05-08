using System;
using Microsoft.SPOT;
using Microsoft.SPOT.Hardware;
using Gadgeteer;

namespace SPIRLe {
	public class DigitalPin {
		public static bool setv(int socket, int pin, bool v) {
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

		public static bool getv(int socket, int pin) {
			InputPort ip = new InputPort((Cpu.Pin)pin, false, Port.ResistorMode.Disabled); //need to check this is right
			return ip.Read();
		}

	}

	public class AnalogPin {
		public static void setv(int socket, int pin, int v) {
			AnalogOutput ao = new AnalogOutput((Cpu.AnalogOutputChannel)pin);
			ao.WriteRaw(v);
		}

		public static int getv(int socket, int pin) {
			AnalogInput ai = new AnalogInput((Cpu.AnalogChannel)pin);
			return ai.ReadRaw();
		}
	}

	public class PwmPin {
		public static void setv()
	}
}