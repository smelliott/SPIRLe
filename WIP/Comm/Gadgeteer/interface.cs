using System;
using System.Text;
using Microsoft.SPOT;
using Microsoft.SPOT.Hardware;

namespace SPIRLe {

	public interface ICommProvider {
		bool write(string s);
		string read(int len);
		bool open();
		bool close();
		int available();
		bool poll_read(int timeout);
		bool poll_write(int timeout);
	}

}