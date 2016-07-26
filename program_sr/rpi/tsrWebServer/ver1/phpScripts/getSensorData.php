<?php
$servername = "localhost";
$username = "monitor";
$password = "1234";
$dbname = "srDB";

//create connection
$conn = new mysqli($servername,$username,$password,$dbname);
//check connection
if($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

$sql = "SELECT * FROM srCurrent";
$result = $conn->query($sql);
$data = $result->fetch_assoc();
$valVAC = (float)$data["srVAC"];
$valVBat = (float)$data["srVBat"];
$valIBat = (float)$data["srIBat"];
$valILoad = (float)$data["srILoad"];
$val6V5 = (float)$data["sr6V5"];
$val12V = (float)$data["sr12V"];
$val13V5 = (float)$data["sr13V5"];
$val19V5 = (float)$data["sr19V5"];
$val24V = (float)$data["sr24V"];
$val48V_A = (float)$data["sr48V_A"];
$val48V_B = (float)$data["sr48V_B"];
$valTemp = (float)$data["srTemp"];

$arr = array(
    'srVAC' => $valVAC,
    'srVBat' => $valVBat,
    'srIBat' => $valIBat,
    'srILoad' => $valILoad,
    'sr6V5' => $val6V5,
    'sr12V' => $val12V,
    'sr13V5' => $val13V5,
    'sr19V5' => $val19V5,
    'sr24V' => $val24V,
    'sr48V_A' => $val48V_A,
    'sr48V_B' => $val48V_B,
    'srTemp' => $valTemp
);
echo json_encode($arr);

$conn->close();
?>
