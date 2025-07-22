

$(document).ready(function() {
    const apiUrl = '/products/api/v1/list/';
    let currentPage = 1;
    const productsPerPage =10;
    let currentSearch = '';
    let currentSort = 'newest';
    
    // Initial load
    loadProducts();
    
    // Search handler
    $('#searchBtn').click(function() {
        currentSearch = $('#searchInput').val();
        currentPage = 1;
        loadProducts();
    });
    
    // Sort handler
    $(document).on('click', '.sort-option', function() {
        // Update active state
        $('.sort-option').removeClass('active');
        $(this).addClass('active');

        // Get new sort value
        currentSort = $(this).data('sort');
        currentPage = 1; // Reset to first page on sort change

        //console.log('Current Sort Value:', currentSort);
        // Reload products with new sorting
        loadProducts();
    });
    
    // Load products from API
    function loadProducts() {
        showLoading();
        
        let params = {
            page: currentPage,
            page_size: productsPerPage
        };
        
        // Add search parameter if exists
        if (currentSearch) {
            params.search = currentSearch;
        }
        
        // Add sorting
        switch(currentSort) {
            case 'price_asc':
                params.ordering = 'price';
                break;
            case 'price_desc':
                params.ordering = '-price';
                break;
            case 'discount':
                params.ordering = '-discount_percent';
                break;
            default:
                params.ordering = '-created_date';
        }
        $.ajax({
            url: apiUrl,
            method: 'GET',
            data: params,
            success: function(response) {
                renderProducts(response.results);
                renderPagination(response.count);
                hideLoading();
            },
            error: function(xhr) {
                console.error('Error loading products');
                $('#productsContainer').html(`
                    <div class="col-12 text-center py-5">
                        <i class="fas fa-exclamation-triangle fa-3x text-danger mb-3"></i>
                        <h4>Error loading products. Please try again.</h4>
                    </div>
                `);
                hideLoading();
            }
        });
    }
    
    // Render products
    function renderProducts(products) {
        const container = $('#productsContainer');
        container.empty();
        
        if (products.length === 0) {
            container.html(`
                <div class="col-12 col-sm-6 col-lg-4 col-xxl-3 my-3 product-single-card-box ">
                هیچ محصولی یافت نشد
                </div>
            `);
            return;
        }
        
        products.forEach(product => {
            const hasDiscount = product.discount_percent > 0;
            const discountedPrice = hasDiscount ? product.discounted_price : product.price;
            
            const productCard = `
                            <div class="col-12 col-sm-6 col-lg-4 col-xxl-3 my-3 product-single-card-box ">
                                <div class="product-single-card d-flex flex-column align-items-center">
                                    <div class="product-top-area d-flex ">
                                        <span class="ribbon ribbon-product">30%</span>

                                        <div class="product-img d-flex flex-column justify-content-center ">
                                            <div class="first-view d-flex align-items-center">
                                                <img src="${product.image_url || '/static/images/default-product.png'}" alt="${product.title_en}" class="img-fluid"
                                                        onerror="this.src='https://i.ibb.co/qpB9ZCZ/placeholder.png'">
                                            </div>
                                            <div class="hover-view d-flex align-items-center justify-content-center">
                                                <img src="${product.image_url}" alt="logo" class="img-fluid"
                                                        onerror="this.src='https://i.ibb.co/qpB9ZCZ/placeholder.png'">
                                            </div>
                                        </div>
                                        <div class="sideicons">

                                            <a href="product-details.html" class="sideicons-btn">
                                                <i class="fa-solid fa-eye"></i>
                                            </a>
                                            <button class="sideicons-btn">
                                                <i class="fa-solid fa-heart"></i>
                                            </button>
                                            <button class="sideicons-btn">
                                                <i class="fa-solid fa-shuffle"></i>
                                            </button>
                                        </div>
                                    </div>
                                    <div class="product-info ">

                                        <h6 class="product-title text-color"><a href="#"> ${product.title_fa} </a></h6>
                                        <div class="d-flex align-items-center justify-content-center">
                                            <div class="review-star me-1">
                                                <i class="fa-solid fa-star"></i>
                                                <i class="fa-solid fa-star"></i>
                                                <i class="fa-solid fa-star"></i>
                                                <i class="fa-regular fa-star-half-stroke"></i>
                                                <i class="fa-regular fa-star"></i>
                                            </div>

                                            <span class="review-count">(3.5)</span>
                                        </div>
                                        <div class="d-flex flex-wrap flex-column justify-content-center align-items-center py-2">
                                        ${hasDiscount ? `
                                            <div class="old-price price">
                                            ${product.price}
                                            </div>
                                            <div class="new-price price">${product.discounted_price}</div>
                                        ` 
                                        : `<div class="new-price price">${product.price}</div>`}

                                            

                                        </div>
                                    </div>
                                    <button class="sideicons-btn btn btn-primary btn-card">
                                        <i class="fa-solid fa-cart-plus"></i>
                                        افزودن به سبد
                                    </button>
                                </div>
                            </div>

            `;
            
            container.append(productCard);
        });
    }
    
    // Render pagination
    function renderPagination(totalItems) {
        const pagination = $('#pagination');
        pagination.empty();
        
        const totalPages = Math.ceil(totalItems / productsPerPage);
        
        if (totalPages <= 1) return;
        
        // Previous button
        if (currentPage !== 1){
            pagination.append(`
            <a href="#" class="page-number p-1 px-2 p-md-2 px-md-3 border " data-page="${currentPage - 1}">
            <i class="fa-solid fa-angles-right"></i></a>
            `);

        }
        
        // Page numbers
        for (let i = 1; i <= totalPages; i++) {
            pagination.append(`
                <a href="#" class="page-number ${i === currentPage ? 'active-page' : ''} p-1 px-2 p-md-2 px-md-3 border " data-page="${i}">${i}</a>
            `);
        }
        
        // Next button
        if (currentPage !== totalPages){
            pagination.append(`
            <a href="#" class="page-number p-1 px-2 p-md-2 px-md-3 border " data-page="${currentPage + 1}">
            <i class="fa-solid fa-angles-left"></i></a>
            `);

        }

        
        // Add click handlers
        $('.page-number').click(function(e) {
            e.preventDefault();
            const page = $(this).data('page');
            if (page && page !== currentPage) {
                currentPage = page;
                loadProducts();
                $('html, body').animate({ scrollTop: 0 }, 'fast');
            }
        });
    }
    
    // Loading state
    function showLoading() {
        $('#loadingSpinner').show();
    }
    
    function hideLoading() {
        $('#loadingSpinner').hide();
    }
});