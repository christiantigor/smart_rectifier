<?php
$servername = "localhost";
$username = "monitor";
$password = "1234";
$dbname = "smartRectifier";

//create connection
$conn = new mysqli($servername,$username,$password,$dbname);
//check connection
if($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

$sql = "SELECT * FROM networkParameter LIMIT 1";
$result = $conn->query($sql);
$data = $result->fetch_assoc();
$valIP = $data["IP"];
$valNetmask = $data["Netmask"];
$valGateway = $data["Gateway"];
$valNetwork = $data["Network"];
$valBroadcast = $data["Broadcast"];

$arr = array(
    'IP' => $valIP,
    'Netmask' => $valNetmask,
    'Gateway' => $valGateway,
    'Network' => $valNetwork,
    'Broadcast' => $valBroadcast
);
echo json_encode($arr);

$conn->close();
?>

