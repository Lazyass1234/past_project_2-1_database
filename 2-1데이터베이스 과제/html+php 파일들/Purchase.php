<?php
$PurchaseCode = $_POST['PurchaseCode'];
$PurchasedProductCode = $_POST['PurchasedProductCode'];
$NameOfPurchasedProducts = $_POST['NameOfPurchasedProducts'];
$VolumeOfPurchase = $_POST['VolumeOfPurchase'];
$InVoiceNumber= $_POST['InVoiceNumber'];
$LumpSum= $_POST['LumpSum'];

$host = "localhost";
$dbusername = "root";
$dbpassword = "";
$dbname = "testdb";


$conn = new mysqli ($host, $dbusername, $dbpassword, $dbname);


if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
} 
echo "Connected successfully \n";

$sql = "INSERT INTO purchase (PurchaseCode, PurchasedProductCode, NameOfPurchasedProducts, VolumeOfPurchase, InVoiceNumber, LumpSum) values ('$PurchaseCode', '$PurchasedProductCode', '$NameOfPurchasedProducts', '$VolumeOfPurchase', '$InVoiceNumber', '$LumpSum') ";
      
if ($conn->query($sql)){
	echo "New record is inserted sucessfully";
	}
	else{
echo "Error: ". $sql ." ". $conn->error;
     }
$conn->close();