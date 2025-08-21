from django.views.generic import TemplateView, ListView
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse


from ..models import Product, ProductImage, ProductCategory, ProductColor, ProductSpecifications, ProductGuarantee, ProductVideos
from .forms import ProductForm, ProductImageForm, ProductCategoryForm, ProductGuaranteeForm, ProductColorForm, ProductVideosForm
from ..validators import validate_persian, validate_english
from .permissions import AdminOrSuperuserRequiredMixin



def product_search_api(request):
    query = request.GET.get('q', '')
    page = int(request.GET.get('page', 1))
    page_size = 10
    
    products = Product.objects.filter(
        Q(title_fa__icontains=query) | Q(title_en__icontains=query)
    ).order_by('title_fa')
    
    total_count = products.count()
    products = products[(page-1)*page_size : page*page_size]
    
    results = [{
        'id': p.id,
        'title_fa': p.title_fa,
        'title_en': p.title_en,
        'text': f"{p.title_fa} ({p.title_en})"
    } for p in products]
    
    return JsonResponse({
        'results': results,
        'total_count': total_count
    })
    
def category_search_api(request):
    query = request.GET.get('q', '')
    page = int(request.GET.get('page', 1))
    page_size = 10
    
    categories = ProductCategory.objects.filter(
        Q(title_fa__icontains=query) | Q(title_en__icontains=query)
    ).order_by('title_fa')
    
    total_count = categories.count()
    categories = categories[(page-1)*page_size : page*page_size]
    
    results = [{
        'id': p.id,
        'title_fa': p.title_fa,
        'title_en': p.title_en,
        'text': f"{p.title_fa} ({p.title_en})"
    } for p in categories]
    
    return JsonResponse({
        'results': results,
        'total_count': total_count
    })

def color_search_api(request):
    query = request.GET.get('q', '')
    page = int(request.GET.get('page', 1))
    page_size = 10
    
    objects = ProductColor.objects.filter(
        Q(title_fa__icontains=query) | Q(title_en__icontains=query)
    ).order_by('title_fa')
    
    total_count = objects.count()
    objects = objects[(page-1)*page_size : page*page_size]
    
    results = [{
        'id': p.id,
        'title_fa': p.title_fa,
        'title_en': p.title_en,
        'text': f"{p.title_fa} ({p.title_en})"
    } for p in objects]
    
    return JsonResponse({
        'results': results,
        'total_count': total_count
    })

def guarantee_search_api(request):
    query = request.GET.get('q', '')
    page = int(request.GET.get('page', 1))
    page_size = 10
    
    objects = ProductGuarantee.objects.filter(
        Q(title_fa__icontains=query) | Q(title_en__icontains=query)
    ).order_by('title_fa')
    
    total_count = objects.count()
    objects = objects[(page-1)*page_size : page*page_size]
    
    results = [{
        'id': p.id,
        'title_fa': p.title_fa,
        'title_en': p.title_en,
        'text': f"{p.title_fa} ({p.title_en})"
    } for p in objects]
    
    return JsonResponse({
        'results': results,
        'total_count': total_count
    })


