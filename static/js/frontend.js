"use strict";

$(document).ready(function(){

    $(".card-body-signup").hide();
    
    $(".form-signin").on('submit', function(){

        /* get ID and check if valid */
        const uID = $("#userID").val();

        $.post("/validate", {
            userID: uID
        });
        
    })

    $(".form-signup").on('submit', function(){

        /* get ID and add to users database */
        const uID = $("#new-user-id").val();
        console.log(uID)
        $.post("/addNewUser", {
            userID: uID
        });

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