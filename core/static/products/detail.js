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