class ProductCreateView(LoginRequiredMixin,AdminOrSuperuserRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'accounts/products/add_new.html'
    success_url = reverse_lazy('products:accounts:list_product')  # Change to your success URL
    
    def form_valid(self, form):
        # Automatically set the user to the current logged-in user
        form.instance.user = self.request.user
        
        # First save the product (this creates the product instance)
        response = super().form_valid(form)
        # Handle additional images
        additional_images = self.request.FILES.getlist('additional_images')
        
        # Limit to 5 images (matches the frontend limit)
        for image in additional_images[:5]:
            ProductImage.objects.create(
                product=self.object,  # The newly created product
                image=image
            )
        # Handle specifications
        titles_en = self.request.POST.getlist('new_spec_title_en[]')
        titles_fa = self.request.POST.getlist('new_spec_title_fa[]')
        values = self.request.POST.getlist('new_spec_value[]')
        specs_number = 0
        # Create specifications
        for title_en, title_fa, value in zip(titles_en, titles_fa, values):
            if title_en and title_fa and value:  # Only create if all fields have values
                specs_number = specs_number + 1
                ProductSpecifications.objects.create(
                    product=self.object,
                    title_en=title_en.strip(),
                    title_fa=title_fa.strip(),
                    value=value.strip()
                )
        # Add success message
        messages.success(
            self.request,
            f"محصول «{form.instance.title_fa}» با {len(additional_images)} تصویر اضافی و {specs_number} مشخصه اضافه شد."
        )
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add any additional context you need
        context['page_title'] = "افزودن محصول جدید"
        return context
    
class ProductUpdateView(LoginRequiredMixin,AdminOrSuperuserRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'accounts/products/add_new.html'
    success_url = reverse_lazy('products:accounts:list_product')  # Change to your success URL

    # def get_success_url(self):
    #     return reverse_lazy('products:accounts:edit_product', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        response = super().form_valid(form)
        
        # Handle main image deletion if checkbox is checked
        if 'image-clear' in self.request.POST:
            self.object.image.delete(save=True)
        
        # Handle deletion of existing additional images
        delete_images = self.request.POST.getlist('delete_images')
        if delete_images:
            self.object.images.filter(id__in=delete_images).delete()
        
        # Handle new additional images
        additional_images = self.request.FILES.getlist('additional_images')
        for image in additional_images[:5]:  # Limit to 5 images
            ProductImage.objects.create(
                product=self.object,
                image=image
            )

        # Handle existing specifications updates
        
        for spec in self.object.productspecifications_set.all():
            title_en = self.request.POST.get(f'existing_spec_title_en_{spec.id}')
            title_fa = self.request.POST.get(f'existing_spec_title_fa_{spec.id}')
            value = self.request.POST.get(f'existing_spec_value_{spec.id}')
            
            if title_en and title_fa and value:
                spec.title_en = title_en.strip()
                spec.title_fa = title_fa.strip()
                spec.value = value.strip()
                spec.save()
            else:
                spec.delete()  # Delete if any field is empty

        # Handle deleted specifications
        delete_specs = self.request.POST.getlist('delete_specs')
        ProductSpecifications.objects.filter(
            id__in=delete_specs, 
            product=self.object
        ).delete()

        # Handle new specifications (same as create view)
        titles_en = self.request.POST.getlist('new_spec_title_en[]')
        titles_fa = self.request.POST.getlist('new_spec_title_fa[]')
        values = self.request.POST.getlist('new_spec_value[]')

        for title_en, title_fa, value in zip(titles_en, titles_fa, values):
            if title_en and title_fa and value:
                ProductSpecifications.objects.create(
                    product=self.object,
                    title_en=title_en.strip(),
                    title_fa=title_fa.strip(),
                    value=value.strip()
                )

        # Add success message
        images_message = ""
        if delete_images or additional_images:
            deleted_count = len(delete_images)
            added_count = len(additional_images)
            messages_list = []
            if deleted_count:
                messages_list.append(f"{deleted_count} تصویر حذف شد")
            if added_count:
                messages_list.append(f"{added_count} تصویر اضافه شد")
            images_message = f" ({'، '.join(messages_list)})"
        
        messages.success(
            self.request,
            f"محصول «{form.instance.title_fa}» با موفقیت ویرایش شد.{images_message}"
        )
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'page_title': "ویرایش محصول",
            'editing': True,
            'existing_images': self.object.images.all().order_by('-created_date'),
            # Main image context
            'has_main_image': bool(self.object.image),
            'main_image_url': self.object.image.url if self.object.image else None,
        })
        return context

class ProductListView(LoginRequiredMixin,AdminOrSuperuserRequiredMixin, ListView):
    model = Product
    template_name = 'accounts/products/product_list.html'  # Update with your actual template path
    context_object_name = 'products'
    paginate_by = 10  # Adjust as needed
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter only published products
        queryset = queryset.all()
        
        # Search functionality
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(title_en__icontains=search_query) | 
                Q(title_fa__icontains=search_query) |
                Q(description__icontains=search_query)
            )
        
        # Category filter
        category_slug = self.request.GET.get('category')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
            
        # Color filter
        color_slug = self.request.GET.get('color')
        if color_slug:
            queryset = queryset.filter(color__slug=color_slug)
            
        # Price range filter
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
            
        # Discount filter
        has_discount = self.request.GET.get('has_discount')
        if has_discount:
            queryset = queryset.filter(discount_percent__gt=0)
        
        # draft filter
        is_draft = self.request.GET.get('is_draft')
        if is_draft:
            queryset = queryset.filter(status="draft")
            
        return queryset.distinct()  # Use distinct() to avoid duplicates from many-to-many relationships
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Add search query to context
        context['search_query'] = self.request.GET.get('search', '')
        
        # Add filter parameters to context for template
        context['selected_category'] = self.request.GET.get('category')
        context['selected_color'] = self.request.GET.get('color')
        context['min_price'] = self.request.GET.get('min_price')
        context['max_price'] = self.request.GET.get('max_price')
        context['has_discount'] = self.request.GET.get('has_discount')
        context['is_draft'] = self.request.GET.get('is_draft')
        # You might want to add available categories/colors for filter dropdowns
        context['categories'] = ProductCategory.objects.all()
        context['colors'] = ProductColor.objects.all()
        
        return context


