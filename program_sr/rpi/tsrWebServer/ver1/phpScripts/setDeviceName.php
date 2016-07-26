<?php
$newDeviceName = $_GET["newDeviceName"];
$cmd = "sudo hostname " . $newDeviceName;

$out = shell_exec('sudo hostname asu');
echo $out;

$arr = array(
    'status' => 'success'
);
echo json_encode($arr);
?>
