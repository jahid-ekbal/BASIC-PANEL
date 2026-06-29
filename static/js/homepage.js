$(document).ready(function () {
    console.log('ready');




    

});
function auth()
    {
        username = $("#username").val();
        password = $("#password").val();

        SendInfo = {
            username: username,
            password: password
        }

        if(username && password)
        {
            $.ajax({
                type: "POST",
                url: "/auth",
                data: JSON.stringify(SendInfo),
                contentType: "application/json; charset=utf-8",
                success: function (response) {
                    if (response.status == 200)
                    {
                        window.location.href = '/dashboard'
                    }
                    else {
                        $("#status").text("Credentials MisMatch!!!");
                    }
                }
            });
        }
    }