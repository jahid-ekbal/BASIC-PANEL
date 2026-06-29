$(document).ready(function () {
    console.log('extra ready')

    $("#chamsmenu").click(function (e) { 
        e.preventDefault();
        $.ajax({
            type: "POST",
            url: "/chams-menu",
            success: function (response) {
                if(response.status == 200)
                {
                    $("#chamsmenu").addClass('border-[#1bbc9b] text-white');
                }
                else {
                    $("#chamsmenu").addClass('bg-inherit text-white');
                }
                
            }
        });
    });
    $("#chams3d").click(function (e) { 
        e.preventDefault();
        $.ajax({
            type: "POST",
            url: "/chams-3D",
            success: function (response) {
                if(response.status == 200)
                {
                    $("#chams3d").addClass('border-[#1bbc9b] text-white');
                }
                else {
                    $("#chams3d").addClass('bg-inherit text-white');
                }
                
            }
        });
    });

    $("#mbEnable").click(function (e) { 
        e.preventDefault();
        $.ajax({
            type: "POST",
            url: "/m82b-esp-on",
            success: function (response) {
                if(response.status == 200)
                {
                    $("#mbEnable").addClass('border-[#1bbc9b] text-white');
                    $("#mbDisable").removeClass('border-[#1bbc9b]');
                }
                else {
                    $("#mbEnable").addClass('bg-inherit text-white');
                }
                
            }
        });
    });

    $("#mbDisable").click(function (e) { 
        e.preventDefault();
        $.ajax({
            type: "POST",
            url: "/m82b-esp-off",
            success: function (response) {
                if(response.status == 200)
                {
                    $("#mbDisable").addClass('border-[#1bbc9b] text-white');
                    $("#mbEnable").removeClass('border-[#1bbc9b]');
                }
                else {
                    $("#mbDisable").addClass('bg-inherit text-white');
                }
                
            }
        });
    });

    $("#fovEnable").click(function (e) { 
        e.preventDefault();
        $.ajax({
            type: "POST",
            url: "/aimfov-on",
            success: function (response) {
                if(response.status == 200)
                {
                    $("#fovEnable").addClass('border-[#1bbc9b] text-white');
                    $("#fovDisable").removeClass('border-[#1bbc9b]');
                }
                else {
                    $("#fovEnable").addClass('bg-inherit text-white');
                }
                
            }
        });
    });
    $("#fovDisable").click(function (e) { 
        e.preventDefault();
        $.ajax({
            type: "POST",
            url: "/aimfov-off",
            success: function (response) {
                if(response.status == 200)
                {
                    $("#fovDisable").addClass('border-[#1bbc9b] text-white');
                    $("#fovEnable").removeClass('border-[#1bbc9b]');
                }
                else {
                    $("#fovDisable").addClass('bg-inherit text-white');
                }
                
            }
        });
    });




});