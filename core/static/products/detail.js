// Get product ID from URL (assuming it's passed as a query parameter)
const productContainer = document.getElementById('product-details');
const productId = productContainer.dataset.productId;
const apiUrl = productContainer.dataset.apiUrl.replace('0', productId);


// DOM elements
const productDetailsContainer = document.getElementById('product-details-container');

// Fetch product details
async function fetchProductDetails() {
    try {
        const response = await fetch(apiUrl);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const product = await response.json();
        displayProductDetails(product);
    } catch (error) {
        console.error('Error fetching product details:', error);
        productDetailsContainer.innerHTML = `
            <div class="error">
                <h3>Error loading product</h3>
                <p>${error.message}</p>
                <p>Please try again later.</p>
            </div>
        `;
    }
}

// Display product details
function displayProductDetails(product) {
    // Format price with commas
    const formatPrice = (price) => {
        return price ? price.toLocaleString() : '0';
    };

    // Determine price display
    let priceDisplay = '';
    if (product.discount_percent > 0) {
        priceDisplay = `
            <span class="original-price">${formatPrice(product.price)} تومان</span>
            <span class="discounted-price">${formatPrice(product.discounted_price)} تومان (${product.discount_percent}% off)</span>
        `;
    } else {
        priceDisplay = `<span>${formatPrice(product.price)} تومان</span>`;
    }

    // Determine stock status
    const stockStatus = product.stock > 0 
        ? `<span style="color: green;">In Stock (${product.stock} available)</span>`
        : '<span style="color: red;">Out of Stock</span>';

    // Create HTML for product details
    productDetailsContainer.innerHTML = `
    
            <div class="product-container">
            <h1 class="product-title">${product.title_en} / ${product.title_fa}</h1>
            
            ${product.image_url ? `<img src="${product.image_url}" alt="${product.title_en}" class="product-image">` : ''}
            
            <div class="product-price">
                ${priceDisplay}
            </div>
            
            <div class="product-meta">
                <p><strong>Status:</strong> ${product.status}</p>
                <p><strong>Stock:</strong> ${stockStatus}</p>
                <p><strong>SKU:</strong> ${product.id}</p>
            </div>
            
            ${product.brief_description ? `
                <div class="product-description">
                    <h3>Brief Description</h3>
                    <p>${product.brief_description}</p>
                </div>
            ` : ''}
            
            ${product.description ? `
                <div class="product-description">
                    <h3>Full Description</h3>
                    <p>${product.description}</p>
                </div>
            ` : ''}
            
            <div class="product-meta">
                <p><strong>Last Updated:</strong> ${new Date(product.updated_date).toLocaleString()}</p>
            </div>
        </div>

    
    `
    productDetailsContainer.innerHTML = `

            <div class="col-12 col-lg-4  gallery-box">
                <div class="row guid-line d-flex flex-row justify-content-center  gap-3 ">
                    <div class="col-auto " data-toggle="tooltip" data-placement="right" title="اضافه به علاقه مندی">
                        <a href="#"><i class="fa-regular fa-heart"></i></a></div>
                    <div class="col-auto" data-toggle="tooltip" data-placement="left" title="به اشتراک گذاری کالا">
                        <a href="#"><i class="fa-solid fa-share-nodes"></i></a></div>
                    <div class="col-auto" data-toggle="tooltip" data-placement="left"
                         title="اطلاع رسانی شگفت انگیز"><a href="#"><i class="fa-regular fa-bell"></i></a></div>
                    <div class="col-auto" data-toggle="tooltip" data-placement="left" title="نمودار قیمت"><a
                            href="#"><i class="fa-solid fa-chart-line"></i></a></div>
                    <div class="col-auto" data-toggle="tooltip" data-placement="left" title="مقایسه کالا"><a
                            href="#"><i class="fa-solid fa-code-compare"></i></a></div>
                    <div class="col-auto" data-toggle="tooltip" data-placement="left" title="افزودن به لیست"><a
                            href="#"><i class="fa-solid fa-list"></i></a></div>
                </div>
                <div style="--swiper-navigation-color: #fff; --swiper-pagination-color: #fff"
                     class="swiper gallery">
                    <div id='lens'></div>
                    <div class="swiper-wrapper">
                        <div class="swiper-slide">
                            <img src="${product.image_url}"/>
                        </div>
                    ${product.other_images.map(image => `
                        <div class="swiper-slide">
                            <img src="${image.image}"/>
                        </div>
                    `).join('')}
                    </div>
                </div>

                <div thumbsSlider="" class="swiper gallery-thumbs">

                    <div class="swiper-wrapper">
                        <div class="swiper-slide">
                            <img src="${product.image_url}"/>
                        </div>
                        ${product.other_images.map(image => `
                        <div class="swiper-slide">
                            <img src="${image.image}"/>
                        </div>
                        `).join('')}
                    </div>
                </div>

            </div>

            <div class="col-12 col-lg-8  font-vazir mt-5">
                <div class="product-detail-title-box ms-2 ms-md-5">
                    <div class="row">
                        <div class="col-12 col-lg-8  pb-3">
                                <span class="product-main-title">
                                    <h4>گوشی موبایل سامسونگ مدل Galaxy S24 Ultra</h4>
                                </span>
                            <span class="product-detail-title">
                                    <h6>دو سیم کارت ظرفیت 256 گیگابایت و رم 12 گیگابایت - ویتنام </h6>
                                </span>
                            <div class="detail-2 d-flex justify-content-start ">
                                <div class="product-brand me-5">
                                    <span>برند:</span><a href="#">سامسونگ</a>
                                </div>
                                <div class="product-cat pb-4">
                                    <span>دسته بندی:</span><a href="#">گوشی موبایل</a>
                                </div>
                            </div>
                            <div class="row border-line">

                                <span class="line"> گوشی موبایل سامسونگ مدل Galaxy S24 Ultra</span></div>

                        </div>
                        <div class="col-4 d-none d-lg-flex justify-content-center">
                            <div class="product-logo"><img src="{% static 'images/Samsung_Logo.svg.png' %}"></div>

                        </div>
                    </div>
                </div>
                <div class="row">
                    <div class="col-12 col-xl-8">
                        <div class="product-rate d-flex ms-lg-5">
                            <div class="review-star font-small-12 me-1">
                                <i class="fa-solid fa-star"></i>
                                <i class="fa-solid fa-star"></i>
                                <i class="fa-solid fa-star"></i>
                                <i class="fa-regular fa-star-half-stroke"></i>
                                <i class="fa-regular fa-star"></i>
                            </div>
                            <span class="review-count font-small-12">(3.5)</span><span class="mx-2 font-small-12">از 48 نفر </span>

                            <div class="feedback ms-2 ms-md-5">
                                <a href="#comments ">315 دیدگاه</a>
                            </div>
                            <div class="feedback ms-2 ms-md-5">
                                <a href="#questions ">212 پرسش</a>
                            </div>
                        </div>
                        <div class="like ms-lg-5 my-3">
                            <span><i class="fa-regular fa-thumbs-up"></i></span><span class="ps-3 font-small-14">۸۶% (۵۹۰ نفر) از خریداران، این کالا را پیشنهاد کرده‌اند</span>
                        </div>
                        <div class="product-color ms-lg-5 font-18">
                            <span>رنگ:</span><span id="colorOutput ps-2" class="color-label"> انتخاب کنید  </span>
                        </div>
                        <div class="product-color ms-lg-5  d-flex">
                                <span class="rounded-circle gray" onclick="selectCircle(this, 'خاکستری')">  <span
                                        class="checkmark">✔</span>  </span>
                            <span class="rounded-circle yellow" onclick="selectCircle(this, 'زرد')">  <span
                                    class="checkmark">✔</span>  </span>
                            <span class="rounded-circle purple" onclick="selectCircle(this, 'بنفش')">  <span
                                    class="checkmark">✔</span>  </span>
                            <span class="rounded-circle  black" onclick="selectCircle(this, 'مشکی')">  <span
                                    class="checkmark">✔</span>  </span>
                        </div>

                        <div class="row ms-lg-5 my-3 d-flex flex-lg-column ">
                            <div class="features-box border-warning font-yekan">
                                <div class="fw-bold font-20 font-small-16 mb-3">ویژگی ها:</div>
                                <div class="feature d-flex align-items-center justify-content-start rounded-3 my-2 p-2 ps-4">
                                    <span class=" feature-title font-small-12">فناوری صفحه‌ نمایش :</span>
                                    <span class="mx-2 feature font-small-12">Dynamic LTPO AMOLED 2X </span>
                                </div>
                                <div class="feature d-flex align-items-center justify-content-start rounded-3 my-2 p-2 ps-4">
                                    <span class=" feature-title font-small-12">رزولوشن دوربین :</span>
                                    <span class="mx-2 feature font-small-12">200 مگاپیکسل </span>
                                </div>
                                <div class="feature d-flex align-items-center justify-content-start rounded-3 my-2 p-2 ps-4">
                                    <span class=" feature-title font-small-12">نسخه سیستم عامل :</span>
                                    <span class="mx-2 feature font-small-12">Android 14 </span>
                                </div>
                                <div class="feature d-flex align-items-center justify-content-start rounded-3 my-2 p-2 ps-4">
                                    <span class=" feature-title font-small-12">اندازه :</span>
                                    <span class="mx-2 feature font-small-12">6.8 اینچ </span>
                                </div>
                                <a href="#feature"
                                   class="feature feature-title border rounded-3 my-2 p-2 d-flex align-items-center justify-content-center font-small-14">مشاهده
                                    همه ویژگی ها</a>
                            </div>
                            <div class="row my-3  ms-3  rounded-3 insurance">
                                <div class="col-1 border rounded-3 rounded-end-0 d-flex justify-content-center align-items-center border-end ">
                                    <input type="checkbox"></div>
                                <div class="col-11 rounded-3 rounded-start-0 border border-start-0 py-2 ps-4">
                                    <div class="row d-flex flex-column">
                                        <div class="col-auto font-small-14"><span>بیمه تجهیزات دیجیتال -بانک دی</span>
                                        </div>
                                        <div class="col-auto d-flex justify-content-between">
                                            <span class="price font-small-14">850,000</span>
                                            <span><a href="#" class="font-small-13">جزئیات </a></span></div>
                                    </div>

                                </div>
                            </div>
                        </div>

                    </div>
                    <div class="col-12 col-xl-4">
                        <div class="row d-flex flex-column border bg-light rounded-3 seller-panel-box justify-content-between justify-content-lg-center">
                            <div class="col-auto d-none d-xl-flex justify-content-start px-3 py-3"><h4><i
                                    class="fa-regular fa-circle-check"></i> موجود </h4></div>
                            <div class="col-auto d-none d-xl-flex justify-content-between px-3  py-2"><h5>
                                فروشنده</h5><span><a href="#sellers" class="font-14">15 فروشنده دیگر</a></span>
                            </div>
                            <div class="col-auto d-none d-xl-flex px-3  py-2"><span class="shop-icon"><i
                                    class="fa-solid fa-shop me-3 font-18"></i></span><span class="seller-name">گالری دیجی مارکت</span>
                            </div>
                            <div class="col-xl-auto col-6 d-flex  gap-2 gap-xl-0 flex-column flex-xl-row justify-content-center  my-xl-3 pt-3 seller-panel-box-counter-price align-items-center justify-content-xl-between">
                                <div class="counter cart-prd-counter">
                                        <span class="up" onClick='increaseCount(event, this)'><i
                                                class="fa-solid fa-circle-plus"></i></span>
                                    <input type="text" value="1">
                                    <span class="down" onClick='decreaseCount(event, this)'><i
                                            class="fa-solid fa-circle-minus"></i></span></div>
                                <span class="price font-sans font-14">60,100,000</span>
                            </div>

                            <div class="col-auto d-none d-xl-flex px-2 guarantee py-2"><span><i
                                    class="fa-solid fa-award font-20"></i></span><span class="ps-3">گارانتی ۱۸ ماهه پایدار پردازش کوشان</span>
                            </div>
                            <div class="col-6 col-xl-auto d-flex justify-content-center px-1 guarantee py-3 ">
                                <button class="sideicons-btn py-2 px-3 px-md-4 btn btn-primary btn-card font-small-14">
                                    <i
                                            class="fa-solid fa-cart-plus "></i>افزودن به سبد
                                </button>
                            </div>

                        </div>


                    </div>
                </div>


            </div>
    `;
}

// Initialize the page
if (productId) {
    fetchProductDetails();
} else {
    productDetailsContainer.innerHTML = `
        <div class="error">
            <h3>Product ID not specified</h3>
            <p>Please provide a product ID in the URL.</p>
        </div>
    `;
}