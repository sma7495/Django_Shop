;(function($) {



    'use strict';

    var isMobile = {
        Android: function() {
            return navigator.userAgent.match(/Android/i);
        },
        BlackBerry: function() {
            return navigator.userAgent.match(/BlackBerry/i);
        },
        iOS: function() {
            return navigator.userAgent.match(/iPhone|iPad|iPod/i);
        },
        Opera: function() {
            return navigator.userAgent.match(/Opera Mini/i);
        },
        Windows: function() {
            return navigator.userAgent.match(/IEMobile/i);
        },
        any: function() {
            return (isMobile.Android() || isMobile.BlackBerry() || isMobile.iOS() || isMobile.Opera() || isMobile.Windows());
        }
    }; // is Mobile

    var responsiveMenu = function() {
        var menuType = 'desktop';

        $(window).on('resize', function() {
            var currMenuType = 'desktop';

            if (matchMedia('only screen and (max-width: 1200px)').matches) {
                currMenuType = 'mobile';
                console.log("done")
            }

            if (currMenuType !== menuType) {
                menuType = currMenuType;

                if (currMenuType === 'mobile') {
                    var $mobileMenu = $('#mainnav').attr('id', 'mainnav-mobi').hide();
                    var hasChildMenu = $('#mainnav-mobi').find('li:has(ul)');
                    var hasChildMenuMega = $('#mainnav-mobi').find('li:has(div.submenu)');

                    $('#header').after($mobileMenu);
                    hasChildMenu.children('ul').hide();
                    hasChildMenu.children('a').after('<span class="btn-submenu"></span>');
                    hasChildMenuMega.children('div.submenu').hide();
                    $('ul.submenu-child').hide();
                    hasChildMenuMega.find('h3').append('<span class="btn-submenu-child"></span>');
                    $('.btn-menu').removeClass('active');

                } else {
                    var $desktopMenu = $('#mainnav-mobi').attr('id', 'mainnav').removeAttr('style');
                    $desktopMenu.find('.submenu').removeAttr('style');
                    $('#header').find('.nav-wrap').append($desktopMenu);
                    $('.btn-submenu').remove();
                    $('ul.submenu-child').show();
                    $('h3').children('span').removeClass('btn-submenu-child');
                }
            }
        });


        $(document).ready(function (){
            var currMenuType = 'desktop';

            if (matchMedia('only screen and (max-width: 1200px)').matches) {
                currMenuType = 'mobile';
                console.log("done")
            }

            if (currMenuType !== menuType) {
                menuType = currMenuType;

                if (currMenuType === 'mobile') {
                    var $mobileMenu = $('#mainnav').attr('id', 'mainnav-mobi').hide();
                    var hasChildMenu = $('#mainnav-mobi').find('li:has(ul)');
                    var hasChildMenuMega = $('#mainnav-mobi').find('li:has(div.submenu)');

                    $('#header').after($mobileMenu);
                    hasChildMenu.children('ul').hide();
                    hasChildMenu.children('a').after('<span class="btn-submenu"></span>');
                    hasChildMenuMega.children('div.submenu').hide();
                    $('ul.submenu-child').hide();
                    hasChildMenuMega.find('h3').append('<span class="btn-submenu-child"></span>');
                    $('.btn-menu').removeClass('active');

                } else {
                    var $desktopMenu = $('#mainnav-mobi').attr('id', 'mainnav').removeAttr('style');
                    $desktopMenu.find('.submenu').removeAttr('style');
                    $('#header').find('.nav-wrap').append($desktopMenu);
                    $('.btn-submenu').remove();
                    $('ul.submenu-child').show();
                    $('h3').children('span').removeClass('btn-submenu-child');
                }
            }
        });
        $('.btn-menu').on('click', function() {
            $('#mainnav-mobi').slideToggle(300);
            $(this).toggleClass('active');
            return false;
        });

        $(document).on('click', '#mainnav-mobi li.has-mega-menu .row .btn-submenu-child', function(e) {
            $(this).toggleClass('active').parent('h3.cat-title').next('.submenu-child').slideToggle(400);
            e.stopImmediatePropagation();
            return false;
        });

        $(document).on('click', '#mainnav-mobi li .btn-submenu', function(e) {
            $(this).toggleClass('active').next('.submenu').slideToggle(400);
            e.stopImmediatePropagation();
            return false;
        });

    }; // Responsive Menu

    var responsiveMenuMega_S2 = function() {
        var menuType = 'desktop';

        $(window).on('resize', function() {
            var currMenuType = 'desktop';

            if (matchMedia('only screen and (max-width: 1200px)').matches) {
                currMenuType = 'mobile';
            }

            if (currMenuType !== menuType) {
                menuType = currMenuType;

                if ($('body').hasClass('grid')) {
                    if (currMenuType === 'mobile') {
                        var $mobileMenuMegaV2 = $('#mega-menu').attr('id', 'mega-mobile').hide();
                        var ChildMenuMegaV2 = $('.header-bottom').find('.grid-right');
                        var ChildDropmenuV2 = $('.drop-menu').children('.one-third');

                        $('.btn-mega').hide();
                        $('#header').after($mobileMenuMegaV2);
                        ChildMenuMegaV2.append('<div class="btn-menu-mega"><span></span></div>');

                        $('.drop-menu').hide();
                        $mobileMenuMegaV2.find('.dropdown').append('<span class="btn-dropdown"></span>');

                        ChildDropmenuV2.children('ul').hide();
                        $('.drop-menu').find('.cat-title').append('<span class="btn-dropdown-child"></span>');

                    } else {
                        var $desktopMenuMegaV2 = $('#mega-mobile').attr('id', 'mega-menu').removeAttr('style');

                        $desktopMenuMegaV2.find('.drop-menu').removeAttr('style');
                        $('.header-bottom.style1').find('.grid-left').append($desktopMenuMegaV2);
                    }
                }
            }
        });
        $(document).ready(function (){
            var currMenuType = 'desktop';

            if (matchMedia('only screen and (max-width: 1200px)').matches) {
                currMenuType = 'mobile';
            }

            if (currMenuType !== menuType) {
                menuType = currMenuType;

                if ($('body').hasClass('grid')) {
                    if (currMenuType === 'mobile') {
                        var $mobileMenuMegaV2 = $('#mega-menu').attr('id', 'mega-mobile').hide();
                        var ChildMenuMegaV2 = $('.header-bottom').find('.grid-right');
                        var ChildDropmenuV2 = $('.drop-menu').children('.one-third');

                        $('.btn-mega').hide();
                        $('#header').after($mobileMenuMegaV2);
                        ChildMenuMegaV2.append('<div class="btn-menu-mega"><span></span></div>');

                        $('.drop-menu').hide();
                        $mobileMenuMegaV2.find('.dropdown').append('<span class="btn-dropdown"></span>');

                        ChildDropmenuV2.children('ul').hide();
                        $('.drop-menu').find('.cat-title').append('<span class="btn-dropdown-child"></span>');

                    } else {
                        var $desktopMenuMegaV2 = $('#mega-mobile').attr('id', 'mega-menu').removeAttr('style');

                        $desktopMenuMegaV2.find('.drop-menu').removeAttr('style');
                        $('.header-bottom.style1').find('.grid-left').append($desktopMenuMegaV2);
                    }
                }
            }
        });


        $(document).on('click', '#mega-mobile ul.menu li a .btn-dropdown', function(e) {
            $(this).toggleClass('active').closest('li').children('.drop-menu').slideToggle(400);
            e.stopImmediatePropagation();
            return false;
        });

        $(document).on('click', '#mega-mobile .btn-dropdown-child', function(e) {
            $(this).toggleClass('active').closest('.one-third').children('ul').slideToggle(400);
            e.stopImmediatePropagation();
            return false;
        });

    }; // Responsive Menu Mega S2

    var responsiveMenuMega = function() {
        var menuType = 'desktop';

        $(window).on('resize', function() {
            var currMenuType = 'desktop';

            if (matchMedia('only screen and (max-width: 1200px)').matches) {
                currMenuType = 'mobile';
            }

            if (currMenuType !== menuType) {
                menuType = currMenuType;

                if (currMenuType === 'mobile') {
                    var $mobileMenuMega = $('#mega-menu').attr('id', 'mega-mobile').hide();
                    var ChildMenuMega = $('.header-bottom').find('.col-2');
                    var ChildDropmenu = $('.drop-menu').children('.one-third');

                    $('.btn-mega').hide();
                    $('#header').after($mobileMenuMega);
                    ChildMenuMega.append('<div class="btn-menu-mega"><span></span></div>');

                    $('.drop-menu').hide();
                    $mobileMenuMega.find('.dropdown').append('<span class="btn-dropdown"></span>');

                    ChildDropmenu.children('ul').hide();
                    $('.drop-menu').find('.cat-title').append('<span class="btn-dropdown-child"></span>');

                } else {
                    var $desktopMenuMega = $('#mega-mobile').attr('id', 'mega-menu').removeAttr('style');

                    $('.btn-mega').show();
                    $desktopMenuMega.find('.drop-menu').removeAttr('style');
                    $('.header-bottom').find('.col-2').append($desktopMenuMega);
                    $('.btn-menu-mega').remove();
                    $('.btn-dropdown-child').remove();
                    $('.drop-menu').children('.one-third').children('ul').show();
                }
            }
        });
        $(document).ready(function (){

            var currMenuType = 'desktop';

            if (matchMedia('only screen and (max-width: 1200px)').matches) {
                currMenuType = 'mobile';
            }

            if (currMenuType !== menuType) {
                menuType = currMenuType;

                if (currMenuType === 'mobile') {
                    var $mobileMenuMega = $('#mega-menu').attr('id', 'mega-mobile').hide();
                    var ChildMenuMega = $('.header-bottom').find('.col-2');
                    var ChildDropmenu = $('.drop-menu').children('.one-third');

                    $('.btn-mega').hide();
                    $('#header').after($mobileMenuMega);
                    ChildMenuMega.append('<div class="btn-menu-mega"><span></span></div>');

                    $('.drop-menu').hide();
                    $mobileMenuMega.find('.dropdown').append('<span class="btn-dropdown"></span>');

                    ChildDropmenu.children('ul').hide();
                    $('.drop-menu').find('.cat-title').append('<span class="btn-dropdown-child"></span>');

                } else {
                    var $desktopMenuMega = $('#mega-mobile').attr('id', 'mega-menu').removeAttr('style');

                    $('.btn-mega').show();
                    $desktopMenuMega.find('.drop-menu').removeAttr('style');
                    $('.header-bottom').find('.col-2').append($desktopMenuMega);
                    $('.btn-menu-mega').remove();
                    $('.btn-dropdown-child').remove();
                    $('.drop-menu').children('.one-third').children('ul').show();
                }
            }

        });
        $(document).on('click', '.btn-menu-mega', function() {
            $('#mega-mobile').slideToggle(300);
            $(this).toggleClass('active');
            return false;
        });

        $(document).on('click', '#mega-mobile ul.menu li a .btn-dropdown', function(e) {
            $(this).toggleClass('active').closest('li').children('.drop-menu').slideToggle(400);
            e.stopImmediatePropagation();
            return false;
        });

        $(document).on('click', '#mega-mobile .btn-dropdown-child', function(e) {
            $(this).toggleClass('active').closest('.one-third').children('ul').slideToggle(400);
            e.stopImmediatePropagation();
            return false;
        });

    }; // Responsive Menu Mega

    var searchButton = function() {
        var showsearch = $('.show-search button');
        showsearch.on('click', function() {
            $('.show-search').parent('div').children('.top-search.style1').toggleClass('active');
            showsearch.toggleClass('active');
        });
    }; // Show Search

    // Dom Ready

    $(function() {
        responsiveMenu();
        responsiveMenuMega_S2();
        responsiveMenuMega();
        searchButton();
    });

})(jQuery);




