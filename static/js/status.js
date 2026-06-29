$(document).ready(function () {
    console.log('status ok');

    $.ajax({
        type: "POST",
        url: "/get-process",
        success: function (response) {
            if(response.status== 200)
            {
                $("#onlinebtn").text("Online");
                $("#onlinebtn").addClass('bg-blue-600 border-green-400 border');
            }
            else {
                $("#onlinebtn").text("Offline");
                $("#onlinebtn").addClass('bg-inherit border border-red-400');
            }
        }
    });

});