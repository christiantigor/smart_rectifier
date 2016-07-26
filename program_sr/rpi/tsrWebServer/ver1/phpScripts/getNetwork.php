<?php
$ifaceFile = "/etc/network/interfaces";

$lines = file($ifaceFile);
$valIP = str_replace("\n",'',substr($lines[7],strpos($lines[7]," ")+1));
$valGateway = str_replace("\n",'',substr($lines[8],strpos($lines[8]," ")+1));
$valNetmask = str_replace("\n",'',substr($lines[9],strpos($lines[9]," ")+1));
$valNetwork = str_replace("\n",'',substr($lines[10],strpos($lines[10]," ")+1));
$valBroadcast = str_replace("\n",'',substr($lines[11],strpos($lines[11]," ")+1));

$arr = array(
    'IP' => $valIP,
    'Netmask' => $valNetmask,
    'Gateway' => $valGateway,
    'Network' => $valNetwork,
    'Broadcast' => $valBroadcast
);
echo json_encode($arr);
?>