$(document).ready(function(){
    $('#cities-map svg g path').hover(function() {
        var className = $(this).attr('class');// tabriz
        var parrentClassName = $(this).parent('g').attr('class');// province
        var itemName = $('#cities-map .list .' + parrentClassName + ' .' + className + ' a').html();// تبریز
        //console.log(itemName);
        if (itemName) {
            $('#cities-map .list .' + parrentClassName + ' .' + className + ' a').addClass('hover');// رنگ تگ a عوض میشه
        }
    }, function() {
        $('#cities-map .list a').removeClass('hover');
    });

    $('#cities-map .list ul li ul li a').hover(function() {
        var className = $(this).parent('li').attr('class');// tabriz
        var parrentClassName = $(this).parent('li').parent('ul').parent('li').attr('class');// province
        var object = '#cities-map svg g.' + parrentClassName + ' path.' + className;// <path class="tabriz">
        var currentClass = $(object).attr('class');// class="tabriz"
        $(object).attr('class', currentClass + ' hover');// class="tabriz hover"
    }, function() {
        var className = $(this).parent('li').attr('class');// tabriz

        var parrentClassName = $(this).parent('li').parent('ul').parent('li').attr('class');
        var object = '#cities-map svg g.' + parrentClassName + ' path.' + className;
        var currentClass = $(object).attr('class');
        $(object).attr('class', currentClass.replace(' hover', ''));
    });

    $("#cities-map .list ul li ul li a").click(function(e) {
        e.preventDefault();
        var city = $(this).text();// تبریز
        console.log(city);
        var cityEnglish = $(this).parent().attr("class");// tabriz
        $("#cities-map .list ul li ul li a").removeClass("active");// هر چی کلاس اکتیو هستش حذف میشه
        $("#cities-map path").removeClass("active");// هر چی کلاس اکتیو هستش حذف میشه
        $(this).addClass("active");// به اون موردی که کلیک شده کلاس اکتیو اضافه میشه
        $("#cities-map path[class='" + cityEnglish + "']").addClass("active");// به تگ پث هم کلاس اکتیو اضافه میشه
        $("#cities-map path[class='" + cityEnglish + " hover']").addClass("active");
        $("#btn-cities span").text(city);// به تگ اسپن محتوای متنی که کلیک شده اضافه میشه
        $('.modal.in').modal('hide');
    });

    $("#cities-map svg g path").click(function() {
        var className = $(this).attr("class");
        $("#cities-map a[href='#" + className + "']").trigger("click");
    });
});







