from django.shortcuts import render,get_object_or_404,redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import Blog
from .forms import BlogForm

def home(request):
    blogs = Blog.objects.all()
    paginator = Paginator(blogs, 3)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)

    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        page_obj = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        page_obj = paginator.page(page)
    return render(request,'home.html',{'page_obj':page_obj, 'paginator':paginator})

def detail(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    return render(request,'detail.html',{'blog':blog})

def new(request):
    return render(request,'new.html')

def create(request):
    new_blog = Blog()
    new_blog.title = request.POST.get('title')
    new_blog.content = request.POST.get('content')
    new_blog.image = request.FILES.get('image')
    new_blog.save()
    return redirect('detail', new_blog.id)
    # return render(request, 'detail.html', {'blog':new_blog})

# def create(request):
#     form = BlogForm(request.POST)
#
#     if form.is_valid():
#         new_blog = form.save(commit=False)
#         new_blog.save()
#         return redirect('detail', new_blog.id)
#
#     return render(request, 'new.html')

def edit(request, blog_id):
    edit_blog = get_object_or_404(Blog, pk=blog_id) # print() 해보기
    return render(request, 'edit.html', {'edit_blog':edit_blog})


def update(request, blog_id):
    old_blog = get_object_or_404(Blog, pk=blog_id)
    old_blog.title = request.POST.get('title')
    old_blog.content = request.POST.get('content')
    old_blog.image = request.FILES.get('image')
    old_blog.save()
    return redirect('detail', old_blog.id)

# def update(request, blog_id):
#     old_blog = get_object_or_404(Blog, pk=blog_id)
#     form = BlogForm(request.POST, instance=old_blog)

    # 클라이언트가 유효한 값을 입력한 경우
    if form.is_valid():
        new_blog = form.save(commit=False)
        new_blog.save()
        return redirect('detail', old_blog.id)

    return render(request, 'new.html', {'old_blog':old_blog})


def delete(request, blog_id):
    delete_blog = get_object_or_404(Blog, pk=blog_id)
    delete_blog.delete()
    return redirect('home')


def search(request):
    if request.method=="POST":
        searched = request.POST['searched']
        searched_blogs = Blog.objects.filter(title__contains=searched)
        return render(request, 'searched.html', {'searched':searched, 'searched_blogs': searched_blogs})
    else:
        return render(request, 'searched.html', {})

