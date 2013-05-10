#ifndef _MOCKCOMM_H
#define _MOCKCOMM_H
#include "interface.h"
#include <string.h>
//#include <time.h>

namespace SPIRLe {

	class MockCommProvider : public ICommProvider {

	public:
		MockCommProvider() { }
		~MockCommProvider() { }
		bool open() {
			return true;
		}
		bool close() {
			return true;
		}
		int available() {
			return 0;
		}
		bool write(const string& s) {
			return true;
		}
		bool write(const char* s) {
			return true;
		}
		char* read(int len = 0) {
			return NULL;
		}
		bool poll_read(int timeout = 0) {
			return true;
		}
		bool poll_write(int timeout = 0) {
			return true;
		}
	};
}

#endif