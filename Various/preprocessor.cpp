#include <iostream>
#include <string>
#include <map>
#include <utility>
#include <vector>
#include <cctype>
#include <sstream>
#include <algorithm>

using std::string;
using std::cout;
using std::cin;
using std::cerr;
using std::endl;
using std::map;
using std::vector;
using std::pair;
using std::isspace;
using std::copy;
using std::stringstream;

template <typename T> inline T string_to_numeric(const string& str) {
	stringstream ss(str);
	T result;
	ss >> result;
	return result;
}

template <typename T> inline string numeric_to_string(const T num) {
	stringstream ss;
	ss << num;
	return ss.str();
}

void explode(const string& text, const string& separator, vector<string>& results) {
	string::size_type found;
	string copy(text);
	const string::size_type separator_size = separator.length();
	do {
		found = copy.find(separator);
		if(found > 0){
			results.push_back(copy.substr(0, found));
		}
		copy = copy.substr(found + separator_size);
	}
	while(found != string::npos);

	if(results.empty()) {
		results.push_back(text);
	}
	return;
}

void explode_by_first_of(const std::string& text, const std::string& separator, std::vector<std::string>& results) {
	std::string::size_type found;
	std::string copy(text);
	do {
		found = copy.find_first_of(separator);
		if(found > 0){
			results.push_back(copy.substr(0, found));
		}
		copy = text.substr(found + 1);
	}
	while(found != std::string::npos);

	if(results.empty()) {
		results.push_back(text);
	}
	return;
}

void ltrim(string& text) {
  string::size_type i = 0;
  const string::size_type text_size = text.size();
  while(i < text_size && isspace(text[i])) {
  	++i;
  }
  text.erase(0, i);
}

void rtrim(string& text) {
  string::size_type i = text.size();
  while (i > 0 && isspace(text[i - 1])) {
  	--i;
  }
  text.erase(i);
}

void trim(string& text) {
  ltrim(text);
  rtrim(text);
}

bool replace_char(string& text, const char candidate, const string& new_text) {
	const string::size_type text_size = text.size();
	bool did_change = false;
	for(string::size_type i = 0; i < text_size; ++i) {
		if(text[i] == candidate) {
			text.replace(i, 1, new_text);
			did_change = true;
		}
	}
	return did_change;
}

bool replace_string(string& text, const string& candidate, const string& new_text) {
	string::size_type found = text.find(candidate);
	bool did_change = false;
	while(found != string::npos) {
		text.replace(found, candidate.size(), new_text);
		did_change = true;
		found = text.find(candidate, found + 1);
	}
	return did_change;
}

void syntax_error(size_t line, string what) {
	cerr << "Syntax error on line " << line << ". " <<  what << "." << endl;
	//exit(1);
}

enum Type_t {
	INT, FP, STRING, BOOL, VOID
};

struct Instruction {
	string name;
	string desc;
	string function;
	Type_t ret;
	string sourcefile;
	string prototype;
	vector<Type_t> ops;
};

vector<Instruction> insts;

void fill_insts() {
	Instruction i;
	i.name = "Flash LED";
	i.desc = "Flash a connected LED";
	i.function = "flashLed";
	i.ret = VOID;
	i.sourcefile = "flashled.cpp";
	i.prototype = "void flashLed(int)";
	i.ops.push_back(INT);
	insts.push_back(i);
}

vector<string> read_input() {
	vector<string> res;
    string line = "";
    getline(cin, line);

    while(!cin.eof()) {
    	res.push_back(line);
        getline(cin, line);
    }
    res.push_back(line);

    return res;
}

int main() {
	fill_insts();
	vector<string> lines = read_input();
	string::size_type temp, begin, end;
	string res;
	for(int j = 0; j < lines.size(); ++j) {
		res = lines[j];
		for(int i = 0; i < insts.size(); ++i) {
			begin = res.find(insts[i].function);
			while(begin != string::npos) {
				temp = begin + insts[i].function.size();
				//!: will also match calls within comments
				if(res[temp] == '(') {
					//assume we've found function call
					//!: will also match nested function end
					end = res.find(")", temp);
					if(end == string::npos) {
						//clearly this line didn't contain any function call at all
						break;
					}
					++temp; //get inside parenthesis
					string inner_call = res.substr(temp, end - temp);
					vector<string> args;
					explode(inner_call, ",", args);
					if(args.size() != insts[i].ops.size() || (args.size() == 1 && args[0].empty())) {
						syntax_error(j + 1, "Invalid parameter count in call to " + insts[i].function);
					}
					string ss;
					ss = "sockwrite(\"";
					ss += insts[i].function;
					//!: format forbids literal newlines in strings
					for(int k = 0; k < args.size(); ++k) {
						//!: currently doesn't test type
						if(!args[k].empty())
						ss += "\\n" + args[k];
					}
					ss += "\\n\\n" "\")";
					cout << end;
					res = res.replace(begin, end, ss);
					begin = res.find(insts[i].function, end);
				}
			}
		}
		lines[j] = res;
	}
	for(int i = 0; i < lines.size(); ++i) {
		cout << lines[i] << "\r\n";
	}
	return 0;
}