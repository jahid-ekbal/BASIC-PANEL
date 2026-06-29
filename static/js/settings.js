$(document).ready(function () {
    $.ajax({
        type: "POST",
        url: "/user-info",
        success: function (response) {
            if(response.status == 200)
            {
                $("#username").text(response.username);
                $("#hwid").text(response.hwid);
                $("#expiry").text(response.expiry);
                $("#onlineusers").text(response.onlineUsers);
            }
            else {
                $("#username").text('XXXXXX');
                $("#hwid").text('XXXXXX');
                $("#expiry").text('XXXXX');
                $("#onlineusers").text('XXXXX');
            }
        }
    });
});