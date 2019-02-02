$(document).ready(function(){

    // 根据分类显示产品
    var ids = document.getElementsByClassName("getid")
    for (var i = 0 ; i<ids.length;i++){
        subid = ids[i]
        subid.addEventListener("click",function () {
            var sub = this.getAttribute("ga")
            $.ajax({
                url:"/cglist/",
                data:{"sub_id":sub,"type":0},
                method:"get",
                success:function(data){
                    if(data.length>0){
                        $("#cg-prodlist").html(data)
                    }

                }
            })
        })
    }

    // 搜索框
    var cg_searchid = document.getElementById("cg_searchid") // 输入框
    var cg_searchbtn = document.getElementById("cg_searchbtn") // 点击按钮
    
    cg_searchbtn.addEventListener("click",function () {
        var searchText = cg_searchid.value
        $.get("/cglist/",{"searchText":searchText,"type":1},function (data) {
            if(data.length>0){
                $("#cg-prodlist").html(data)
            }
        })
    })

})