<?php
$servername = "localhost";
$username = "monitor";
$password = "1234";
$dbname = "srDB";

//create DB connection
$conn = new mysqli($servername,$username,$password,$dbname);
//check DB connection
if($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

//Fetch data to DB
$sql = "SELECT TIMESTAMP(dt) AS 'time',"
    . " srVAC AS 'srVAC', srVBat AS 'srVBat', srIBat AS 'srIBat', srILoad AS 'srILoad',"
    . " sr6V5 AS 'sr6V5', sr12V AS 'sr12V', sr13V5 AS 'sr13V5', sr19V5 AS 'sr19V5',"
    . " sr24V AS 'sr24V', sr48V_A AS 'sr48V_A', sr48V_B AS 'sr48V_B', srTemp AS 'srTemp'" 
    . " FROM srHistory" 
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
