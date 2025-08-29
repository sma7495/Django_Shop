# views.py
from django.views.generic import CreateView, UpdateView, ListView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect

from .forms import PostForm, PostSearchForm, CategoryForm, TagForm
from ..models import Post, Category, Tag
from .permissions import AdminOrSuperuserRequiredMixin

    
def category_search_api(request):
    query = request.GET.get('q', '')
    page = int(request.GET.get('page', 1))
    page_size = 10
    
    categories = Category.objects.filter(
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

def tag_search_api(request):
    query = request.GET.get('q', '')
    page = int(request.GET.get('page', 1))
    page_size = 10
    
    categories = Tag.objects.filter(
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



class PostCreateView(LoginRequiredMixin,AdminOrSuperuserRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'accounts/blog/add_post.html'
    success_url = reverse_lazy("blog:accounts:list_post")
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)
        # Add success message
        messages.success(
            self.request,
            f"پست «{form.instance.title_fa}» با موفقیت اضافه شد."
        )
        return response
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add any additional context you need
        context['page_title'] = "افزودن پست جدید"
        return context

class PostUpdateView(LoginRequiredMixin,AdminOrSuperuserRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'accounts/blog/add_post.html'

    def get_success_url(self):
        return reverse_lazy("blog:accounts:edit_post", kwargs={"pk": self.object.pk})
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)
        # Add success message
        messages.success(
            self.request,
            f"پست «{form.instance.title_fa}» با موفقیت ویرایش شد."
        )
        return response
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add any additional context you need
        context['page_title'] = "ویرایش پست "
        return context

class PostListView(LoginRequiredMixin,AdminOrSuperuserRequiredMixin, ListView):
    model = Post
    template_name = 'accounts/blog/post_list.html'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = super().get_queryset()
        form = PostSearchForm(self.request.GET)
        
        if form.is_valid():
            search = form.cleaned_data.get('search')
            status = form.cleaned_data.get('status')
            category = form.cleaned_data.get('category')
            featured = form.cleaned_data.get('featured')
            date_from = form.cleaned_data.get('date_from')
            date_to = form.cleaned_data.get('date_to')
            
            if search:
                queryset = queryset.filter(
                    Q(title_fa__icontains=search) |
                    Q(title_en__icontains=search) |
                    Q(content__icontains=search)
                )
            
            if status:
                queryset = queryset.filter(status=status)
            
            if category:
                queryset = queryset.filter(categories=category)
            
            if featured:
                queryset = queryset.filter(featured=True)
            
            if date_from:
                queryset = queryset.filter(created_date__date__gte=date_from)
            
            if date_to:
                queryset = queryset.filter(created_date__date__lte=date_to)
        
        return queryset.order_by('-created_date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = "نمایش لیست پست ها"
        context['search_form'] = PostSearchForm(self.request.GET)
        context['categories'] = Category.objects.all()  # Adjust based on your Category model
        return context
  
class PostDeleteView(LoginRequiredMixin,AdminOrSuperuserRequiredMixin,DeleteView):
    model = Post
    template_name = 'accounts/delete_confirm.html'
    success_url = reverse_lazy('blog:accounts:list_post')
    
    def delete(self, request, *args, **kwargs):
        """
        Override delete method to add success message
        """
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        messages.success(self.request, f"'{self.object.title_fa}' با موفقیت حذف شد")
        return HttpResponseRedirect(success_url)
    
    def get_context_data(self, **kwargs):
        """
        Add extra context to the template
        """
        context = super().get_context_data(**kwargs)
        context['page_title'] = f"تایید حذف پست :  {self.object.title_fa} "
        context['item_detail'] = f"پست:  {self.object.title_fa} "
        context['item_title'] = f" تیتر لاتین:  {self.object.title_en} "
        context['item_description'] = self.object.excerpt 
        return context  

# Category Views
class CategoryListView(LoginRequiredMixin,AdminOrSuperuserRequiredMixin, ListView):
    model = Category
    template_name = 'accounts/blog/category_list.html'
    context_object_name = 'categories'
    paginate_by = 10
    
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
        context['page_title'] = "نمایش لیست دسته بندی ها"
        
        # Add search query to context
        context['search_query'] = self.request.GET.get('search', '')
        return context

class CategoryCreateView(LoginRequiredMixin,AdminOrSuperuserRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'accounts/blog/add_category_tag.html'
    success_url = reverse_lazy('blog:accounts:list_category')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, _('دسته‌بندی با موفقیت ایجاد شد'))
        return response
    
    def form_invalid(self, form):
        messages.error(self.request, _('خطا در ایجاد دسته‌بندی. لطفاً اطلاعات را بررسی کنید'))
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context["page_title"] = "ایجاد دسته بندی جدید"
        context["page_category_title"] = "مدیریت دسته بندی وبلاگ"
        return context
    
class CategoryUpdateView(LoginRequiredMixin,AdminOrSuperuserRequiredMixin,UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'accounts/blog/add_category_tag.html'
    success_url = reverse_lazy('blog:accounts:list_category')
    
    def get_object(self):
        return get_object_or_404(Category, pk=self.kwargs['pk'])
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, _('دسته‌بندی با موفقیت ویرایش شد'))
        return response
    
    def form_invalid(self, form):
        messages.error(self.request, _('خطا در ویرایش دسته‌بندی. لطفاً اطلاعات را بررسی کنید'))
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context["page_title"] = "ویرایش دسته بندی "
        context["page_category_title"] = "مدیریت دسته بندی وبلاگ"
        return context
    
class CategoryDeleteView(LoginRequiredMixin,AdminOrSuperuserRequiredMixin,DeleteView):
    model = Category
    template_name = 'accounts/delete_confirm.html'
    success_url = reverse_lazy('blog:accounts:list_category')
    
    def delete(self, request, *args, **kwargs):
        """
        Override delete method to add success message
        """
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        messages.success(self.request, f"'{self.object.title_fa}' با موفقیت حذف شد")
        return HttpResponseRedirect(success_url)
    
    def get_context_data(self, **kwargs):
        """
        Add extra context to the template
        """
        context = super().get_context_data(**kwargs)
        context['page_title'] = f"تایید حذف دسته :  {self.object.title_fa} "
        context['item_detail'] = f"دسته:  {self.object.title_fa} "
        context['item_title'] = f" تیتر لاتین:  {self.object.title_en} "
        context['item_description'] = "ندارد"
        return context


# Tag Views
class TagListView(LoginRequiredMixin, AdminOrSuperuserRequiredMixin, ListView):
    model = Tag
    template_name = 'accounts/blog/tag_list.html'
    context_object_name = 'categories'
    paginate_by = 10
    
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
        context["page_title"] = "نمایش لیست تگ ها"
        
        # Add search query to context
        context['search_query'] = self.request.GET.get('search', '')
        return context

class TagCreateView(LoginRequiredMixin, AdminOrSuperuserRequiredMixin, CreateView):
    model = Tag
    form_class = TagForm
    template_name = 'accounts/blog/add_category_tag.html'
    success_url = reverse_lazy('blog:accounts:list_tag')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, _('تگ با موفقیت ایجاد شد'))
        return response
    
    def form_invalid(self, form):
        messages.error(self.request, _('خطا در ایجاد تگ. لطفاً اطلاعات را بررسی کنید'))
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context["page_title"] = "ایجاد تگ جدید"
        context["page_category_title"] = "مدیریت تگ های وبلاگ"
        return context

class TagUpdateView(LoginRequiredMixin, AdminOrSuperuserRequiredMixin, UpdateView):
    model = Tag
    form_class = TagForm
    template_name = 'accounts/blog/add_category_tag.html'
    success_url = reverse_lazy('blog:accounts:list_tag')
    
    def get_object(self):
        return get_object_or_404(Tag, pk=self.kwargs['pk'])
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, _('تگ با موفقیت ویرایش شد'))
        return response
    
    def form_invalid(self, form):
        messages.error(self.request, _('خطا در ویرایش تگ. لطفاً اطلاعات را بررسی کنید'))
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context["page_title"] = "ویرایش تگ  "
        context["page_category_title"] = "مدیریت تگ وبلاگ"
        return context

class TagDeleteView(LoginRequiredMixin,AdminOrSuperuserRequiredMixin,DeleteView):
    model = Tag
    template_name = 'accounts/delete_confirm.html'
    success_url = reverse_lazy('blog:accounts:list_tag')
    
    def delete(self, request, *args, **kwargs):
        """
        Override delete method to add success message
        """
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        messages.success(self.request, f"'{self.object.title_fa}' با موفقیت حذف شد")
        return HttpResponseRedirect(success_url)
    
    def get_context_data(self, **kwargs):
        """
        Add extra context to the template
        """
        context = super().get_context_data(**kwargs)
        context['page_title'] = f"تایید حذف تگ :  {self.object.title_fa} "
        context['item_detail'] = f"تگ:  {self.object.title_fa} "
        context['item_title'] = f" تیتر لاتین:  {self.object.title_en} "
        context['item_description'] = "ندارد"
        return context  
# continue ..............