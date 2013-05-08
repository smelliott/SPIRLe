<?php

require_once("generator.php");

define("DISPATCH_HEADER", "dispatch.h");
define("FILL_FUNCTION_NAME", "fill_instructions");
define("INSTRUCTIONS_VARIABLE", "insts");
define("OUTPUT_FILENAME", "dispatch.cpp");
define("DECL_HEADER", "fwddecl.h");

$output = "#include \"" . DECL_HEADER . "\"\n";
$output .= "#include \"" . DISPATCH_HEADER . "\"\n\n";
$output .= "using namespace std;\n\n";
$output .= "map<string, Instruction> insts;\n\n";
$output .= "void " . FILL_FUNCTION_NAME . "() {\n";
$output .= "\tInstruction i;\n";
$output .= "\tOperand o;\n";

foreach($insts as $i) {
	$output .= "\ti.name = \"" . $i->name . "\";\n";
	$output .= "\ti.desc = \"" . $i->desc . "\";\n";
	$output .= "\ti.function = \"" . $i->function . "\";\n";
	$output .= "\ti.prototype = \"" . $i->prototype . "\";\n";
	$output .= "\ti.ret = \"" . $i->return . "\";\n";
	$output .= "\ti.sourcefile = \"" . $i->sourcefile . "\";\n";
	for($x = 0; $x < count($i->operands); $x++) {
		$output .= "\to.name = \"" . $i->operands[$x]->name . "\";\n";
		$output .= "\to.type = \"" . $i->operands[$x]->type . "\";\n";
		$output .= "\to.optional = " . (($i->operands[$x]->optional) ? "true" : "false") . ";\n";
		$output .= "\ti.ops.push_back(o);\n";
	}
	$output .= "\t" . INSTRUCTIONS_VARIABLE . ".insert(pair<string, Instruction>(\"" . $i->function . "\", i));\n";
}

$output .= "}\n\n";

$output .= "string dispatch(const string inst, const vector<string> args) {\n";
foreach($insts as $i) {
	$output .= "\tif(inst == \"" . $i->function . "\") {\n";
	$output .= "\t\t" . $i->function . "(";
	for($x = 0; $x < count($i->operands); $x++) {
		if($i->operands[$x]->type == "int") {
			$output .= "string_to_numeric<int>(args[" . $x . "]),";
		}
		else if($i->operands[$x]->type == "bool") {
			$output .= "string_to_numeric<bool>(args[" . $x . "]),";
		}
		else if($i->operands[$x]->type == "float") {
			$output .= "string_to_numeric<double>(args[" . $x . "]),";
		}
		else {
			$output .= "args[" . $x . "],";
		}
	}
	$output = rtrim($output, ",");
	$output .= ");\n";
	$output .= "\t\treturn \"true\\n\\n\";\n";
	$output .= "\t}\n";
}
$output .= "}";

file_put_contents(OUTPUT_FILENAME, $output);

$output = "#ifndef _FWDDECL_H\n";
$output .= "#define _FWDDECL_H\n\n";
$output .= "#include <string>\n\n";

foreach($insts as $i) {
	$output .= $i->prototype . ";\n";
}
$output .= "\n#endif";

file_put_contents(DECL_HEADER, $output);
?>