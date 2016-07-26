<?php
$valDeviceName = shell_exec('hostname');

$arr = array(
    'DeviceName' => $valDeviceName
);
echo json_encode($arr);
?>