window.addEventListener('scroll', function() {
    if (window.scrollY > 118) {

       const header_bottom= document.querySelector(".header-bottom");
       const mega_mobile=document.getElementById('mega-mobile');
       const mainnav_mobi=document.getElementById('mainnav-mobi');
        header_bottom.style.position = 'fixed';
        header_bottom.style.top = '0';
        header_bottom.style.right = '0';
        header_bottom.style.width='100%';
        mega_mobile.style.position = 'fixed';
        mega_mobile.style.top = '36px';
        mega_mobile.style.right = '0';
        mainnav_mobi.style.position = 'fixed';
        mainnav_mobi.style.top = '36px';
        mainnav_mobi.style.right = '0';

    }



});
let previousScrollPosition = window.scrollY;

window.addEventListener('scroll', () => {
    const currentScrollPosition = window.scrollY;
    const header_bottom= document.querySelector(".header-bottom");
    const mega_mobile=document.getElementById('mega-mobile');
    const mainnav_mobi=document.getElementById('mainnav-mobi');
    if (window.scrollY < 118){
    if (currentScrollPosition < previousScrollPosition) {

        if (currentScrollPosition <= 118) {

            header_bottom.style.position = 'relative';
            mega_mobile.style.position = 'absolute';
            mainnav_mobi.style.position = 'absolute';
            mega_mobile.style.top = 'inherit';
            mega_mobile.style.left = '0';
            mainnav_mobi.style.left = '0';
            mainnav_mobi.style.top = 'inherit';
            }
        }
    }
    previousScrollPosition = currentScrollPosition;
});



