#include <string>

namespace SPIRLe {

	class ICommProvider {
	protected:
		virtual bool write(const std::string& s) = 0;
		virtual bool write(const char* s) = 0;
		virtual std::string read(int len) = 0;
		virtual bool open() = 0;
		virtual bool close() = 0;
		virtual int available() = 0;
		virtual bool poll_read(int timeout) = 0;
		virtual bool poll_write(int timeout) = 0;
	};

}