class ProductCategoryCreateView(LoginRequiredMixin,  AdminOrSuperuserRequiredMixin, CreateView):
    model = ProductCategory
    form_class = ProductCategoryForm
    template_name = 'accounts/products/add_category.html'
    success_url = reverse_lazy('products:accounts:list_category')  # Change to your list URL name
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = "افزودن دسته‌بندی جدید"
        return context
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'دسته‌بندی جدید با موفقیت ایجاد شد.')
        return response
    
    def form_invalid(self, form):
        messages.error(self.request, 'لطفاً خطاهای زیر را اصلاح کنید.')
        return super().form_invalid(form)

class ProductCategoryUpdateView(LoginRequiredMixin,  AdminOrSuperuserRequiredMixin, UpdateView):
    model = ProductCategory
    form_class = ProductCategoryForm
    template_name = 'accounts/products/add_category.html'
    success_url = reverse_lazy('products:accounts:list_category')  # Change to your list URL name
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = "ویرایش دسته‌بندی"
        return context
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'دسته‌بندی با موفقیت ویرایش شد.')
        return response
    
    def form_invalid(self, form):
        messages.error(self.request, 'لطفاً خطاهای زیر را اصلاح کنید.')
        return super().form_invalid(form)

class ProductCategoryListView(LoginRequiredMixin,  AdminOrSuperuserRequiredMixin, ListView):
    model = ProductCategory
    template_name = 'accounts/products/category_list.html'  # Update with your actual template path
    context_object_name = 'categories'
    paginate_by = 10  # Adjust as needed
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter only published products
        queryset = queryset.all()
        
        # Search functionality
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(title_en__icontains=search_query) | 
                Q(title_fa__icontains=search_query) |
                Q(slug__icontains=search_query)
            )
            
        return queryset.distinct()  # Use distinct() to avoid duplicates from many-to-many relationships
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Add search query to context
        context['search_query'] = self.request.GET.get('search', '')
        
        return context


class ProductguaranteeCreateView(LoginRequiredMixin,  AdminOrSuperuserRequiredMixin, CreateView):
    model = ProductGuarantee
    form_class = ProductGuaranteeForm
    template_name = 'accounts/products/add_guarantee.html'
    success_url = reverse_lazy('products:accounts:list_guarantee')  # Change to your list URL name
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = "افزودن گارانتی جدید"
        return context
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'گارانتی جدید با موفقیت ایجاد شد.')
        return response
    
    def form_invalid(self, form):
        messages.error(self.request, 'لطفاً خطاهای زیر را اصلاح کنید.')
        return super().form_invalid(form)

class ProductguaranteeUpdateView(LoginRequiredMixin,  AdminOrSuperuserRequiredMixin, UpdateView):
    model = ProductGuarantee
    form_class = ProductGuaranteeForm
    template_name = 'accounts/products/add_guarantee.html'
    success_url = reverse_lazy('products:accounts:list_guarantee')  # Change to your list URL name
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = "ویرایش گارانتی"
        return context
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'گارانتی با موفقیت ویرایش شد.')
        return response
    
    def form_invalid(self, form):
        messages.error(self.request, 'لطفاً خطاهای زیر را اصلاح کنید.')
        return super().form_invalid(form)

class ProductguaranteeListView(LoginRequiredMixin,  AdminOrSuperuserRequiredMixin, ListView):
    model = ProductGuarantee
    template_name = 'accounts/products/guarantees_list.html'  # Update with your actual template path
    context_object_name = 'guarantees'
    paginate_by = 10  # Adjust as needed
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter only published products
        queryset = queryset.all()
        
        # Search functionality
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(title_en__icontains=search_query) | 
                Q(title_fa__icontains=search_query) |
                Q(slug__icontains=search_query) |
                Q(description__icontains=search_query)
            )
            
        return queryset.distinct()  # Use distinct() to avoid duplicates from many-to-many relationships
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Add search query to context
        context['search_query'] = self.request.GET.get('search', '')
        
        return context


class ProductColorCreateView(LoginRequiredMixin,  AdminOrSuperuserRequiredMixin, CreateView):
    model = ProductColor
    form_class = ProductColorForm
    template_name = 'accounts/products/add_color.html'
    success_url = reverse_lazy('products:accounts:list_color')  # Change to your list URL name
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = "افزودن رنگ جدید"
        return context
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'رنگ جدید با موفقیت ایجاد شد.')
        return response
    
    def form_invalid(self, form):
        messages.error(self.request, 'لطفاً خطاهای زیر را اصلاح کنید.')
        return super().form_invalid(form)

