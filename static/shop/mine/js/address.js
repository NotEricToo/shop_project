$(document).ready(function () {

    // input form
    var adsname = document.getElementById("adsname")        // 地址命名
    var adsdetail = document.getElementById("adsdetail")    // 地址详情
    var adsrecname = document.getElementById("adsrecname")  // 收货人姓名
    var adsmphone = document.getElementById("adsmphone")    // 收货人电话
    var confirmbtn = document.getElementById("confirmbtn")  // 确认按钮
    var addressform = document.getElementById("addressform") // form 表单
    var addressid = document.getElementById("addressid") // 隐藏 address id

    // validate info
    var addressnamenull = document.getElementById("addressnamenull")    // 地址命名为空
    var addressnull = document.getElementById("addressnull")            // 地址详情为空
    var receivenamenull = document.getElementById("receivenamenull")    // 收货人姓名为空
    var phonenull = document.getElementById("phonenull")                // 收货电话为空

    // adsname
    // 地址命名  验证函数：
    function validate_adsname() {
        namevalue = adsname.value

        if(namevalue.replace("/\s+/g","") == ""){
            addressnamenull.style.display = "block"
            return false
        }
        return true
    }

    // 地址详情 验证函数
    function validate_aadsdetail(){
        adsvalue = adsdetail.value

        if(adsvalue.replace("/\s+/g","") == ""){
            addressnull.style.display = "block"
            return false
        }
        return true
    }

    // 收货人姓名 验证函数
    function validate_adsrecname(){
        adsrecvalue = adsrecname.value

        if(adsrecvalue.replace("/\s+/g","") == ""){
            receivenamenull.style.display = "block"
            return false
        }
        return true
    }

    // 收货人手机号码 验证函数
    function validate_adsmphone(){
        adsmvalue = adsmphone.value

        if(adsmvalue.replace("/\s+/g","") == ""){
            phonenull.style.display = "block"
            return false
        }
        return true
    }

    // 地址命名 验证开始
    adsname.addEventListener("blur",validate_adsname)
    adsname.addEventListener("focus",function () {
        addressnamenull.style.display = "none"
    })

    // 地址详情
    adsdetail.addEventListener("blur",validate_aadsdetail)
    adsdetail.addEventListener("focus",function () {
        addressnull.style.display = "none"
    })

    // 收货人姓名
    adsrecname.addEventListener("blur",validate_adsrecname)
    adsrecname.addEventListener("focus",function () {
        receivenamenull.style.display = "none"
    })

    // 收货人手机号码
    adsmphone.addEventListener("blur",validate_adsmphone)
    adsmphone.addEventListener("focus",function () {
        phonenull.style.display = "none"
    })

    confirmbtn.addEventListener("click",function () {
        if(
            validate_adsname()
            &&validate_aadsdetail()
            &&validate_adsrecname()
            &&validate_adsmphone()
        ){
            if(addressid.value.replace("/\s+/g","") == "" ){
                addressid.value = 0
            }
            addressform.submit()
            // alert("表单提交成功")
        }
    })
})