function increaseCount(a, b) {
    var input = b.nextElementSibling;
    var value = parseInt(input.value, 10);
    value = isNaN(value) ? 0 : value;
    value++;
    input.value = value;
}

function decreaseCount(a, b) {
    var input = b.previousElementSibling;
    var value = parseInt(input.value, 10);
    if (value > 1) {
        value = isNaN(value) ? 0 : value;
        value--;
        input.value = value;
    }
}




const story_other_prd = new Swiper(".modal-body .story-other-prd", {
    slidesPerView: 1,
    spaceBetween: 20,
    freeMode: true,
});





const st_slider = new Swiper('.swiper.st_slider', {
    // Optional parameters
    effect: "cube",
    grabCursor: true,
    loop:true,
    cubeEffect: {
        shadow: true,
        slideShadows: true,
        shadowOffset: 20,
        shadowScale: 0.94,

    },
    autoplay: {
        delay: 2500,
        disableOnInteraction: false,
        slideShadows:true
    },
    // If we need pagination



});


const st_slider2 = new Swiper('.swiper.st_slider2', {
    loop:true,
    direction: 'horizontal',
    slidesPerView: 5,
    spaceBetween: 15,

    // If we need pagination


    // Navigation arrows
    navigation: {
        nextEl: '.swiper-button-next',
        prevEl: '.swiper-button-prev',
    },
    breakpoints: {
        // when window width is >= 320px
        320: {
            slidesPerView: 2,
            spaceBetween: 10,
        },

        // when window width is >= 480px
        480: {
            slidesPerView: 3,
            spaceBetween: 10,
        },
        // when window width is >= 640px
        640: {
            slidesPerView: 6,
            spaceBetween: 10,
        }
    }

});

