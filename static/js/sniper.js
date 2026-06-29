$(document).ready(function () {
    console.log('Sniper Ready')



    $("#ssEnable").click(function (e) { 
        e.preventDefault();
        $.ajax({
            type: "POST",
            url: "/sniper-switch-on",
            success: function (response) {
                if(response.status == 200)
                {
                    $("#ssEnable").addClass('border-[#1bbc9b] text-white');
                    $("#ssDisable").removeClass('border-[#1bbc9b]');
                }
                else {
                    $("#ssEnable").addClass('bg-inherit text-white');
                }
                
            }
        });
    });
    $("#ssDisable").click(function (e) { 
        e.preventDefault();
        $.ajax({
            type: "POST",
            url: "/sniper-switch-off",
            success: function (response) {
                if(response.status == 200)
                {
                    $("#ssDisable").addClass('border-[#1bbc9b] text-white');
                    $("#ssEnable").removeClass('border-[#1bbc9b]');
                }
                else {
                    $("#ssDisable").addClass('bg-inherit text-white');
                }
                
            }
        });
    });
    $("#swEnable").click(function (e) { 
        e.preventDefault();
        $.ajax({
            type: "POST",
            url: "/sniper-scope-on",
            success: function (response) {
                if(response.status == 200)
                {
                    $("#swEnable").addClass('border-[#1bbc9b]');
                    $("#swDisable").removeClass('border-[#1bbc9b]');
                }
                else {
                    $("#swEnable").addClass('bg-inherit text-white');
                }
                
            }
        });
    });
    $("#swDisable").click(function (e) { 
        e.preventDefault();
        $.ajax({
            type: "POST",
            url: "/sniper-scope-off",
            success: function (response) {
                if(response.status == 200)
                {
                    $("#swDisable").addClass('border-[#1bbc9b] text-white');
                    $("#swEnable").removeClass('border-[#1bbc9b]');
                }
                else {
                    $("#swDisable").addClass('bg-inherit text-white');
                }
                
            }
        });
    });
});