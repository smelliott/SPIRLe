using System;
using System.Text;
using Microsoft.SPOT;
using Microsoft.SPOT.Hardware;
using System.Net;
using System.Net.Sockets;

namespace SPIRLe {

	public class SocketCommProvider : ICommProvider {
		public const int TIMEOUT = 5;
		public const int US_PER_SEC = 1000000;

		public int port { get; private set; }
		public IPEndPoint bind_ip { get; private set; }
		private Socket s = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
		private Socket c;

		public SocketCommProvider(int port, string local_ip) {
			//this.bind_ip = ...
			this.port = port;
			this.bind_ip = new IPEndPoint(IPAddress.Any, port);
			s.Bind(bind_ip);
			s.Listen(Int32.MaxValue);
		}

		~SocketCommProvider() {
			s.Close();
		}

		public bool open() {
			c = s.Accept();
			return true;
		}

		public bool close() {
			c.Close();
			c = null;
			return true;
		}

		public int available() {
			if(c == null) {
				return -1;
			}
			return c.Available;
		}

		public bool write(string s) {
			if(c == null || !poll_write(0)) {
				return false;
			}

			int res = c.Send(UTF8Encoding.UTF8.GetBytes(s));
			if(res == -1) {
				return false;
			}
			if(res < s.Length) {
				//not all data made it. try again.
				return write(s.Substring(res));
			}
			return true;
		}

		public string read(int len = 0) {
			if(c == null || !poll_read(0)) {
				return null;
			}
			int av = available();
			if(av == 0) {
				return "";
			}

			int res = 0; int temp;
			string ret = "";

			if(len == 0) {
				len = av;
			}

			while(len > res) {
				byte[] msg = new byte[len];
				temp = c.Receive(msg, len - res, SocketFlags.None);
				if(temp == -1) {
					return null;
				}
				res += temp;
				ret += UTF8Encoding.UTF8.GetChars(msg).ToString();
			}
			return ret;
		}

		public bool poll_read(int timeout = TIMEOUT) {
			return c.Poll(timeout * US_PER_SEC, SelectMode.SelectRead);
		}

		public bool poll_write(int timeout = TIMEOUT) {
			return c.Poll(timeout * US_PER_SEC, SelectMode.SelectWrite);
		}
	}
}