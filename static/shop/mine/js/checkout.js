$(document).ready(function () {
    var coadsid = document.getElementById("coadsid") // 地址详情框
    var commitorder = document.getElementById("commitorder") // 提交订单

    var price_span = document.getElementById("total_amount") // 获取总价格
    var total_price = price_span.innerText

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

    function validate_price(){
        if(total_price==0){
            alert("请选择商品")
            return false
        }else{
            return true
        }
    }
    
    commitorder.addEventListener("click",function () {
        if(
            confirm("提交订单")
            &&validate_address()
            &&validate_price()
        ){

            var adsid = adsselectid.value
            // 添加数据
            var papytype = $("#paytype").val()
            var dict={
                "adsid":adsid,
                "paytype":papytype,
                "total_price":total_price

            }

            $.get("/commitorder/",dict,function (data) {
                if(data.status == "success"){
                    alert("提交订单成功。。")
                    window.location.href = "/mine/"
                }

                if(data.status == "nologin"){
                    window.location.href = "/login/"
                }

            })
            // alert(papytype)
            // To order list page
            // window.location.href=""
        }
    })


})