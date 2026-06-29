$(document).ready(function () {
    console.log('ready');
    var msgbox = false;

    $("#consolebtn").click(function (e) { 
        e.preventDefault();
        msgbox = !msgbox;
        // $("#consolebtn").toggleClass('hidden');
        
        if (msgbox)
        {
            $("#consolebtn").text("Close");
            // $("#consolebtn").text("Close");
            // $("#console").addClass('h-48');
            $("#console").toggleClass('hidden');
            $.ajax({
                type: "POST",
                url: "/logs",
                success: function (response) {
                    if (response.status)
                    {
                        var contents = ""
                        response.message.forEach(element => {
                            var content = `<span class="text-green-400 text-lg">${element}</span>`
                            contents += content
                        });
                        $("#console").html(contents)
                    }
                }
            });
        }
        else {
            $("#consolebtn").text("Open");
            // $("#consolebtn").text("Open");
            // $("#console").addClass('hidden');
            $("#console").toggleClass('hidden');
        }
    });
});