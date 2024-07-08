document.addEventListener("DOMContentLoaded", function(event) {
    var trigger = $('.hamburger'), isClosed = false;
    const showNavbar = (toggleId, navId, bodyId) =>{
        const toggle = document.getElementById(toggleId),
        nav = document.getElementById(navId),
        bodypd = document.getElementById(bodyId)
        //headerpd = document.getElementById(headerId)

        // Validate that all variables exist
        if(toggle && nav && bodypd ){
            toggle.addEventListener('click', ()=>{
                hamburger_cross();
                // show navbar
                nav.classList.toggle('side_bar_show')
                // change icon
                toggle.classList.toggle('bx-x')
                // add padding to body
                bodypd.classList.toggle('body-pd')
                // add padding to mapbar
                // mapbarpd.classList.toggle('mapbar-pd')
                // add padding to header
                //headerpd.classList.toggle('header-body-pd')
            })
        }
    }

    showNavbar('header-toggle','nav-bar','body-pd')

    function hamburger_cross() {

        if (isClosed == true) {          
          trigger.removeClass('is-open');
          trigger.addClass('is-closed');
          isClosed = false;
        } else {   
          trigger.removeClass('is-closed');
          trigger.addClass('is-open');
          isClosed = true;
        }
    }

    /*===== LINK ACTIVE =====*/
    const linkColor = document.querySelectorAll('.nav_link')

    function colorLink(){
        if(linkColor){
            linkColor.forEach(l=> l.classList.remove('active'))
            this.classList.add('active')
        }
    }
    linkColor.forEach(l=> l.addEventListener('click', colorLink))

    // Your code to run since DOM is loaded and ready
});