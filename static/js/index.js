$(document).ready(function(){
    $(".add-btn").click(function(){

        document.body.style.overflow = "hidden";

        var element = document.getElementsByClassName("display-form")[0];
        element.style.display = "block";

        const vh = Math.max(document.documentElement.clientHeight || 0, window.innerHeight || 0);
        element.style.height = vh+"px";

    });
    $(".close-btn").click(function(){
        document.body.style.overflow = "scroll";
        var element = document.getElementsByClassName("display-form")[0];
        element.style.display = "none";
    });
    $(".close-btn-1").click(function(){
        document.body.style.overflow = "scroll";
        var element = document.getElementsByClassName("display-form-1")[0];
        element.style.display = "none";
    });
    var height1 = document.querySelector('.counts').offsetHeight;
    var height2 = document.querySelector('.book').offsetHeight;
    var height3 = height2-height1;

    document.querySelector('.group').style.height = height3+"px";
});
function click_me(name, amount, id_no){
    document.body.style.overflow = "hidden";

    var element = document.getElementsByClassName("display-form-1")[0];
    element.style.display = "block";

    const vh = Math.max(document.documentElement.clientHeight || 0, window.innerHeight || 0);
    element.style.height = vh+"px";

    var customer_name = document.getElementById("customer-name-1");
    customer_name.value = name;

    var customer_amount = document.getElementById("amount-1");
    customer_amount.value = amount;

    var data_id =  document.getElementById("ID");
    data_id.value = id_no;
}
window.onscroll = function()
    {
    var btn = document.getElementsByClassName('add-btn')[0];
    
    if ( btn )
    {
        if ( document.body.scrollTop > 0 || document.documentElement.scrollTop > 0 )
        {
            btn.style.display = "none";
        }
        else
        {
            btn.style.display = "block";
        }
    }
}