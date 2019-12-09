"use strict";

$(document).ready(function(){

    $(".card-body-signup").hide();
    
    $(".form-signin").on('submit', function(){

        /* get ID and check if valid */
        const userID = $("#userID").val();
        
    })

    $(".sign-up").on('click', function(){
        $(".card-body-signin").hide();
        $(".card-body-signup").show();
    })

    $(".sign-in").on('click', function(){
        $(".card-body-signup").hide();
        $(".card-body-signin").show();
    })











});