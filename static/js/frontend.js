"use strict";

$(document).ready(function(){

    $(".card-body-signup").hide();
    
    $(".form-signin").on('submit', function(event){

        event.preventDefault();
        
        /* get ID and check if valid */
        const userID = $("#userID").val();

        $.ajax({
            url: "/validate",
            data: {
                userID: userID,
            },
            type: 'POST',
            success: function(){
                window.location.href = "/ratings/" + userID
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
                window.location.href = "/ratings/" + userID
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

    $("#logout").on('click', function(){
        /* log out and send to home page */
        window.location.href = "/"
    })

});