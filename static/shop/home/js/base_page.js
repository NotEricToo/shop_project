$(document).ready(function () {



})

function addtips(dom,tip){
        sp = document.createElement("span")
        sp.style.color = "red"
        sp.setAttribute("id","errortips")
        sp.innerHTML = tip
        dom.parentNode.insertBefore(sp,dom)

    }

    function removetips() {
        tipdom = document.getElementById("errortips")
        if(tipdom){
            tipdom.parentNode.removeChild(tipdom)
        }
    }