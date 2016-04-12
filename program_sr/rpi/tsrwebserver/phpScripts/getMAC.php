<?php
$out = shell_exec('cat /sys/class/net/eth0/address');
$code = substr($out,0,-1);

$arr = array(
    'kodePerangkat' => $code
);
echo json_encode($arr);
?>

