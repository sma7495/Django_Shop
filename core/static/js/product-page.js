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

/*-------------product-page---------*/







const rangeInput = document.querySelectorAll(".range-input input"),
    priceInput = document.querySelectorAll(".price-input input"),
    range = document.querySelector(".slider .progress");
let priceGap = 1000;

priceInput.forEach((input) => {
    input.addEventListener("input", (e) => {
        let minPrice = parseInt(priceInput[0].value),
            maxPrice = parseInt(priceInput[1].value);

        if (maxPrice - minPrice >= priceGap && maxPrice <= rangeInput[1].max) {
            if (e.target.className === "input-min") {
                rangeInput[0].value = minPrice;
                range.style.left = (minPrice / rangeInput[0].max) * 100 + "%";
            } else {
                rangeInput[1].value = maxPrice;
                range.style.right = 100 - (maxPrice / rangeInput[1].max) * 100 + "%";
            }
        }
    });
});

rangeInput.forEach((input) => {
    input.addEventListener("input", (e) => {
        let minVal = parseInt(rangeInput[0].value),
            maxVal = parseInt(rangeInput[1].value);

        if (maxVal - minVal < priceGap) {
            if (e.target.className === "range-min") {
                rangeInput[0].value = maxVal - priceGap;
            } else {
                rangeInput[1].value = minVal + priceGap;
            }
        } else {
            priceInput[0].value = minVal;
            priceInput[1].value = maxVal;
            range.style.left = (minVal / rangeInput[0].max) * 100 + "%";
            range.style.right = 100 - (maxVal / rangeInput[1].max) * 100 + "%";
        }
    });
});


$(document).ready(function() {
    $(".container-xxl .sticky-sidebar").theiaStickySidebar({
        // Settings
        additionalMarginTop: 60
    });
});






function selectCircle(selected, color) {
    const circles = document.querySelectorAll('.rounded-circle');
    circles.forEach(circles => {
        circles.classList.remove('selected');
    });
    selected.classList.add('selected');
}

//

var modal = document.getElementById("myModal");

// Get the button that opens the modal
var btn = document.getElementById("openModal");

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

// When the user clicks the button, open the modal
btn.onclick = function() {
    modal.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
    modal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}
const filterProduct = document.getElementById("filterMenu");
const filter_list=document.querySelector(".modal-list")
const filterProductContent=filterProduct.innerHTML;
filter_list.innerHTML=filterProductContent;


let menuToggle = document.querySelector('.menuToggle');
menuToggle.onclick = function () {
    menuToggle.classList.toggle('open');
}

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
