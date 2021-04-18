<!doctype html>
<html lang="en">
<head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css"
          integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
    <link media="all" type="text/css" rel="stylesheet" href="https://pro.fontawesome.com/releases/v5.2.0/css/all.css">
    <link rel="icon" href="icon.png">
    <title>Frequent itemsets | Project Python</title>
    <link rel="stylesheet" type="text/css" href="css/common.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.2.13/semantic.min.css">
    <link rel="stylesheet"
          href="https://cdnjs.cloudflare.com/ajax/libs/jquery.tablesorter/2.31.3/css/theme.bootstrap_4.min.css">


    <style type="text/css">
        .background-ripple {
            width: 100vw;
            height: 100vh;
            position: absolute;
            background: black;
            z-index: 100000000000000;
        }

        .lds-ripple {
            background: black;
            display: inline-block;
            width: 80px;
            height: 80px;
            position: absolute;
            z-index: 1000;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);

        }

        .lds-ripple div {
            position: absolute;
            border: 4px solid #fff;
            opacity: 1;
            border-radius: 50%;
            animation: lds-ripple 1s cubic-bezier(0, 0.2, 0.8, 1) infinite;
        }

        .lds-ripple div:nth-child(2) {
            animation-delay: -0.5s;
        }

        @keyframes lds-ripple {
            0% {
                top: 36px;
                left: 36px;
                width: 0;
                height: 0;
                opacity: 1;
            }
            100% {
                top: 0px;
                left: 0px;
                width: 72px;
                height: 72px;
                opacity: 0;
            }
        }

    </style>
</head>
<body>


<?php
session_start();
error_reporting(E_ALL);
ini_set('display_errors', 1);
if (!isset($_SESSION["first_load"])) {
    $_SESSION["first_load"] = "true";
} else {
    $_SESSION["first_load"] = "false";

}

$string = file_get_contents("data.json");
$json_a = json_decode($string, true);
if ($json_a['filename'] == "" || $json_a['filename'] == null) {
    $json = array("filename" => "retail_dataset.csv", "min" => 0.1, "direct" => "file_upload", "row" => null);
    $info = json_encode($json);
    $file = fopen('data.json', 'w+') or die("File not found");
    fwrite($file, $info);
    fclose($file);
}


if (!empty($_SESSION['message'])) {
    $message = $_SESSION['message'];
    echo "<input type='hidden' name='message' value='" . $message . "'>";
    $_SESSION['message'] = null;

} else {
    echo "<input type='hidden' name='message' value=''>";

}

?>

<div class="container-custom" id="container-custom">
    <div class="field-button">
        <button class="btn btn-danger " id="close-btn">X</button>
    </div>
    <div class="box">

        <div class="title">
            <span class="block"></span>
            <h1>Frequent Itemsets<span></span></h1>
        </div>

        <div class="role">
            <div class="block"></div>
            <p>Language : Python & PHP</p>
        </div>

    </div>
</div>

<!--<a href="" target="_blank"><footer>-->
<!---->
<!--        <span>-->
<!--            <i class="fas fa-user-graduate"></i>-->
<!--             51703077 - Dương Nhật Hào</span>-->
<!---->
<!--        <span>-->
<!--            <i class="fas fa-user-graduate"></i>-->
<!--             517003030 - Nguyễn Thanh Song Trúc</span>-->
<!--    </footer>-->
<!--</a>-->


<?php
$output = shell_exec("python test.py");

echo $output;

