$(document).ready(function(){
    // form 控件
    var lgusername = document.getElementById("lgusername") // 账户 username
    var lgpassword = document.getElementById("lgpassword") // 密码 password
    var loginbtn = document.getElementById("loginbtn") // 点击 login 按钮

    // 错误信息标签
    var lgnamenull = document.getElementById("lgnamenull") // 账户为空
    var lgpswnull = document.getElementById("lgpswnull") // 密码为空
    var lgpswerror = document.getElementById("lgpswerror") // 账户密码错误



    // username 验证
    //验证函数
    function valida_lgusername(){
        var uname = lgusername.value

        if(uname.replace('/\s+/g',"")==""){
            lgnamenull.style.display = "block"

            return false
        }
        return true
    }
    //执行验证
    lgusername.addEventListener('blur',valida_lgusername)
    // 取消错误信息
     lgusername.addEventListener('focus',function(){
        lgnamenull.style.display = "none"
     })

    // password 验证
    //验证函数
    function valid_lgpassword(){
         var psw = lgpassword.value

        if(psw.replace('/\s+/g',"")==""){
            lgpswnull.style.display = "block"
            return false
        }
        return true
    }
    //执行验证
    lgpassword.addEventListener('blur',valid_lgpassword)
    // 取消错误信息
     lgpassword.addEventListener('focus',function(){
        lgpswnull.style.display = "none"
        lgpswerror.style.display = "none"
     })

    loginbtn.addEventListener("click",function(){
        if(
            valida_lgusername()
            && valid_lgpassword()
        ){
            $.post("/login/",{"username":lgusername.value,"password":lgpassword.value},function(data){
                if(data.status=="success"){
                    window.location.href="/shop/"
                }else{
                    lgpswerror.style.display = "block"
                }
            })
        }
    })
})