const swiper = new Swiper(".swiper.main_slider", {
    loop: true,
    autoplay: {
        delay: 2500,
        disableOnInteraction: false,
        slideShadows:true
    },
    breakpoints: {
        320: {
            slidesPerView: 1.1,
            centeredSlides: true,
            spaceBetween: 10,
        },

        480: {
            slidesPerView: "auto",
            spaceBetween: 20,
        },
    },
    navigation: {
        nextEl: ".swiper-button-next",
        prevEl: ".swiper-button-prev",
    },
    pagination: {
        el: ".swiper-pagination",
        clickable: true,
    },


});

const brand = new Swiper(".brand", {
    slidesPerView: 7,
    spaceBetween: 15,
    freeMode: true,
    pagination: {
        el: ".swiper-pagination",
        clickable: true,
    },
    breakpoints: {
        // when window width is >= 320px
        320: {
            slidesPerView: 3,
            spaceBetween: 5,
        },
        // when window width is >= 480px
        480: {
            slidesPerView: 4,
            spaceBetween: 5,
        },
        // when window width is >= 640px
        640: {
            slidesPerView: 4,
            spaceBetween: 15,
        },
        768: {
            slidesPerView: 5,
            spaceBetween: 15,
        },
        1000: {
            slidesPerView: 7,
            spaceBetween: 15,
        },
    }
});

const storys = new Swiper(".storys", {
    slidesPerView: 12,

    freeMode: true,
    pagination: {
        el: ".swiper-pagination",
        clickable: true,
    },
    breakpoints: {
        // when window width is >= 320px
        320: {
            slidesPerView: 3,
            spaceBetween:0,
        },
        390: {
            slidesPerView: 4,

        },
        // when window width is >= 480px
        480: {
            slidesPerView: 5,

        },
        // when window width is >= 640px

        768: {
            slidesPerView: 7,

        },
        1000: {
            slidesPerView: 9,

        },
        1200: {
            slidesPerView: 12,

        },
        1500: {
            slidesPerView: 13,

        },
    }
});

allPrice=document.querySelectorAll(".price")
allPrice.forEach(function (price){
    if(price.innerText!=" "){
        price.textContent+=" تومان"
    }
})



/*----------timer--------*/

let timeToStart = document.querySelector('#timeToStart');
let timeControl = document.querySelector('#timeControl');
let second = 1000;
let minute = second * 60;
let hour = minute * 60;
let day = hour * 24;

// اون تاریخی که قراره بهش برسیم
let countDown = new Date('dec 20, 2025 00:00:00').getTime();

const convertToPersianNumbers = (num) => {
    const persianDigits = ['۰', '۱', '۲', '۳', '۴', '۵', '۶', '۷', '۸', '۹'];
    return num.toString().replace(/[0-9]/g, (d) => persianDigits[d]);
};

const myRacing = () => {
    let nowDate = new Date().getTime(),
        distance = countDown - nowDate;

    document.getElementById('days').innerText = convertToPersianNumbers(Math.floor(distance / day));
    document.getElementById('hours').innerText = convertToPersianNumbers(Math.floor((distance % day) / hour));
    document.getElementById('minutes').innerText = convertToPersianNumbers(Math.floor((distance % hour) / minute));
    document.getElementById('seconds').innerText = convertToPersianNumbers(Math.floor((distance % minute) / second));

    // وقتی تاریخ و زمان گذشته بود
    if (distance < 0) {
        clearInterval(MyTimer);
        timeToStart.innerHTML = 'جشنواره شروع شد ☻';
        timeControl.innerHTML = 'مهلت تخفیف به پایان رسید!';
    }
};

MyTimer = setInterval(myRacing, 1000);


let timeToStart2 = document.querySelector('#timeToStart');
let timeControl2 = document.querySelector('#timeControl');
let second2 = 1000;
let minute2 = second2 * 60;
let hour2 = minute2 * 60;
let day2 = hour2 * 24;

// تاریخ هدف
let countDown2 = new Date('dec 24, 2025 00:00:00').getTime();