?>
<div class="modal fade" id="modalLoginForm" tabindex="-1" role="dialog" aria-labelledby="myModalLabel"
     aria-hidden="true">
    <div class="modal-dialog" role="document">
        <div class="modal-content">
            <div class="modal-header text-center">
                <h4 class="modal-title w-100 font-weight-bold">Upload File</h4>
                <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                    <span aria-hidden="true">&times;</span>
                </button>
            </div>
            <div class="modal-body mx-3">
                <div class="md-form mb-5">
                    <form action="upload.php" method="post" enctype="multipart/form-data">
                        <p class="text-danger">Only Support *.CSV:</p>
                        <div class="custom-file mb-3">
                            <input type="file" class="custom-file-input" id="file" name="file">
                            <label class="custom-file-label" for="customFile">Choose file</label>
                        </div>
                        <div class="mt-3">
                            <input type="submit" class="btn btn-danger" id="btn-submit" disabled name="submit"
                                   value="Upload"/>
                        </div>
                    </form>
                </div>


            </div>
        </div>
    </div>
</div>


<div class="modal modal-custom fade" id="modalSettingForm" tabindex="-1" role="dialog" aria-labelledby="myModalLabel"
     aria-hidden="true">
    <div class="modal-dialog" role="document">
        <div class="modal-content">
            <div class="modal-header text-center">
                <h4 class="modal-title w-100 font-weight-bold">Setting Input</h4>
                <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                    <span aria-hidden="true">&times;</span>
                </button>
            </div>
            <div class="modal-body mx-3">
                <div class="md-form mb-5">
                    <form action="edit.php" method="post" id="form-setting" class="ui form">
                        <label class="form-title">File: </label>
                        <select name="file" class="ui search dropdown file-dropdown w-100 ">
                            <option value="">File CSV</option>
                            <?php
                            $fileList = glob('file_upload/*csv');
                            foreach ($fileList as $filename) {
                                echo "<option value='" . explode("/", $filename)[1] . "'>" . explode("/",
                                        $filename)[1] . "</option>";
                            }

                            ?>
                        </select>
                        <div class="field" id="field-row">


                        </div>
                        <label for="min-support" class="form-title">Min Support (Max: 1): </label>
                        <input type="number" name="min-support" id="min-support" min="0" max="1" step="0.00000001">
                        <div class="field py-2 d-flex justify-content-end">

                            <input type="submit" class='btn btn-success '>

                        </div>
                    </form>
                </div>


            </div>
        </div>
    </div>
</div>
<input type="hidden" name="json_array_rating">
<input type="hidden" name="json_array_item">
<div class="buy-recommend h-100">
    <div class="container">
        <div class="row">
            <div class="col-6"> <h2>List Item From Data Set</h2>
                <form>
                    <?php
                    $string2 = file_get_contents("json/product.json");
                    $json_a2 = json_decode($string2, true);
                    $string3 = file_get_contents("json/itemset.json");
                    $json_a3 = json_decode($string3, true);

                    foreach ($json_a2 as $val) {

                        echo "<div class='checkbox'>
                <label><input type='checkbox' class='input-check'  value='$val'> $val</label>
            </div>";

                    }

                    $recommend_rating = [];
                    $recommend_set = [];
                    foreach ($json_a3 as $val) {
                        foreach ($val as $item) {
                            array_push($recommend_rating,$item[0]["Support"]);
                            array_push($recommend_set,$item[1]);


                        }

                    }
//                    var_dump($recommend_rating);
//
//                    var_dump($recommend_set);
                    ?>
                </form></div>
            <div class="col-6"><ul class="list-group" id="list-group">

                </ul></div>
        </div>


    </div>
</div>

</body>


<!-- Optional JavaScript -->
<!-- jQuery first, then Popper.js, then Bootstrap JS -->
<script src="https://code.jquery.com/jquery-3.2.1.slim.min.js"
        integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN"
        crossorigin="anonymous"></script>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js"
        integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q"
        crossorigin="anonymous"></script>
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js"
        integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl"
        crossorigin="anonymous"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.2.13/semantic.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/jquery.tablesorter/2.31.3/js/jquery.tablesorter.min.js"></script>

