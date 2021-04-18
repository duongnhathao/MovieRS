<?php
session_start();

if ( isset($_POST["submit"]) ) {

    if ( isset($_FILES["file"])) {


        //if there was an error uploading the file
        if ($_FILES["file"]["error"] > 0) {
            $_SESSION['message'] = $_FILES["file"]["error"];
            header('Location: index.php?message=');


        }
        else {
            //Print file details


            //if file already exists
            if (file_exists("file_upload/" . $_FILES["file"]["name"])) {
                $_SESSION['message'] = $_FILES["file"]["name"] . " already exists. ";

                header('Location: index.php');
            }
            else {
                //Store file in directory "upload" with the name of "uploaded_file.txt"
                $storagename = $_FILES["file"]["name"];
                move_uploaded_file($_FILES["file"]["tmp_name"], "file_upload/" . $storagename);
                echo "Stored in: " . "file_upload/" . $_FILES["file"]["name"] . "<br />";
                $_SESSION['message'] = 'Upload file successfully';
                header('Location: index.php');
            }
        }
    } else {
        echo "No file selected <br />";
    }
}
?>