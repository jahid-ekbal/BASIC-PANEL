$(document).ready(function () {
    console.log('headshot ready')



    $("#aimbotLoad").click(function (e) { 
        e.preventDefault();
        $("#aimbotLoad").addClass("hidden");
        $("#spinner1").removeClass("hidden");
        $.ajax({
            type: "POST",
            url: "/aimbot-load",

            success: function (response) {
                if(response.status == 200)
                {
                    $("#aimbotLoad").addClass('border-[#1bbc9b] text-white');
                    $("#spinner1").addClass("hidden");
                    $("#aimbotLoad").removeClass("hidden");

                }
                else {
                    $("#spinner1").addClass("hidden");
                    $("#aimbotLoad").removeClass("hidden");
                    $("#aimbotLoad").addClass('bg-inherit text-white');
                }
            }
        });
    });
    $("#aimbotEnable").click(function (e) { 
        e.preventDefault();
        $("#aimbotEnable").addClass("hidden");
        $("#aimbotDisable").addClass("hidden");
        $("#spinner2").removeClass("hidden");
        $.ajax({
            type: "POST",
            url: "/aimbot-on",

            success: function (response) {
                if(response.status == 200)
                {
                    $("#aimbotEnable").addClass('border-[#1bbc9b]');
                    $("#aimbotDisable").removeClass('border-[#1bbc9b]');
                    $("#spinner2").addClass("hidden");
                    $("#AimEnable").removeClass("hidden");
                }
                else {
                    $("#spinner2").addClass("hidden");
                    $("#AimEnable").removeClass("hidden");
                    $("#aimbotEnable").addClass('bg-inherit text-white');
                }
            }
        });
        $("#aimbotEnable").removeClass("hidden");
        $("#aimbotDisable").removeClass("hidden");
    });
    $("#aimbotDisable").click(function (e) { 
        e.preventDefault();
        $("#aimbotDisable").addClass("hidden");
        $("#spinner2").removeClass("hidden");
        $.ajax({
            type: "POST",
            url: "/aimbot-off",

            success: function (response) {
                if(response.status == 200)
                {
                    $("#aimbotDisable").addClass('border-[#1bbc9b]');
                    $("#aimbotEnable").removeClass('border-[#1bbc9b]');
                    $("#spinner2").addClass("hidden");
                    $("#AimDisable").removeClass("hidden");
                }
                else {
                    $("#spinner2").addClass("hidden");
                    $("#AimDisable").removeClass("hidden");
                    $("#aimbotDisable").addClass('bg-slate-600 text-white');
                }
            }
        });
        $("#aimbotDisable").removeClass("hidden");
    });
    $("#dragLoad").click(function (e) { 
        e.preventDefault();
        $("#dragLoad").addClass("hidden");
        $("#spinner3").removeClass("hidden");
        $.ajax({
            type: "POST",
            url: "/aimdrag-load",

            success: function (response) {
                if(response.status == 200)
                {
                    $("#spinner3").addClass("hidden");
                    $("#dragLoad").removeClass("hidden");
                    $("#dragLoad").addClass('border-[#1bbc9b] text-white');
                }
                else {
                    $("#spinner3").addClass("hidden");
                    $("#dragLoad").removeClass("hidden");
                    $("#dragLoad").addClass('bg-inherit text-white');
                }
            }
        });
    });
    $("#dragEnable").click(function (e) { 
        e.preventDefault();
        $("#spinner4").removeClass("hidden");
        $("#dragEnable").addClass("hidden");
        $.ajax({
            type: "POST",
            url: "/aimdrag-on",

            success: function (response) {
                if(response.status == 200)
                {
                    $("#spinner4").addClass("hidden");
                    $("#dragEnable").removeClass("hidden");
                    $("#dragEnable").addClass('border-[#1bbc9b]');
                    $("#dragDisable").removeClass('border-[#1bbc9b]');
                }
                else {
                    $("#spinner4").addClass("hidden");
                    $("#dragEnable").removeClass("hidden");
                    $("#dragEnable").addClass('bg-slate-600 text-white');
                }
            }
        });
    });
    $("#dragDisable").click(function (e) { 
        e.preventDefault();
        $("#spinner4").removeClass("hidden");
        $("#dragDisable").addClass("hidden");
        $.ajax({
            type: "POST",
            url: "/aimdrag-off",

            success: function (response) {
                if(response.status == 200)
                {
                    $("#spinner4").addClass("hidden");
                    $("#dragDisable").removeClass("hidden");
                    $("#dragDisable").addClass('border-[#1bbc9b]');
                    $("#dragEnable").removeClass('border-[#1bbc9b]');
                }
                else {
                    $("#spinner4").addClass("hidden");
                    $("#dragDisable").removeClass("hidden");
                    $("#dragDisable").addClass('bg-inherit');
                }
            }
        });
    });
});