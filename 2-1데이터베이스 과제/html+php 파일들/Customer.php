<?php
$ID = $_POST['ID'];
$password = $_POST['password'];
$address = $_POST['address'];
$email = $_POST['email'];
$buycode= $_POST['buycode'];

$host = "localhost";
$dbusername = "root";
$dbpassword = "";
$dbname = "testdb";

// Create connection
$conn = new mysqli ($host, $dbusername, $dbpassword, $dbname);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
} 
echo "Connected successfully \n";

$sql = "INSERT INTO customer (ID, password, address, email, buycode) values ('$ID', '$password', '$address', '$email', '$buycode') ";
      
if ($conn->query($sql)){
	echo "New record is inserted sucessfully";
	}
	else{
echo "Error: ". $sql ." ". $conn->error;
     }
$conn->close();