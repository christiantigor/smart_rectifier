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

$sql = "SELECT DeviceName FROM networkParameter ORDER BY DeviceName ASC LIMIT 1";
$result = $conn->query($sql);
$data = $result->fetch_assoc();
$valDeviceName = $data["DeviceName"];

$arr = array(
    'DeviceName' => $valDeviceName
);
echo json_encode($arr);

$conn->close();
?>
