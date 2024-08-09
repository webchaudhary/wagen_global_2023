document.addEventListener("DOMContentLoaded", function (event) {

    const showNavbar = (toggleId, navId, bodyId, headerId, featuresBox, zoomBox) => {
        const toggle = document.getElementById(toggleId),
            nav = document.getElementById(navId),
            bodypd = document.getElementById(bodyId),
            box = document.getElementById(featuresBox),
            zoom = document.getElementsByClassName(zoomBox),
            headerpd = document.getElementById(headerId)

        // Validate that all variables exist
        if (toggle && nav && bodypd && headerpd && box) {
            toggle.addEventListener('click', () => {
                box.classList.toggle('box-pd')
                // console.log(box);
                zoom[0].classList.toggle('box-pd')
                // show navbar
                nav.classList.toggle('show')
                // change icon
                toggle.classList.toggle('bx-x')
                // add padding to body
                // bodypd.classList.toggle('body-pd')
                // add padding to header
                headerpd.classList.toggle('body-pd')


            })
        }
    }

    showNavbar('header-toggle', 'nav-bar', 'body-pd', 'header', 'featuresBox', 'ol-zoom')

    /*===== LINK ACTIVE =====*/
    // const linkColor = document.querySelectorAll('.nav_link')

    // function colorLink() {
    //     if (linkColor) {
    //         linkColor.forEach(l => l.classList.remove('active'))
    //         this.classList.add('active')
    //     }
    // }
    // linkColor.forEach(l => l.addEventListener('click', colorLink))

    // Your code to run since DOM is loaded and ready
});
// SIDE MENU JS ENDS---------------------------------------------------------------------------------------------------------------------------

$('.nav_link').on('click', function (e) {
    $(".nav_link").find('span').css('opacity', '0');
    // $('.boxes').toggleClass('box-nd');
    // $('.ol-zoom').toggleClass('box-nd');
    if ($(this).hasClass('active')) {
        $(".nav_link").find('span').css('opacity', '1');
        $('.container-fluid').removeClass('body-nd');
        $('header').removeClass('d-none');
        $('.submenu').removeClass('d-block');
        $(this).removeClass('active');
        $('.boxes').removeClass('box-nd');
        $('.ol-zoom').removeClass('box-nd');
    }
    else {
        $('.nav_link').removeClass('active');
        $('.container-fluid').addClass('body-nd');
        $(this).addClass('active');
        $('.submenu').removeClass('d-block');
        $(this).next('.submenu').addClass('d-block');
        $('header').addClass('d-none');
        $('.boxes').addClass('box-nd');
        $('.ol-zoom').addClass('box-nd');
    }
})

$('.closeBtn').on('click', function () {
    $('.nav_link.active').trigger('click');
})

$(document).ready(function(){
    $('#introModal').modal('show')
})






