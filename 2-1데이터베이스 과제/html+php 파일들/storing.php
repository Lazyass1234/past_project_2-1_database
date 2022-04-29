<?php
$ProductCode = $_POST['ProductCode'];
$ProductName = $_POST['ProductName'];
$OutingQuantity = $_POST['OutingQuantity'];
$SaleQuantity = $_POST['SaleQuantity'];
$Price= $_POST['Price'];
$Category= $_POST['Category'];

$host = "localhost";
$dbusername = "root";
$dbpassword = "";
$dbname = "testdb";


$conn = new mysqli ($host, $dbusername, $dbpassword, $dbname);


if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
} 
echo "Connected successfully \n";

$sql = "INSERT INTO purchase (ProductCode, ProductName, OutingQuantity, SaleQuantity, Price, Category) values ('$ProductCode', '$ProductName', '$OutingQuantity', '$SaleQuantity', '$Price', '$Category') ";
      
if ($conn->query($sql)){
	echo "New record is inserted sucessfully";
	}
	else{
echo "Error: ". $sql ." ". $conn->error;
     }
$conn->close();