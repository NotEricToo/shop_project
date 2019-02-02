$(document).ready(function(){
    // form 控件
    var username=document.getElementById("username") // 账号 username
    var password=document.getElementById("password")// 第一次密码
    var password2=document.getElementById("password2")// 第二次密码
    var email=document.getElementById("email") // email
    var phonenumber=document.getElementById("phonenumber") // 电话号码
    var agreebox=document.getElementById("agreebox") // 同意协议 box
    var regbutton=document.getElementById("regbutton") // 提交按钮
    var regform = document.getElementById("regform") // 注册 form 表单
    var userimg = document.getElementById("userimg") // 头像上传

    // 错误提示
    var unamenull=document.getElementById("unamenull") // username 不能为空
    var unamelength=document.getElementById("unamelength") // username 不能为空
    var unameexists=document.getElementById("unameexists") // username 已存在
    var paswnull=document.getElementById("paswnull") // paswnull 不能为空
    var pswlength=document.getElementById("pswlength") // paswnull 不能为空
    var paswalign=document.getElementById("paswalign") // 两次密码不一致
    var emailformat=document.getElementById("emailformat") // 邮箱格式
    var emailnull=document.getElementById("emailnull") //  邮箱不能为空
    var phonenull=document.getElementById("phonenull") //  电话号码为空
    var checkagree=document.getElementById("checkagree") //  勾选协议

    // 其他提示
    var usrimgp = document.getElementById("usrimgp") // 头像文件名


    // 验证 username 开始
    // 验证函数
    function valid_username() {
        var uname = username.value

        // 验证是否为空
        if (uname.replace(/\s+/g, "") == "") {
            unamenull.style.display = "block"
            return false
        }

        // 验证长度
        if(uname.replace(/\s+/g, "").length<6 || uname.replace(/\s+/g, "").length>20){
            unamelength.style.display = "block"
            return false
        }
        // 验证是否存在
        $.get('/reg_username/',{'username':uname},function(data){
            // 验证不通过
            if(data.status=="error"){
                unameexists.style.display = 'block'
                return false
            }


        })
        // 格式，输入字符，暂时不做验证

         // 验证成功，返回 true
        return true
    }
    // 执行验证
    // 丢失焦点，验证 username
    username.addEventListener('blur',valid_username)

    // 获得焦点，username 错误提示消失
    username.addEventListener('focus',function(){
        unamenull.style.display="none"
        unameexists.style.display="none"
        unamelength.style.display="none"
    })
    // 验证username 结束

    //验证 password 开始
    // 验证函数
    function valid_password(){
        var psw = password.value
        // 验证是否为空
        if(psw.replace('/\s+/g',"") == ""){
            paswnull.style.display = "block"
            return false
        }
        // 验证长度
        if(psw.replace(/\s+/g, "").length<6 || psw.replace(/\s+/g, "").length>20){
            pswlength.style.display = "block"
            return false
        }

        // 特殊字符， 暂时不做验证
        // 验证成功，返回 true
         return true

    }

    // 丢失焦点， 开始验证
    password.addEventListener('blur',valid_password)

    // 获取焦点， 错误提示消失
    password.addEventListener('focus',function(){
        // 取消所有的错误提示
        paswnull.style.display = "none"
        pswlength.style.display = "none"
    })
    // 验证 password 结束

    //验证 password2 开始
    // 验证函数
    function valid_password2(){
        var psw = password.value
        var psw2 = password2.value
        // 验证 2 次密码是否一致
        if(psw != psw2){
            paswalign.style.display = "block"
            return false
        }
        // 特殊字符， 暂时不做验证
        // 验证成功，返回 true
         return true
    }
    // 丢失焦点， 开始验证
    password2.addEventListener('blur',valid_password2)

    // 获取焦点， 错误提示消失
    password2.addEventListener('focus',function(){
        // 取消所有的错误提示
        paswalign.style.display = "none"

    })
    // 验证password2 结束


    //验证 email 开始
    // 验证函数
    function valid_email(){
        var mail = email.value
        // 验证是否为空
        if(mail.replace('/\s+/g',"")==""){
            emailnull.style.display = "block"
            return false
        }
        // 验证 email 格式
        if(mail.indexOf("@")==-1){
            emailformat.style.display="block"
            return false
        }
        // 特殊字符， 暂时不做验证
        // 验证成功，返回 true
         return true
    }
    // 丢失焦点， 开始验证
    email.addEventListener('blur',valid_email)

    // 获取焦点， 错误提示消失
    email.addEventListener('focus',function(){
        // 取消所有的错误提示
        emailnull.style.display = "none"
        emailformat.style.display = "none"
    })
    // 验证 email 结束

    //验证 phonenumber 开始、
    // 验证函数
    function valid_phone(){
        var phone = phonenumber.value
        // 验证是否为空
        if(phone.replace('/\s+/g')==""){
            phonenull.style.display="block"
            return false
        }
        // 验证 phonenumber 格式

        // 特殊字符， 暂时不做验证
        // 验证成功，返回 true
         return true
    }
    // 丢失焦点， 开始验证
    phonenumber.addEventListener('blur',valid_phone)

    // 获取焦点， 错误提示消失
    phonenumber.addEventListener('focus',function(){
        // 取消所有的错误提示
        phonenull.style.display="none"
    })
    // 验证 phonenumber 结束

    // 验证 checkbox
    function valid_ckbox(){
        var ck = agreebox.checked
        // 验证是否被选中
        if(ck==false){
            checkagree.style.display="block"
            return false
        }
        return true
    }
    
    agreebox.addEventListener("focus",function () {
        checkagree.style.display = "none"
    })

    // 头像验证
    // 验证函数
    function valid_userimg(){
        var imgname = userimg.value

        if(imgname != null && imgname != ""){
            var suflist = imgname.split(".")
            var suf = suflist[suflist.length-1]
            if(suf.toUpperCase()=="JPG" || suf.toUpperCase()=="PNG"){
                usrimgp.innerText = imgname
                usrimgp.style.color="#4bad4b"
                return true
            }else{
                usrimgp.innerText = "格式不正确,请重新上传"
                usrimgp.style.color="red"
                return false
            }
        }
        return true
    }
    // 开始验证
    // 头像丢失焦点，显示头像文件名字
    userimg.addEventListener('change',valid_userimg)

    userimg.addEventListener("focus",function(){
        usrimgtype.style.display="none"
    })

    function submit_reg(){

        if(
            valid_username()
            &&valid_password()
            &&valid_password2()
            &&valid_email()
            &&valid_phone()
            &&valid_ckbox()
            &&valid_userimg()
        ){
            regform.submit()
            // alert("注册成功")
        }else{
            alert("请完善您的信息！")

        }

    }
    // 点击 注册 ， 提交表单并验证表单
    regbutton.addEventListener('click',submit_reg)

})