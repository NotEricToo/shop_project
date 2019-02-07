$(document).ready(function () {
    var coadsid = document.getElementById("coadsid") // 地址详情框


    $(".my-pay-ul li > a").click(function(){
        $(".my-pay-ul li > a").removeClass('hover');
        $(".my-pay-ul li > a i").removeClass('am-icon-check-circle').addClass('am-icon-circle-thin');
        $(this).addClass('hover');
        var val = $(this).attr('rel');
        $("#paytype").val(val);
        $(this).find('i').removeClass('am-icon-circle-thin').addClass('am-icon-check-circle');


    });

    function validate_address(){
        var adsid = adsselectid.value
        if(adsid==""){
            alert("请选择地址！")
            coadsid.style.display = "none"
            return false
        }
        return true
    }
    var adsselectid = document.getElementById("adsselectid") // 地址选择

    adsselectid.addEventListener("change",function () {
        var adsid = adsselectid.value
        validate_address()

        $.get("/updatecoaddress/",{"adsid":adsid},function (data) {
            coadsid.style.display = "block"
            coadsid.innerHTML = data
        })

    })
    
    recartpage.addEventListener("click",function () {
        window.location.href="/cart/"
    })



})