class ProductColorUpdateView(LoginRequiredMixin,  AdminOrSuperuserRequiredMixin, UpdateView):
    model = ProductColor
    form_class = ProductColorForm
    template_name = 'accounts/products/add_color.html'
    success_url = reverse_lazy('products:accounts:list_color')  # Change to your list URL name
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = "ویرایش رنگ"
        return context
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'رنگ با موفقیت ویرایش شد.')
        return response
    
    def form_invalid(self, form):
        messages.error(self.request, 'لطفاً خطاهای زیر را اصلاح کنید.')
        return super().form_invalid(form)

class ProductColorListView(LoginRequiredMixin,  AdminOrSuperuserRequiredMixin, ListView):
    model = ProductColor
    template_name = 'accounts/products/color_list.html'  # Update with your actual template path
    context_object_name = 'colors'
    paginate_by = 10  # Adjust as needed
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter only published products
        queryset = queryset.all()
        
        # Search functionality
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(title_en__icontains=search_query) | 
                Q(title_fa__icontains=search_query) |
                Q(slug__icontains=search_query) 
            )
            
        return queryset.distinct()  # Use distinct() to avoid duplicates from many-to-many relationships
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Add search query to context
        context['search_query'] = self.request.GET.get('search', '')
        
        return context



class ProductVideoCreateView(LoginRequiredMixin,  AdminOrSuperuserRequiredMixin, CreateView):
    model = ProductVideos
    form_class = ProductVideosForm
    template_name = 'accounts/products/add_video.html'
    success_url = reverse_lazy('products:accounts:list_video')  # Change to your list URL name
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = "افزودن فیلم جدید"
        return context
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'فیلم جدید با موفقیت ایجاد شد.')
        return response
    
    def form_invalid(self, form):
        messages.error(self.request, 'لطفاً خطاهای زیر را اصلاح کنید.')
        return super().form_invalid(form)

class ProductVideoUpdateView(LoginRequiredMixin,  AdminOrSuperuserRequiredMixin, UpdateView):
    model = ProductVideos
    form_class = ProductVideosForm
    template_name = 'accounts/products/add_video.html'
    success_url = reverse_lazy('products:accounts:list_video')  # Change to your list URL name
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = "ویرایش فیلم"
        return context
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'فیلم با موفقیت ویرایش شد.')
        return response
    
    def form_invalid(self, form):
        messages.error(self.request, 'لطفاً خطاهای زیر را اصلاح کنید.')
        return super().form_invalid(form)

class ProductVideoListView(LoginRequiredMixin,  AdminOrSuperuserRequiredMixin, ListView):
    model = ProductVideos
    template_name = 'accounts/products/video_list.html'  # Update with your actual template path
    context_object_name = 'videos'
    paginate_by = 10  # Adjust as needed
    
    def get_queryset(self):
        queryset = super().get_queryset().select_related('user').prefetch_related('product')
        
        # Get filter parameters from request
        search_query = self.request.GET.get('search')
        product_slug = self.request.GET.get('product')
        language = self.request.GET.get('language')
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        has_cover = self.request.GET.get('has_cover')

        # Apply filters
        if search_query:
            queryset = queryset.filter(
                Q(title_fa__icontains=search_query) |
                Q(title_en__icontains=search_query) |
                Q(description__icontains=search_query)
            )
        
        if product_slug:
            queryset = queryset.filter(product__slug=product_slug)
        
        if language == 'fa':
            queryset = queryset.exclude(title_fa__exact='')
        elif language == 'en':
            queryset = queryset.exclude(title_en__exact='')
        
        if start_date:
            queryset = queryset.filter(created_date__gte=start_date)
        
        if end_date:
            queryset = queryset.filter(created_date__lte=end_date)
        
        if has_cover:
            queryset = queryset.exclude(cover__exact='')

        return queryset.order_by('-created_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Add filter values to context for template
        context['search_query'] = self.request.GET.get('search', '')
        context['selected_product'] = self.request.GET.get('product', '')
        context['selected_language'] = self.request.GET.get('language', '')
        context['start_date'] = self.request.GET.get('start_date', '')
        context['end_date'] = self.request.GET.get('end_date', '')
        context['has_cover'] = bool(self.request.GET.get('has_cover'))
        
        # Add products for the product filter dropdown
        context['products'] = Product.objects.all().only('slug', 'title_fa')
        
        return context

# continue coding ............