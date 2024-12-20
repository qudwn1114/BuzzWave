const btn_submit = document.getElementById("btn-submit");

btn_submit.addEventListener("click", () => {
    btn_submit.disabled=true;
    document.getElementById('resetform').submit();
    return;
});