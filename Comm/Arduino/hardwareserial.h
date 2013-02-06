#ifndef _HARDWARESERIAL_H
#define _HARDWARESERIAL_H
#include "interface.h"
#include <string>
#include <cstring>
#include <ctime>

namespace SPIRLe {

	class HardwareSerialCommProvider : public ICommProvider {
		int baud;

	public:
		HardwareSerialCommProvider(int baud_rate);
		~HardwareSerialCommProvider();
		inline bool open();
		inline bool close();
		inline int available();
		bool write(const std::string& s);
		bool write(const char* s);
		std::string read(int len = 0);
		bool poll_read(int timeout = 0);
		bool poll_write(int timeout = 0);
	};
}

#endif