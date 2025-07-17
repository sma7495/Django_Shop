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
        showsearch.on('click',function() {
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






allPrice=document.querySelectorAll(".price")
allPrice.forEach(function (price){
    if(price.innerText!=" "){
        price.textContent+=" تومان"
    }
});



function footerToggle(footerBtn) {
    $(footerBtn).toggleClass("btnActive");
    $(footerBtn).next().toggleClass("active");
}



/*-------------product-detail---------*/


console.log("done")

var gallery_thumbs = new Swiper(".gallery-thumbs", {
    loop: true,
    spaceBetween: 10,
    slidesPerView: 5,
    freeMode: true,
    watchSlidesProgress: true,
});
var gallery = new Swiper(".gallery", {
    loop: true,
    spaceBetween: 10,
    thumbs: {
        swiper: gallery_thumbs,
    },
});

function selectCircle(selected, color) {
    const circles = document.querySelectorAll('.rounded-circle');
    circles.forEach(circles => {
        circles.classList.remove('selected');
    });
    selected.classList.add('selected');

    // نمایش رنگ انتخاب شده
    let colorText;
    switch (color) {
        case 'خاکستری':
            colorText = ' خاکستری';
            break;
        case 'زرد':
            colorText = ' زرد ';
            break;
        case 'بنفش':
            colorText = ' بنفش ';
            break;
        case 'مشکی':
            colorText = ' مشکی ';
            break;
        default:
            colorText = '';
    }
    document.querySelector('.color-label').innerText = colorText;
}

const simple_product = new Swiper('.swiper.simple-product', {
    // Optional parameters
    direction: 'horizontal',
    slidesPerView:5,
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
            slidesPerView: 1,
            spaceBetween: 10,
        },
        520: {
            slidesPerView: 2,
            spaceBetween: 10,
        },
        // when window width is >= 480px
        850: {
            slidesPerView: 3,
            spaceBetween: 15,
        },
        // when window width is >= 640px
        1100: {
            slidesPerView: 4,
            spaceBetween: 15,
        },
        1300: {
            slidesPerView: 5,
            spaceBetween: 15,
        },
        1600: {
            slidesPerView: 6,
            spaceBetween: 15,
        },
    }

});


var video_frame = new Swiper(".video-frame", {
    slidesPerView: 4,
    spaceBetween: 15,
    pagination: {
        el: ".swiper-pagination",
        clickable: true,
    },
    breakpoints: {
        // when window width is >= 320px
        330: {
            slidesPerView: 1,
            spaceBetween: 5,
        },

        700: {
            slidesPerView: 2,
            spaceBetween: 10,
        },

        1000: {
            slidesPerView: 3,
            spaceBetween: 15,
        },
        1300: {
            slidesPerView: 4,
            spaceBetween: 15,
        },

    }
});




function showMore(boxNumber) {
    var moreText = document.getElementById("moreText" + boxNumber);
    var closeButton = moreText.querySelector(".close-button");
    var showMoreLink = document.querySelector(`.show-more[onclick="showMore(${boxNumber})"]`);

    moreText.style.display = "block";
    closeButton.style.display = "inline-block";
    showMoreLink.style.display = "none";
}

function toggleText(boxNumber) {
    var moreText = document.getElementById("moreText" + boxNumber);
    var closeButton = moreText.querySelector(".close-button");
    var showMoreLink = document.querySelector(`.show-more[onclick="showMore(${boxNumber})"]`);

    if (moreText.style.display === "block") {
        moreText.style.display = "none";
        closeButton.style.display = "none";
        showMoreLink.style.display = "block";
    } else {
        showMore(boxNumber); 
    }
}


