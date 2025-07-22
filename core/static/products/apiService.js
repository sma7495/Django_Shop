// apiService.js
const ApiService = {
    fetchProducts: function(params, apiUrl) {
        return new Promise((resolve, reject) => {
            $.ajax({
                url: apiUrl,
                method: 'GET',
                data: params,
                success: function(response) {
                    resolve(response);
                },
                error: function(xhr) {
                    reject(xhr);
                }
            });
        });
    },

    handleError: function(containerSelector = '#productsContainer') {
        $(containerSelector).html(`
            <div class="col-12 text-center py-5">
                <i class="fas fa-exclamation-triangle fa-3x text-danger mb-3"></i>
                <h4>Error loading products. Please try again.</h4>
            </div>
        `);
    }
};

export default ApiService;