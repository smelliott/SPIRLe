<?php

require_once("generator.php");

define("SOCKET_WRITE_FUNC", "sockwrite");
define("OUTPUT_FILENAME", "library.py");

$output = "";
foreach($insts as $i) {
	$output = "def ";
	$output .= $i->function;
	$output .= "(";
	for($x = 0; $x < count($i->operands); $x++) {
		$output .= $i->operands[$x]->name;
		$output .= ",";
	}
	$output = rtrim($output, ",");
	$output .= "):\n";
	$output .= "\t";
	$os = "\"" . $i->function;
	for($x = 0; $x < count($i->operands); $x++) {
		$os .= "\\n\" + ";
		$os .= $i->operands[$x]->name;
	}
	$os .= " + \"\\n\\n\"";
	$output .= SOCKET_WRITE_FUNC . "(" . $os . ")";
	$output .= "\n\n";
}

file_put_contents(OUTPUT_FILENAME, $output);
?>