const myRacing2 = () => {
    let nowDate2 = new Date().getTime();
    let distance2 = countDown2 - nowDate2;

    document.getElementById('days2').innerText = toPersianNumber(Math.floor(distance2 / day2));
    document.getElementById('hours2').innerText = toPersianNumber(Math.floor((distance2 % day2) / hour2));
    document.getElementById('minutes2').innerText = toPersianNumber(Math.floor((distance2 % hour2) / minute2));
    document.getElementById('seconds2').innerText = toPersianNumber(Math.floor((distance2 % minute2) / second2));

    // زمانی که تاریخ به پایان رسیده است
    if (distance2 < 0) {
        clearInterval(MyTimer2);
        timeToStart2.innerHTML = 'کمپ آغاز شد ☻';
        timeControl2.innerHTML = 'مهلت تخفیف به پایان رسید!';
    }
};

let MyTimer2 = setInterval(myRacing2, 1000);


let timeToStart3 = document.querySelector('#timeToStart')
let timeControl3 = document.querySelector('#timeControl')
let second3 = 1000
let minute3 = second3 * 60
let hour3 = minute3 * 60
let day3 = hour3 * 24

// اون تاریخی که قراره بهش برسیم
let countDown3 = new Date('dec 29, 2025 00:00:00').getTime();
const myRacing3 = () => {

    let nowDate3 = new Date().getTime(),
        distance3 = countDown3 - nowDate3;
    //
    document.getElementById('days3').innerText = toPersianNumber(Math.floor(distance3 / day3));
    document.getElementById('hours3').innerText = toPersianNumber(Math.floor((distance3 % day3) / hour3));
    document.getElementById('minutes3').innerText = toPersianNumber(Math.floor((distance3 % hour3) / minute3));
    document.getElementById('seconds3').innerText = toPersianNumber(Math.floor((distance3 % minute3) / second3));

    // وقتی تاریخ و زمان گذشته بود
    if (distance3 < 0) {
        clearInterval(MyTimer3);
        timeToStart3.innerHTML = 'The camp began ☻'
        timeControl3.innerHTML = 'مهلت تخفیف به پایان رسید!'
    }

}
MyTimer3 = setInterval(myRacing3, 1000);



let timeToStart4 = document.querySelector('#timeToStart')
let timeControl4 = document.querySelector('#timeControl')
let second4 = 1000
let minute4 = second4 * 60
let hour4 = minute4 * 60
let day4 = hour4 * 24

// اون تاریخی که قراره بهش برسیم
let countDown4 = new Date('dec 26, 2025 00:00:00').getTime();
const myRacing4 = () => {

    let nowDate4 = new Date().getTime(),
        distance4 = countDown4 - nowDate4;
    //
    document.getElementById('days4').innerText = toPersianNumber(Math.floor(distance4 / day4));
    document.getElementById('hours4').innerText = toPersianNumber(Math.floor((distance4 % day4) / hour4));
    document.getElementById('minutes4').innerText = toPersianNumber(Math.floor((distance4 % hour4) / minute4));
    document.getElementById('seconds4').innerText = toPersianNumber(Math.floor((distance4 % minute4) / second4));

    // وقتی تاریخ و زمان گذشته بود
    if (distance4 < 0) {
        clearInterval(MyTimer4);
        timeToStart4.innerHTML = 'The camp began ☻'
        timeControl4.innerHTML = 'مهلت تخفیف به پایان رسید!'
    }

}
MyTimer4 = setInterval(myRacing4, 1000);



let timeToStart5 = document.querySelector('#timeToStart')
let timeControl5 = document.querySelector('#timeControl')
let second5 = 1000
let minute5 = second5 * 60
let hour5 = minute5 * 60
let day5 = hour5 * 24

// اون تاریخی که قراره بهش برسیم
let countDown5 = new Date('dec 27, 2025 00:00:00').getTime();
const myRacing5 = () => {

    let nowDate5 = new Date().getTime(),
        distance5 = countDown5 - nowDate5;
    //
    document.getElementById('days5').innerText = toPersianNumber(Math.floor(distance5 / day5));
    document.getElementById('hours5').innerText = toPersianNumber(Math.floor((distance5 % day5) / hour5));
    document.getElementById('minutes5').innerText = toPersianNumber(Math.floor((distance5 % hour5) / minute5));
    document.getElementById('seconds5').innerText = toPersianNumber(Math.floor((distance5 % minute5) / second5));

    // وقتی تاریخ و زمان گذشته بود
    if (distance5 < 0) {
        clearInterval(MyTimer5);
        timeToStart5.innerHTML = 'The camp began ☻'
        timeControl5.innerHTML = 'مهلت تخفیف به پایان رسید!'
    }

}
MyTimer5 = setInterval(myRacing5, 1000);


