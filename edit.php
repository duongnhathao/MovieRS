<?php
    var_dump($_POST);
$string = file_get_contents("data.json");
$json_a = json_decode($string, true);


if(isset($_POST['file'])&&$_POST['file']!=null){
    $json_a["filename"] = $_POST['file'];
}
if(isset($_POST['min-support'])&&$_POST['min-support']!=null){
    $json_a["min"] = (float) $_POST['min-support'];
}
if(isset($_POST['row'])&&$_POST['row']!=null){
    $json_a["row"] = (integer)$_POST['row'];
}
$newJsonString = json_encode($json_a);
var_dump($newJsonString);
file_put_contents('data.json', $newJsonString);
header('Location: index.php');
?>