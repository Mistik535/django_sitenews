from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from .forms import AddPostForm
from .models import News, TagPost
from .utils import DataMixin


class NewsHome(DataMixin, ListView):
    template_name = 'news/index.html'
    context_object_name = 'posts'
    title_page = 'Главная страница'
    cat_selected = 0

    def get_queryset(self):
        return News.published.all().select_related('cat')


@login_required
def about(request):
    contact_list = News.published.all()
    paginator = Paginator(contact_list, 3)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'news/about.html',
                  {'title': 'О сайте', 'page_obj': page_obj})


class ShowPost(DataMixin, DetailView):
    template_name = 'news/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title=context['post'].title)

    def get_object(self, queryset=None):
        return get_object_or_404(News.published, slug=self.kwargs[self.slug_url_kwarg])


class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'news/addpage.html'
    title_page = 'Добавление поста'

    def form_valid(self, form):
        w = form.save(commit=False)
        w.author = self.request.user
        return super().form_valid(form)


class UpdatePage(DataMixin, UpdateView):
    model = News
    fields = ['title', 'content', 'photo', 'is_published', 'cat']
    template_name = 'news/addpage.html'
    success_url = reverse_lazy('home')
    title_page = 'Редактирование поста'


def contact(request):
    return HttpResponse("Обратная связь")


def login(request):
    return HttpResponse("Авторизация")


class NewsCategory(DataMixin, ListView):
    template_name = 'news/index.html'
    context_object_name = 'posts'
    slug_url_kwarg = 'cat_slug'
    allow_empty = False

    def get_queryset(self):
        return News.published.filter(cat__slug=self.kwargs[self.slug_url_kwarg]).select_related("cat")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = context['posts'][0].cat
        return self.get_mixin_context(context,
                                      title='Категория - ' + cat.name,
                                      cat_selected=cat.pk,
                                      )


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")


class TagPostList(DataMixin, ListView):
    template_name = 'news/index.html'
    context_object_name = 'posts'
    slug_url_kwarg = 'tag_slug'
    allow_empty = False
    model = TagPost

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = self.model.objects.get(slug=self.kwargs[self.slug_url_kwarg])
        return self.get_mixin_context(context, title='Тег: ' + tag.tag)

    def get_queryset(self):
        return News.published.filter(tags__slug=self.kwargs[self.slug_url_kwarg]).select_related(
            'cat').prefetch_related("tag_slug")