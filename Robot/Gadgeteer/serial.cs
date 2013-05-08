using System;
using System.Text;
using Microsoft.SPOT;
using Microsoft.SPOT.Hardware;
using System.IO.Ports;

namespace SPIRLe {

	public class SerialCommProvider : ICommProvider {
		public string port { get; private set; }
		public int baud { get; private set; }
		private SerialPort sp;

		public bool write(string s) {
			if(!sp.IsOpen) {
				return false;
			}
			byte[] msg = UTF8Encoding.UTF8.GetBytes(s);
			sp.Write(msg, 0, msg.Length);
			return true;
		}

		public string read(int len = 0) {
			if(!sp.IsOpen) {
				return null;
			}
			int av = available();
			if(av == 0) {
				return "";
			}

			if(len == 0) {
				len = av;
			}
			byte[] msg = new byte[len];
			sp.Read(msg, 0, len);
			return UTF8Encoding.UTF8.GetChars(msg).ToString();
		}

		public bool open() {
			if(!sp.IsOpen) {
				sp.Open();
				return true;
			}
			return false;
		}

		public bool close() {
			if(sp.IsOpen) {
				sp.Close();
				return true;
			}
			return false;
		}

		public int available() {
			if(!sp.IsOpen) {
				return -1;
			}
			return sp.BytesToRead;
		}

		public SerialCommProvider(string port, int baud) {
			//this.port = port;
			//this.baud = baud;
			this.port = "COM1";
			this.baud = 9600;
			sp = new SerialPort(port, baud);
		}

		~SerialCommProvider() {
			close();
		}

		public bool poll_read(int timeout = 0) {
			if(timeout == 0) {
				return (available() > 0);
			}
			DateTime now = DateTime.Now;
			now.AddMilliseconds((double)timeout);
			while(now > DateTime.Now) {
				if(available() > 0) {
					return true;
				}
			}
			return false;
		}

		public bool poll_write(int timeout = 0) {
			if(timeout == 0) {
				return (available() != -1 && sp.BytesToWrite == 0);
			}
			DateTime now = DateTime.Now;
			now.AddMilliseconds((double)timeout);
			while(now > DateTime.Now) {
				if(available() != -1 && sp.BytesToWrite == 0) {
					return true;
				}
			}
			return false;
		}

	}

}