</body>
<script>










    var first_load = "<?php echo $_SESSION['first_load']; ?>";
    if (first_load != "true") {
        $("#container-custom").css("display", "none")
    }
    $('#close-btn').click(function () {
        $("#container-custom").css({
            "visibility": "hidden",
            "opacity": 0,
            "transition": "visibility 2s,opacity 0.5s linear",
        });

        setTimeout(
            function () {
                $("#container-custom").css({
                    "display": "none",

                });
            }, 600);

    });
    // Add the following code if you want the name of the file appear on select
    $(function () {
        $('[data-toggle="tooltip"]').tooltip()
    })

    $('#file').on('change', function () {
        myfile = $(this).val();
        var ext = myfile.split('.').pop();
        if (ext == "csv") {
            if (document.getElementById("file").files.length != 0) {
                document.getElementById("btn-submit").removeAttribute("disabled");

                var fileName = $(".custom-file-input").val().split("\\").pop();
                $(".custom-file-input").siblings(".custom-file-label").addClass("selected").html(fileName);

            }
        } else {
            alert("Only Support CSV File");
            $('#file').val("");
            $(".custom-file-input").siblings(".custom-file-label").html("Choose file");
        }
    });
    $(document).ready(function () {


        $.getJSON("json/itemset.json", function(json) {
             a =[];
             b =[];
            for (i = 0; i < json.length; i++) {
                $("#list-group").append("<li class='list-group-item-set'"+"setitem='"+json[i]["itemsets"][1]+"'"+"value='"+json[i]["itemsets"][0]["Support"]+"'>("+json[i]["itemsets"][0]["Support"]*100+"%) : "+json[i]["itemsets"][1]+"</li>")
            }



        });
        var item_buy = [];
        var item_recommend = [];

        var json_array_rating =$('input[name="json_array_rating"]').val();
        var json_array_item =$('input[name="json_array_item"]').val();
        console.log($('input[name="json_array_item"]').val());

        let checker = (arr, target) => target.every(v => arr.includes(v));

        $('.input-check').click(function () {
            if(item_buy.indexOf($(this).val())>-1){
                item_buy.splice(item_buy.indexOf($(this).val()), 1);
            }
            else{
                item_buy.push($(this).val());
                item_buy = item_buy.filter(function(itm, i, a) {
                    return i == a.indexOf(itm);
                });
            }
            for (i = 0; i < $('.list-group-item-set').length; i++) {

                arr2 = $('.list-group-item-set')[i].attributes.setitem.value.split(",");
                if(checkinclude(item_buy,arr2)==true){
                    $('.list-group-item-set')[i].setAttribute("style","display:block")
                    console.log(arr2);

                }
                else{
                    $('.list-group-item-set')[i].setAttribute("style","display:none")
                }
            }


            console.log(item_buy);
        });
        setTimeout(
            function () {
                $('.background-ripple').css("display", "none");

            }, 2000);
    });

    function checkinclude(arr1,arr2) {
        check = true;
        for (j = 0; j < arr1.length; j++) {
            if(!arr2.includes(arr1[j])){
                check = false;

            }
        }

        return check;
    }
    if ($('input:hidden[name=message]').val() != '') {
        alert($('input:hidden[name=message]').val());
        $('input:hidden[name=message]').val('');
    }
    $('.ui.dropdown')
        .dropdown()
    ;

    $(".file-dropdown").dropdown({
        clearable: false,
        onChange: function (value, text, $choice) {
            $.ajax({

                url: "ajax.php",
                method: "GET",
                data: {
                    file_name: value
                },
                dataType: "json",
                beforeSend: function () {
                    console.log(value)
                },
                success: function (response) {

                    $("#field-row").html(
                        "<label>Row use(Max: " + response.len + ")</label>" +
                        response.input_item
                    );
                    // $("#menu").html(result.item_address);
                    //
                },
                error: function (xhr, status, error) {


                },
                complete: function (xhr, status) {

                }
            });
        }
    });
    $(function () {
        $("#table-result").tablesorter();
    });
</script>
</html>



