$(document).ready(function () {
    var collectproduct = document.getElementById("collectproduct") // 收藏商品

    //iscollect = collectproduct.getAttribute("ga") // 是否已经收藏




    // updateCollect()
    collectproduct.addEventListener("click",function () {
        islogin = collectproduct.getAttribute("lg")
        if(islogin == 0 ){
            window.location.href = "/login/"
        }else{
            prodid = collectproduct.getAttribute("pd")
            $.get("/collectproduct/",{"prod_id":prodid},function (data) {
            collectproduct.innerHTML = data
        })
        }


    })

    var addtocart = document.getElementById("addtocart") // 加入购物车
    addtocart.addEventListener("click",function () {
        var prod_num = document.getElementById("prod_num").value // 获取prod 数量
        var prod_id = collectproduct.getAttribute("pd") // 获取prod_id
        // alert(prod_num)
        $.get("/addtocart/",{"prod_num":prod_num,"prod_id":prod_id},function (data) {
            if(data.status == "nologin"){
                window.location.href = "/login/"
            }

            if(data.status == "error"){
                alert("添加错误或已添加商品多于库存，请确认后重试！")
            }

            if(data.status == "success"){
                alert("添加成功！")
            }
        })
    })


    
    
})