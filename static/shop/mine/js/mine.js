$(document).ready(function(){


    var logout = document.getElementById("logout")

    logout.addEventListener("click",function(){
        $.get("/logout/",function(){
            window.location.href="/shop/"
        })
    })
})