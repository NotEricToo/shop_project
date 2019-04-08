$(document).ready(function () {
    var content = document.getElementById("content") // 评论内容
    var httpreferer = document.getElementById("httpreferer")
    var commentform = document.getElementById("commentform") // form

    var confirmbt = document.getElementById("commitcomment") // 确认提交 comment
    var canclebt = document.getElementById("canclecomment")   // cancle comment

   // var inputpanel = document.getElementById("inputpanel") // input 的 div

    function valid_comment(){
        if(content.value.length > 50){
            return false
        }


        return true
    }

    content.addEventListener("focus",function () {
        removetips()

    })

    confirmbt.addEventListener("click",function () {
        if(
            valid_comment()

        ){
            commentform.submit()
        }
    })
    
    content.addEventListener("change",function () {
        if(!valid_comment()){
            removetips()
            addtips(content,"长度超过50.")

        }
    })

    // 点击取消，回到上一页
    canclebt.addEventListener("click",function () {
        window.location.href=httpreferer.value
    })



})