let timeToStart6 = document.querySelector('#timeToStart')
let timeControl6 = document.querySelector('#timeControl')
let second6 = 1000
let minute6 = second6 * 60
let hour6 = minute6 * 60
let day6 = hour6 * 24

// اون تاریخی که قراره بهش برسیم
let countDown6 = new Date('dec 27, 2025 00:00:00').getTime();
const myRacing6 = () => {

    let nowDate6 = new Date().getTime(),
        distance6 = countDown6 - nowDate6;
    //
    document.getElementById('days6').innerText = toPersianNumber(Math.floor(distance6 / day6));
    document.getElementById('hours6').innerText = toPersianNumber(Math.floor((distance6 % day6) / hour6));
    document.getElementById('minutes6').innerText = toPersianNumber(Math.floor((distance6 % hour6) / minute6));
    document.getElementById('seconds6').innerText = toPersianNumber(Math.floor((distance6 % minute6) / second6));

    // وقتی تاریخ و زمان گذشته بود
    if (distance6 < 0) {
        clearInterval(MyTimer6);
        timeToStart6.innerHTML = 'The camp began ☻'
        timeControl6.innerHTML = 'مهلت تخفیف به پایان رسید!'
    }

}
MyTimer6 = setInterval(myRacing6, 1000);

let timeToStart7 = document.querySelector('#timeToStart')
let timeControl7 = document.querySelector('#timeControl')
let second7 = 1000
let minute7 = second7 * 60
let hour7 = minute7 * 60
let day7 = hour7 * 24

// اون تاریخی که قراره بهش برسیم
let countDown7 = new Date('dec 27, 2025 00:00:00').getTime();
const myRacing7 = () => {

    let nowDate7 = new Date().getTime(),
        distance7 = countDown7 - nowDate7;
    //
    document.getElementById('days7').innerText = toPersianNumber(Math.floor(distance7 / day7));
    document.getElementById('hours7').innerText = toPersianNumber(Math.floor((distance7 % day7) / hour7));
    document.getElementById('minutes7').innerText = toPersianNumber(Math.floor((distance7 % hour7) / minute7));
    document.getElementById('seconds7').innerText = toPersianNumber(Math.floor((distance7 % minute7) / second7));

    // وقتی تاریخ و زمان گذشته بود
    if (distance7 < 0) {
        clearInterval(MyTimer7);
        timeToStart7.innerHTML = 'The camp began ☻'
        timeControl7.innerHTML = 'مهلت تخفیف به پایان رسید!'
    }

}
MyTimer7 = setInterval(myRacing7, 1000);




/*----------changer--------*/

var special_sells_thumbs = new Swiper(".special-sells-thumbs", {

    loop: true,
    spaceBetween: 10,
    direction: 'horizontal',
    slidesPerView: 3,
    freeMode: true,
    watchSlidesProgress: true,
    breakpoints: {
        320: {
            direction: 'horizontal',
            slidesPerView: 5,
            spaceBetween: 10,
        },
        768: {
            slidesPerView: 3,
            direction: 'vertical',
            spaceBetween: 10,
        },
    }

});

var special_sells = new Swiper(".special-sells", {
    loop: true,
    spaceBetween: 10,
    thumbs: {
        swiper: special_sells_thumbs,
    },

    autoplay: {
        delay: 2500,
        disableOnInteraction: false
    },

});






/*----------instant_offer--------*/

const progressCircle = document.querySelector(".autoplay-progress svg");
const progressContent = document.querySelector(".autoplay-progress span");
const instant_offer = new Swiper(".instant-offer", {
    spaceBetween: 30,
    centeredSlides: true,

    autoplay: {
        delay: 2500,
        disableOnInteraction: false
    },
    pagination: {
        el: ".swiper-pagination",
        clickable: true
    },
    navigation: {
        nextEl: ".swiper-button-next",
        prevEl: ".swiper-button-prev"
    },
    allowTouchMove: false,

    on: {
        autoplayTimeLeft(s, time, progress) {
            progressCircle.style.setProperty("--progress", 1 - progress);
            progressContent.textContent = `${Math.ceil(time / 1000)}s`;

        }

    }



});

/*----------end-instant_offer--------*/



/*----------recent_offer--------*/