document.addEventListener('DOMContentLoaded', function() {
    const navbar = document.querySelector('.product-navbar');
    const commentRegister = document.querySelector('.comment-register');
    const questionRegister=document.querySelector('.question-register');
    const footer=document.querySelector('footer')
    const stickyClass = 'sticky';
    const stickyCommentClass = 'sticky-comment';
    const stickyQuestionClass = 'sticky-question';
    const menuOffset=document.querySelector('.header-bottom').offsetHeight;
    const navbarOffset = navbar.offsetTop;
    const productNavbarOffset=document.querySelector('.product-navbar').offsetHeight;
    const comment_title=document.querySelector('.comment-title')
    const question_title=document.querySelector('.question-title')

    window.addEventListener('scroll', () => {
        const commentRegisterOffset = commentRegister.offsetTop;
        const questionRegisterOffset = questionRegister.offsetTop;
        const commentTitleOffset = comment_title.offsetTop;
        const questionTitleOffset = question_title.offsetTop;
        const footerOffset = footer.offsetTop;
        const scrollTop = window.scrollY;



        // چسباندن نوار ناوبری
        if (scrollTop >= navbarOffset-menuOffset) {
            navbar.classList.add(stickyClass);
        } else {
            navbar.classList.remove(stickyClass);
        }

        // چسباندن بخش کامنت زیر نوار ناوبری
        if (scrollTop >= commentTitleOffset-productNavbarOffset-menuOffset) {
            commentRegister.classList.add(stickyCommentClass);
        }
        else {
            commentRegister.classList.remove(stickyCommentClass);
        }
        if (scrollTop >= questionTitleOffset-productNavbarOffset-menuOffset) {
            questionRegister.classList.add(stickyQuestionClass);
            commentRegister.classList.remove(stickyCommentClass);
        }

        else {
            questionRegister.classList.remove(stickyQuestionClass);
        }

        console.log(scrollTop)
        console.log(commentTitleOffset)
        console.log(questionTitleOffset)

    });

});


const swiperSlides = document.querySelectorAll('.gallery .swiper-slide img');

swiperSlides.forEach(slide => {
    slide.addEventListener('mouseenter', () => {
        slide.style.transform = 'scale(1.3)';
    });

    slide.addEventListener('mouseleave', () => {
        slide.style.transform = 'scale(1)';
    });
});


const container_video = document.getElementById('video-slider'),
    sliders_video = document.querySelectorAll('.video-thumb[data-video]');

sliders_video.forEach(item => {
    item.addEventListener('click', () => container_video.src = item.dataset.video);
});


const story_video =document.querySelectorAll(".swiper-video")
const video = document.querySelector(".videos-introduction video");
const backdrop = document.querySelector(".videos-introduction.modal");

story_video.forEach(function (item){
    item.addEventListener("click" ,function (){
        video.currentTime = 0;
        video.autoplay = true;
        video.load();
    })
})

backdrop.addEventListener('hide.bs.modal', function () {
    requestAnimationFrame(function() {
        video.pause();
        video.currentTime = 0;
    });
});

var modal = document.getElementById("myModal");
var modal2 = document.getElementById("myModal2");

var btn = document.getElementById("openModal");
var btn2 = document.getElementById("openModal2");

var span = document.getElementsByClassName("close")[0];
var span2 = document.getElementsByClassName("close")[1];
console.log(span2)
btn.onclick = function() {
    modal.style.display = "block";
}
btn2.onclick = function() {
    modal2.style.display = "block";
}

span.onclick = function() {
    modal.style.display = "none";
}
span2.onclick = function() {
    modal2.style.display = "none";
}

window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}
window.onclick = function(event) {
    if (event.target == modal2) {
        modal2.style.display = "none";
    }
}


const question_filter=document.querySelector(".question-filter-list");
const question_filter_content=question_filter.innerHTML;
const modal_question_list=document.querySelector("#myModal2 .modal-list");
modal_question_list.innerHTML=question_filter_content;

const comment_filter=document.querySelector(".comment-filter-list");
const comment_filter_content=comment_filter.innerHTML;
const modal_comment_list=document.querySelector("#myModal .modal-list");
modal_comment_list.innerHTML=comment_filter_content;


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

// فراخوانی تابع پس از بارگذاری صفحه
window.onload = convertAllNumbersToPersian;
