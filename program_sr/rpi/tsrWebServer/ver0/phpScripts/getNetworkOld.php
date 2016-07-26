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

$sql = "SELECT IP FROM networkParameter ORDER BY IP ASC LIMIT 1";
$result = $conn->query($sql);
$data = $result->fetch_assoc();
$valIP = $data["IP"];
//echo $valIP;

$sql = "SELECT Netmask FROM networkParameter ORDER BY Netmask ASC LIMIT 1";
$result = $conn->query($sql);
$data = $result->fetch_assoc();
$valNetmask = $data["Netmask"];
//echo $valNetmask;

$sql = "SELECT Gateway FROM networkParameter ORDER BY Gateway ASC LIMIT 1";
$result = $conn->query($sql);
$data = $result->fetch_assoc();
$valGateway = $data["Gateway"];
//echo $valGateway;

$sql = "SELECT Network FROM networkParameter ORDER BY Network ASC LIMIT 1";
$result = $conn->query($sql);
$data = $result->fetch_assoc();
$valNetwork = $data["Network"];
//echo $valNetwork;

$sql = "SELECT Broadcast FROM networkParameter ORDER BY Broadcast ASC LIMIT 1";
$result = $conn->query($sql);
$data = $result->fetch_assoc();
$valBroadcast = $data["Broadcast"];
//echo $valBroadcast;

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

