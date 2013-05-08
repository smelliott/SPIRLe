#ifndef _INTERFACE_H
#define _INTERFACE_H

#include "string.h"

namespace SPIRLe {

	class ICommProvider {
	public:
		virtual bool write(const string& s) = 0;
		virtual bool write(const char* s) = 0;
		virtual char* read(int len) = 0;
		virtual bool open() = 0;
		virtual bool close() = 0;
		virtual int available() = 0;
		virtual bool poll_read(int timeout) = 0;
		virtual bool poll_write(int timeout) = 0;
	};

}

#endif