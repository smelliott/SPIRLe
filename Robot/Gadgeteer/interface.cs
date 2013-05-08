using System;
using System.Text;
using Microsoft.SPOT;
using Microsoft.SPOT.Hardware;

namespace SPIRLe {

	public interface ICommProvider {
		public bool write(string s);
		public string read(int len);
		public bool open();
		public bool close();
		public int available();
		public bool poll_read(int timeout);
		public bool poll_write(int timeout);
	}

}