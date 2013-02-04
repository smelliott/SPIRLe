#include "fwddecl.h"
#include "dispatch.h"

using namespace std;

map<string, Instruction> insts;

void fill_instructions() {
	Instruction i;
	Operand o;
	i.name = "Flash LED";
	i.desc = "Flash a connected LED";
	i.function = "flashLed";
	i.prototype = "void flashLed(int)";
	i.ret = "void";
	i.sourcefile = "flashled.cpp";
	o.name = "ledId";
	o.type = "int";
	o.optional = true;
	i.ops.push_back(o);
	insts.insert(pair<string, Instruction>("flashLed", i));
}

string dispatch(const string inst, const vector<string> args) {
	if(inst == "flashLed") {
		flashLed(string_to_numeric<int>(args[0]));
		return "true\n\n";
	}
}