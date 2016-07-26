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

$sql = "SELECT * FROM sensorDataCurrent LIMIT 1";
$result = $conn->query($sql);
$data = $result->fetch_assoc();
$valVAC = (float)$data["srVAC"];
$valVBat = (float)$data["srVBat"];
$valIBat = (float)$data["srIBat"];
$valILoad = (float)$data["srILoad"];
$valMdm0 = (float)$data["srMdm0"];
$valMdm1 = (float)$data["srMdm1"];
$valMdm2 = (float)$data["srMdm2"];
$valMdm3 = (float)$data["srMdm3"];
$valSCADA = (float)$data["srSCADA"];
$valSCPC = (float)$data["srSCPC"];
$valBUC = (float)$data["srBUC"];
$valTemp = (float)$data["srTemp"];
$valMdmType = $data["mdmType"];

$arr = array(
    'srVAC' => $valVAC,
    'srVBat' => $valVBat,
    'srIBat' => $valIBat,
    'srILoad' => $valILoad,
    'srMdm0' => $valMdm0,
    'srMdm1' => $valMdm1,
    'srMdm2' => $valMdm2,
    'srMdm3' => $valMdm3,
    'srSCADA' => $valSCADA,
    'srSCPC' => $valSCPC,
    'srBUC' => $valBUC,
    'srTemp' => $valTemp,
    'mdmType' => $valMdmType
);
echo json_encode($arr);

$conn->close();
?>
