let menu = document.getElementById("dropdown-toggle")
menu.addEventListener("click", function(){
    let menu_toggle = document.getElementById("dropdown-menu")
    if (menu_toggle.classList.contains("active")){
        menu_toggle.classList.remove("active")
    }else{
        menu_toggle.classList.add("active")
    }
})
