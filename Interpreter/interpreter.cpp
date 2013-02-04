#include <iostream>
#include <string>
#include <map>
#include <utility>
#include <vector>
#include <cctype>
#include <sstream>
#include <algorithm>

#include "dispatch.h"

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

extern map<string, Instruction> insts;

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

void syntax_error(string what) {
	cout << "Syntax error: " <<  what << ".\r\n";
}

string read_input() {
	string res;
    string line = "";
    getline(cin, line);

    while(!cin.eof()) {
    	res += line + "\n";
        getline(cin, line);
    }
    res += line + "\n";

    return res;
}

bool validate(const vector<string>& in) {
	if(in.empty() || (in.size() == 1 && in[0].empty())) {
		syntax_error("Bad packet format");
		return false;
	}
	if(insts.find(in[0]) == insts.end()) {
		syntax_error("Unknown instruction \"" + in[0] + "\"");
		return false;
	}
	if(in.size() - 1 != insts[in[0]].ops.size()) {
		syntax_error("Invalid operand count to instruction \"" + in[0] + "\"");
		return false;
	}
	return true;
}

int main() {
	fill_instructions();
	string lines = read_input();
	string::size_type begin, end;
	begin = 0;
	end = lines.find("\n\n");
	while(end != string::npos) {
		vector<string> temp;
		explode(lines.substr(begin, end - begin), "\n", temp);
		if(!validate(temp)) {
			begin = end + 2;
			end = lines.find("\n\n", begin);
			continue;
		}
		vector<string> args;
		for(vector<string>::size_type i = 1; i < temp.size(); ++i) {
			args.push_back(temp[i]);
		}
		dispatch(temp[0], args);
		begin = end + 2;
		end = lines.find("\n\n", begin);
	}

	return 0;
}