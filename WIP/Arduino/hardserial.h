#ifndef _HARDWARESERIAL_H
#define _HARDWARESERIAL_H
#include "interface.h"
#include <string.h>
//#include <time.h>

namespace SPIRLe {

	class HardwareSerialCommProvider : public ICommProvider {
		int baud;

	public:
		HardwareSerialCommProvider(int baud_rate);
		~HardwareSerialCommProvider();
		bool open();
		bool close();
		int available();
		bool write(const string& s);
		bool write(const char* s);
		void read(string& out, int len = 0);
		bool poll_read(int timeout = 0);
		bool poll_write(int timeout = 0);
	};
}

#endif