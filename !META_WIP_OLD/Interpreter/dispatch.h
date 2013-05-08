#ifndef _DISPATCH_H
#define _DISPATCH_H

#include <string>
#include <vector>
#include <map>
#include <utility>
#include <sstream>

struct Operand {
	std::string name;
	std::string type;
	bool optional;
};

struct Instruction {
	std::string name;
	std::string desc;
	std::string function;
	std::string ret;
	std::string sourcefile;
	std::string prototype;
	std::vector<Operand> ops;
};

template <typename T> inline T string_to_numeric(const std::string& str) {
	std::stringstream ss(str);
	T result;
	ss >> result;
	return result;
}

template <typename T> inline std::string numeric_to_string(const T num) {
	std::stringstream ss;
	ss << num;
	return ss.str();
}

std::string dispatch(const std::string inst, const std::vector<std::string> args);
void fill_instructions();

#endif