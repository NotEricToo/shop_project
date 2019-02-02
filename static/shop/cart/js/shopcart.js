$(document).ready(function () {
    var delbtncls = document.getElementsByClassName("am-fr")

    for(var i =0 ; i < delbtncls.length ; i++ ){
        delbtn  = delbtncls[i]
        
        delbtn.addEventListener("click",function () {
            var btngavalue = this.getAttribute("ga")
            var delbtnid = document.getElementById("cartlist"+btngavalue) // 删除这个li
            var cfdel = confirm("确定删除该产品?")
            if(cfdel){
                $.get("/updateToCart/2/",{"prodid":btngavalue},function (data) {
                    delbtnid.parentNode.removeChild(delbtnid) // 删除该节点
                    // 更新总数和价格
                    updateTotalInfo(data.totalnum,data.totalprice)
                })
            }



        })
        
    }
})