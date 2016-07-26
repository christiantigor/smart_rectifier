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

$sql = "SELECT srVAC FROM sensorDataCurrent ORDER BY srVAC ASC LIMIT 1";
$result = $conn->query($sql);
$data = $result->fetch_assoc();
$valVAC = (float)$data["srVAC"];

$sql = "SELECT srVBat FROM sensorDataCurrent ORDER BY srVBat ASC LIMIT 1";
$result = $conn->query($sql);
$data = $result->fetch_assoc();
$valVBat = (float)$data["srVBat"];

$sql = "SELECT srIBat FROM sensorDataCurrent ORDER BY srIBat ASC LIMIT 1";
$result = $conn->query($sql);
$data = $result->fetch_assoc();
$valIBat = (float)$data["srIBat"];

$sql = "SELECT srILoad FROM sensorDataCurrent ORDER BY srILoad ASC LIMIT 1";
$result = $conn->query($sql);
$data = $result->fetch_assoc();
$valILoad = (float)$data["srILoad"];

$sql = "SELECT srMdm0 FROM sensorDataCurrent ORDER BY srMdm0 ASC LIMIT 1";
$result = $conn->query($sql);
$data = $result->fetch_assoc();
$valMdm0 = (float)$data["srMdm0"];

$sql = "SELECT srMdm1 FROM sensorDataCurrent ORDER BY srMdm1 ASC LIMIT 1";
$result = $conn->query($sql);
$data = $result->fetch_assoc();
$valMdm1 = (float)$data["srMdm1"];

$sql = "SELECT srMdm2 FROM sensorDataCurrent ORDER BY srMdm2 ASC LIMIT 1";
$result = $conn->query($sql);
$data = $result->fetch_assoc();
$valMdm2 = (float)$data["srMdm2"];

$sql = "SELECT srMdm3 FROM sensorDataCurrent ORDER BY srMdm3 ASC LIMIT 1";
$result = $conn->query($sql);
$data = $result->fetch_assoc();
$valMdm3 = (float)$data["srMdm3"];

$sql = "SELECT srSCADA FROM sensorDataCurrent ORDER BY srSCADA ASC LIMIT 1";
$result = $conn->query($sql);
$data = $result->fetch_assoc();
$valSCADA = (float)$data["srSCADA"];

$sql = "SELECT srSCPC FROM sensorDataCurrent ORDER BY srSCPC ASC LIMIT 1";
$result = $conn->query($sql);
$data = $result->fetch_assoc();
$valSCPC = (float)$data["srSCPC"];

$sql = "SELECT srBUC FROM sensorDataCurrent ORDER BY srBUC ASC LIMIT 1";
$result = $conn->query($sql);
$data = $result->fetch_assoc();
$valBUC = (float)$data["srBUC"];

$sql = "SELECT srTemp FROM sensorDataCurrent ORDER BY srTemp ASC LIMIT 1";
$result = $conn->query($sql);
$data = $result->fetch_assoc();
$valTemp = (float)$data["srTemp"];

$sql = "SELECT mdmType FROM sensorDataCurrent ORDER BY mdmType ASC LIMIT 1";
$result = $conn->query($sql);
$data = $result->fetch_assoc();
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
