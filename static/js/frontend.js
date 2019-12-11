"use strict";

$(document).ready(function(){

    $(".card-body-signup").hide();
    
    $("#sign-in-button").on('click', function(){

        /* get ID and check if valid */
        const userID = $("#userID").val();

        $.ajax({
            url: "/validate",
            data: {
                userID: userID,
            },
            type: 'POST',
            success: function(response){
                window.location.href = "/profile/" + userID
            },
        });
        
    })

    $(".form-signup").on('submit', function(){

        /* get ID and add to users database 
        const uID = $("#new-user-id").val();
        $.post("/addNewUser", {
            userID: uID
        });
*/
    });

    $(".sign-up").on('click', function(){
        $(".card-body-signin").hide(300);
        $(".card-body-signup").show(300);
    })

    $(".sign-in").on('click', function(){
        $(".card-body-signup").hide(300);
        $(".card-body-signin").show(300);
    })

});