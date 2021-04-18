<?php


$json = file_get_contents("data.json");
$json = json_decode($json   , true);
$file_name =$json['direct']."/".$_REQUEST["file_name"];
$fp = file($file_name);
$input_item =  "<input type='number' name='row' min='1' max='".count($fp)."'value='".count($fp)."'>";



echo json_encode(array('success' => 1,'input_item'=>$input_item,"len"=>count($fp)));
?>