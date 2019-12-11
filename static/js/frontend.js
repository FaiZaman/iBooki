"use strict";

$(document).ready(function(){

    $(".card-body-signup").hide();
    
    $("#sign-in-button").on('click', function(e){

        /* get ID and check if valid */
        const userID = $("#userID").val();

        $.ajax({
            url: "/validate",
            data: {
                userID: userID,
            },
            type: 'POST',
            success: function(){
                window.location.href = "/profile/" + userID
            },
            error: function(){
                alert("User ID is invalid. Please try again.")
            }
        });
    })

    $(".form-signup").on('submit', function(e){

        /* get ID and add to users database */
        const userID = $("#new-user-id").val();
        e.preventDefault();
        $.ajax({
            url: "/addNewUser",
            data: {
                userID: userID
            },
            type: 'POST',
            success: function(){
                window.location.href = "/profile/" + userID
            },
            error: function(){
                alert("This ID already exists. Please choose a different ID.")
            }
        })
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