$(document).ready(function () {
    console.log('emulatorjs');
    $("#btn1").addClass("active");

    $("#btn1").click(function (e) { 
        $.ajax({
            type: "POST",
            url: "/update-bit32",
            success: function (response) {
                if(response.status == 200)
                {
                    $("#btn1").addClass("active");
                    $("#btn2").removeClass("active");
                }
            }
        });
    });
    $("#btn2").click(function (e) { 
        
        $.ajax({
            type: "POST",
            url: "/update-bit64",
            success: function (response) {
                if(response.status == 200)
                {
                    $("#btn2").addClass("active");
                    $("#btn1").removeClass("active");
                }
            }
        });
    });
});