const recent_offer = new Swiper('.recent-offer', {
    slidesPerView: 3,
    grid: {
        rows: 3,
        fill: 5,
    },
    spaceBetween: 30,
    pagination: {
        el: ".swiper-pagination",
        clickable: true,
    },

    breakpoints: {
        320: {
            slidesPerView: 1,
            spaceBetween: 5,
            grid: {
                rows: 3,
                fill: 3,
            },
        },
        768: {
            slidesPerView: 2,
            spaceBetween: 10,
            grid: {
                rows: 3,
                fill: 4,
            },
        },
        1000: {
            slidesPerView: 2,
            spaceBetween: 15,
            grid: {
                rows: 3,
                fill: 4,
            },
        },
        1200: {
            slidesPerView: 3,
            spaceBetween: 15,
            grid: {
                rows: 3,
                fill: 5,
            },
        },

    }
});


/*----------end-recent_offer--------*/




const offer_number=document.querySelectorAll(".offer-prd  h3")
const offer_prd=document.querySelectorAll(".offer-prd")
for (let i=0; i<offer_prd.length;i++){
    offer_number[i].innerText=i+1;
}

let currentTab = 0; // شاخص تب فعلی
const tabs = document.querySelectorAll('.cycle-tab-item');
const tabContents = document.querySelectorAll('.tab-pane'); 

// تابع برای نمایش تب جدید
function showTab(index) {
    tabs.forEach((tab, i) => {
        if (i === index) {
            tab.classList.add('active');
            tabContents[i].classList.add('active', 'in');
        } else {
            tab.classList.remove('active'); //
            tabContents[i].classList.remove('active', 'in');
        }
    });
}

// تابع برای چرخش تب‌ها
function cycleTabs() {
    showTab(currentTab);
    currentTab = (currentTab + 1) % tabs.length;
    setTimeout(cycleTabs, 10000);

}


function handleTabClick(index) {
    currentTab = index;
    showTab(currentTab);
}


document.addEventListener('DOMContentLoaded', () => {
    cycleTabs();


    tabs.forEach((tab, index) => {
        tab.addEventListener('click', () => {
            handleTabClick(index); //
        });
    });
});

let menuToggle = document.querySelector('.menuToggle');
menuToggle.onclick = function () {
    menuToggle.classList.toggle('open');
}




document.addEventListener('DOMContentLoaded', () => {
        video.pause();
        video.currentTime = 0;

});


const container = document.getElementById('story-slider'),
    sliders = document.querySelectorAll('[data-video]');

sliders.forEach(item => {
    item.addEventListener('click', () => container.src = item.dataset.video);
});




function footerToggle(footerBtn) {
    $(footerBtn).toggleClass("btnActive");
    $(footerBtn).next().toggleClass("active");
}



const story_img =document.querySelectorAll(".swiper-img")
const video = document.querySelector(".story-videos-box video");
const backdrop = document.querySelector(".modal");

story_img.forEach(function (item){
    item.addEventListener("click" ,function (){
        video.currentTime = 0;
        video.autoplay = true;
        video.load();
    })
})

backdrop.addEventListener('hidden.bs.modal', function (){
    video.pause();
    video.currentTime = 0;
})





/*-------------to-persian-numbr---------*/


function toPersianNumber(num) {
    const persianDigits = ['۰', '۱', '۲', '۳', '۴', '۵', '۶', '۷', '۸', '۹'];
    return num.toString().replace(/\d/g, (d) => persianDigits[d]);
}

function convertAllNumbersToPersian() {
    // جستجو در تمامی عناصر صفحه
    const elements = document.body.getElementsByTagName('*');

    for (let i = 0; i < elements.length; i++) {
        const element = elements[i];
        // بررسی اینکه آیا عنصر متنی است
        if (element.childNodes.length > 0) {
            for (let j = 0; j < element.childNodes.length; j++) {
                const node = element.childNodes[j];
                // اگر نود متنی باشد
                if (node.nodeType === Node.TEXT_NODE) {
                    const text = node.nodeValue.trim();
                    // استفاده از regex برای پیدا کردن اعداد
                    if (/\d/.test(text)) {
                        const convertedText = toPersianNumber(text);
                        node.nodeValue = convertedText; // تغییر متن به شماره فارس
                    }
                }
            }
        }
    }
}


window.onload = convertAllNumbersToPersian;




window.addEventListener('scroll', function() {
    const toTopButton = document.querySelector('.to-top-btn');
    if (window.scrollY >= 300) {
        toTopButton.style.display = 'flex';
    } else {
        toTopButton.style.display = 'none';
        toTopButton.style.animation = 'up 500ms linear';
    }
});


