$(document).ready(function () {

    // 点击删除， 直接删除对应的li
    var delbtnlist = document.getElementsByClassName("deladsbtn") // 列表的单个 li

    for(var i = 0 ; i < delbtnlist.length ; i++){
        adsli = delbtnlist[i]
        adsli.addEventListener("click",function () {
            var liga = this.getAttribute("ga")
            var lidom = document.getElementById("adsli"+liga)
            if(confirm("确定删除该地址？")){
                // ajax 删除该地址
                $.get("/deleteAddress/",{"adsid":liga},function (data) {
                    if(data.status == "success"){
                        lidom.parentNode.removeChild(lidom)
                    }
                })
            }

        })
    }

    // 点击每个 收货地址， 直接进行update 页面
    var adslistli = document.getElementsByClassName("updtadsbtn") // 点击那个li

    for(var i = 0 ; i< adslistli.length; i++ ){
        var  clkli = adslistli[i]
        
        clkli.addEventListener("click",function () {
            var adsid = this.getAttribute("ga")
            // alert("to page"+adsid)
            window.location.href="/updateAddress/"+adsid+"/"
        })

    }
})