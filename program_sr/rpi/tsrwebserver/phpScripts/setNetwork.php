<?php
$servername = "localhost";
$username = "monitor";
$password = "1234";
$dbname = "smartRectifier";

$newAddress = $_GET["newAddress"];
$newNetmask = $_GET["newNetmask"];
$newGateway = $_GET["newGateway"];
$newNetwork = $_GET["newNetwork"];
$newBroadcast = $_GET["newBroadcast"];

//Validate network parameter
$validAddress = false;
$validNetmask = false;
$validGateway = false;
$validNetwork = false;
$validBroadcast = false;

if(filter_var($newAddress,FILTER_VALIDATE_IP)){
    $validAddress = true;
}
if(filter_var($newNetmask,FILTER_VALIDATE_IP)){
    $validNetmask = true;
}
if(filter_var($newGateway,FILTER_VALIDATE_IP)){
    $validGateway = true;
}
if(filter_var($newNetwork,FILTER_VALIDATE_IP)){
    $validNetwork = true;
}
if(filter_var($newNetwork,FILTER_VALIDATE_IP)){
    $validBroadcast = true;
}

//Print network parameter
if($validAddress && $validNetmask && $validGateway && $validNetwork && $validBroadcast){
    //echo "Correct Address: " . $newAddress . "<br>";
    //echo "Correct Netmask: " . $newNetmask . "<br>";
    //echo "Correct Gateway: " . $newGateway . "<br>";
    //echo "Correct Network: " . $newNetwork . "<br>";
    //echo "Correct Broadcast: " . $newBroadcast . "<br>";
} else{
    //echo "At least one of network parameter is false<br>";
    $arr = array(
        'status' => 'failed'
    );
    echo json_encode($arr);
    exit();
}

//----- Success get network parameter -----

//create DB connection
$conn = new mysqli($servername,$username,$password,$dbname);
//check DB connection
if($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

//Save network parameter to DB
$sql = "UPDATE networkParameter SET"
    . " IP = \"" . $newAddress . "\","
    . " Netmask = \"" . $newNetmask . "\","
    . " Gateway = \"" . $newGateway . "\","
    . " Network = \"" . $newNetwork . "\","
    . " Broadcast = \"" . $newBroadcast . "\""
    . " WHERE Name = \"netParam\"";

if($conn->query($sql) === TRUE) {
    //echo "Record updated successfully";
} else {
    //echo "Error updating record: " . $conn->error;
    exit();
}
$conn->close();


//Write new interfaces file
//Notes: user need to create file manually first then change permission to 666
$fileLoc = getcwd();

$newFile = fopen($fileLoc . "/interfaces","w") or die("unable to open file!");
//print_r(error_get_last());
$txt = "#TSR Generated Interfaces File\n\n";
fwrite($newFile,$txt);
$txt = "auto lo\n";
fwrite($newFile,$txt);
$txt = "iface lo inet loopback\n\n";
fwrite($newFile,$txt);

$txt = "auto eth0\n";
fwrite($newFile,$txt);
$txt = "iface eth0 inet static\n";
fwrite($newFile,$txt);
$txt = "address " . $newAddress . "\n";
fwrite($newFile,$txt);
$txt = "gateway " . $newGateway . "\n";
fwrite($newFile,$txt);
$txt = "netmask " . $newNetmask . "\n";
fwrite($newFile,$txt);
$txt = "network " . $newNetwork . "\n";
fwrite($newFile,$txt);
$txt = "broadcast " . $newBroadcast . "\n\n";
fwrite($newFile,$txt);

$txt = "auto wlan0\n";
fwrite($newFile,$txt);
$txt = "allow-hotplug wlan0\n";
fwrite($newFile,$txt);
$txt = "iface wlan0 inet manual\n";
fwrite($newFile,$txt);
$txt = "wpa-conf /etc/wpa_supplicant/wpa_supplicant.conf\n\n";
fwrite($newFile,$txt);

$txt = "auto wlan1\n";
fwrite($newFile,$txt);
$txt = "allow-hotplug wlan1\n";
fwrite($newFile,$txt);
$txt = "iface wlan1 inet manual\n";
fwrite($newFile,$txt);
$txt = "wpa-conf /etc/wpa_supplicant/wpa_supplicant.conf\n\n";
fwrite($newFile,$txt);
fclose($newFile);
//echo "Finish write file<br>";

//Copy new interfaces file to /etc/network
//Note: create file on /etc/network first then change permission to 666
//copy("/var/www/phpScripts/customFile", "/etc/network/customFile");
copy("/var/www/phpScripts/interfaces", "/etc/network/interfaces");
print_r(error_get_last());
//echo "Finish copy file<br>";
$arr = array(
    'status' => 'success'
);
echo json_encode($arr);
?>
