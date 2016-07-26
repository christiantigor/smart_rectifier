<?php
$servername = "localhost";
$username = "monitor";
$password = "1234";
$dbname = "smartRectifier";

//create DB connection
$conn = new mysqli($servername,$username,$password,$dbname);
//check DB connection
if($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

//Fetch data to DB
$sql = "SELECT TIMESTAMP(tdate, ttime) AS 'time',"
    . " sensorVAC AS 'srVAC', sensorVBat AS 'srVBat', sensorIBat AS 'srIBat', sensorILoad AS 'srILoad',"
    . " sensorModem0 AS 'srMdm0', sensorModem1 AS 'srMdm1', sensorModem2 AS 'srMdm2', sensorModem3 AS 'srMdm3',"
    . " sensorSCADA AS 'srSCADA', sensorSCPC AS 'srSCPC', sensorBUC AS 'srBUC', sensorTemp AS 'srTemp'" 
    . " FROM sensorDataHistory" 
    . " ORDER BY time DESC LIMIT 1000";

$arr = array();
if ($result = mysqli_query($conn, $sql)) {
    /* fetch associative array */
    while ($row = mysqli_fetch_assoc($result)) {
        array_push($arr,
            $row
        );
    }

    /* free result set */
    mysqli_free_result($result);
}

echo json_encode($arr);

$conn->close();
?>