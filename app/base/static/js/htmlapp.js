(function () {


    // $('.burger-menu:first-child').on('click', function(e) {
    //     e.preventDefault();
    //     $('body').toggleClass('toggle-sidebar');
    // })

    document.querySelector('.burger-menu:first-child').addEventListener("click", (e) => {
        e.preventDefault();
        const $body = document.querySelector('body');
        $body.classList.toggle('toggle-sidebar');
    });



})();