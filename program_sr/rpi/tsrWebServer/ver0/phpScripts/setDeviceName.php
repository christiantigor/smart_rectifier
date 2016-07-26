<?php
$servername = "localhost";
$username = "monitor";
$password = "1234";
$dbname = "smartRectifier";

$newDeviceName = $_GET["newDeviceName"];

//create DB connection
$conn = new mysqli($servername,$username,$password,$dbname);
//check DB connection
if($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

//Save network parameter to DB
$sql = "UPDATE networkParameter SET"
    . " DeviceName = \"" . $newDeviceName . "\""
    . " WHERE Name = \"netParam\"";

if($conn->query($sql) === TRUE) {
    //echo "Record updated successfully";
} else {
    //echo "Error updating record: " . $conn->error;
    exit();
}
$conn->close();

$arr = array(
    'status' => 'success'
);
echo json_encode($arr);
?>
