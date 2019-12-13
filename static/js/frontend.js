"use strict";

$(document).ready(function(){

    $(".card-body-signup").hide();
    $("#update-input").hide();
    $("#delete-input").hide();
    
    $(".form-signin").on('submit', function(event){

        event.preventDefault();
        
        /* get ID and check if valid */
        const userID = $("#userID").val();

        $.ajax({
            url: "/validateUser",
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

    $("#form-delete").on('submit', function(e){

        const bookID = $().val();
        const userID = getUserID();
        e.preventDefault();

        $.ajax({
            url: "/deleteRating",
            data: {
                bookID: bookID,
            },
            type: 'POST',
            success: function(){
                window.location.href = "/ratings/" + userID /* TODO: get user ID in get request */
            },
            error: function(){
                alert("This book does not exist or you have not rated it.")
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

    $("#add-button").on('click', function(){
        $("#update-input").show();
    });

    $("#delete-button").on('click', function(){
        $("#delete-input").show();
    })

    function getUserID(){

        userID = 0

        $.ajax({
            url: "/",
            type: 'GET',
            success: function(response){
                userID = response.data.userID
            },
            error: function(){
                alert("dang")
            }
        })

        return userID
    }

});