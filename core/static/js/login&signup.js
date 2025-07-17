





function moveToNext(input) {
    const inputs = document.querySelectorAll('.styled-input');
    const index = Array.from(inputs).indexOf(input);

    // اگر input پر شده باشد، به input بعدی برود
    if (input.value.length >= 1 && index < inputs.length - 1) {
        inputs[index + 1].focus(); // تمرکز روی input بعدی
    }

    // اگر محتوا پاک شود، به input قبلی برگردد
    if (input.value.length === 0 && index > 0) {
        inputs[index - 1].focus(); // تمرکز روی input قبلی
    }
}

const verify=document.querySelectorAll(".styled-input");
console.dir(verify)


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
