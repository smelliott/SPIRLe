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

//inheritance model
// class Instruction {
// protected:
// 	string what;
// 	const int op_count;

// public:
// 	virtual void operator()(void*) = 0;
// 	const std::string& get_what() {

// 	}
// };

//function pointer model
struct Instruction {
	void (*act)(const vector<string>&);
	int oper_min;
	int oper_max;
};

void mvf(const vector<string>& operv) {
	cout << "moving forward with speed: " << operv[0] << endl;
}

void prequel(map<string, Instruction>& inst) {
	Instruction movef;
	movef.oper_min = 1;
	movef.oper_max = 1;
	movef.act = &mvf;

	inst.insert(pair<string, Instruction>("mvf", movef));
}

void syntax_error(size_t line, string what) {
	cerr << "Syntax error on line " << line << ". " <<  what << "." << endl;
	exit(1);
}

int main() {
	map<string, Instruction> inst;
	prequel(inst);

	string input = "mvf 100,100\r\nlol";
	vector<string> lines;
	explode(input, "\n", lines);
	for(vector<string>::size_type i = 0; i < lines.size(); ++i) {
		trim(lines[i]);
		if(lines[i].empty()) {
			continue;
		}
		vector<string> tokens;
		explode_by_first_of(lines[i], " ,", tokens);
		if(tokens.empty()) {
			continue;
		}
		trim(tokens[0]);
		if(inst.find(tokens[0]) == inst.end()) {
			syntax_error(i, "Invalid instruction \"" + tokens[0] + "\"");
		}
		for(vector<string>::size_type j = 1; j < tokens.size(); ++j) {
			trim(tokens[j]);
			if(tokens[j].empty()) {
				tokens.erase(tokens.begin() + j);
			}
		}
		if(tokens.size() - 1 > inst[tokens[0]].oper_max || tokens.size() - 1 < inst[tokens[0]].oper_min) {
			syntax_error(i, "Bad operand count");
		}

		vector<string> operands;
		copy(tokens.begin() + 1, tokens.end(), operands.begin());
		inst[tokens[0]].act(operands);
	}
}
