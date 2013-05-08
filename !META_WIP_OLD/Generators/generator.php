<?php
define("XML_LOCATION", "test/");

class Operand {
	public $name;
	public $optional;
	public $type;
}

class Instruction {
	public $name;
	public $desc;
	public $function;
	public $return;
	public $sourcefile;
	public $prototype;
	public $operands;
}


$insts = Array();

$z = 0;

foreach(glob(XML_LOCATION . "*.xml") as $fn) {
	$xml = simplexml_load_file($fn);
	$i = new Instruction();
	$i->name = $xml->name;
	$i->desc = $xml->desc;
	$i->function = $xml->function;
	$i->return = $xml->return;
	$i->sourcefile = $xml->sourcefile;
	$i->prototype = $xml->prototype;
	$i->operands = Array();
	$x = 0;
	foreach($xml->operands->operand as $op) {
		$newop = new Operand();
		$newop->name = $op["name"];
		$newop->optional = $op["optional"];
		$newop->type = $op["type"];
		$i->operands[$x] = $newop;
		$x++;
	}

	$insts[$z] = $i;
	$z++;
}
?>