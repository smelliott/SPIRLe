#include <Boards.h>
#include <Wire.h>
#include <Dns.h>
#include <EthernetUdp.h>
#include <EthernetServer.h>
#include <EthernetClient.h>
#include <Dhcp.h>
#include <util.h>
#include <Ethernet.h>
#include "Arduino.h"
#include "string.h"
#include <cstring>
#include <ctime>

#define ms() (clock() / CLOCKS_PER_SEC) * 1000


namespace SPIRLe {

class EthernetSocketCommProvider : public ICommProvider {
		int port;
		EthernetServer s;
		EthernetClient c;

	public:
		EthernetSocketCommProvider(int port_no) : port(port_no), s(port_no) {
		}

		~EthernetSocketCommProvider() {
			close();
		}

		inline bool open() {
			char mac[] = {0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED };
			Ethernet.begin(mac); //should also take IP, gateway etc. or use DHCP
			s.begin();
			c = s.available();
			return true;
		}

		inline bool close() {
			c.stop();
			return true;
		}

		inline int available() {
			return c.available();
		}

		bool write(const string& s) {
			const char* str = s.c_str();
			size_t str_size = std::strlen(str);
			int ret = s.write(str, str_size);
			if(ret < str_size) {
				string again = s.substr(ret);
				return write(again);
			}
			return true;
		}

		bool write(const char* s) {
			string str(s);
			return write(str);
		}

		string read(int len = 0) {
			int av = available();
			if(av == 0) {
				return "";
			}
			if(len == 0) {
				len = av;
			}
			string ret = "";
			for(int i = 0; i < len; ++i) {
				ret += c.read();
			}
			return ret;
		}

		bool poll_read(int timeout = 0) {
			//have to implement own timeout on arduino
			clock_t end = ms() + timeout;
			while(ms() < end) {
				if(available() > 0) {
					return true;
				}
			}
			return false;
		}

		bool poll_write(int timeout = 0) {
			//can't poll serial writes on arduino
			return true;
		}
	};
}