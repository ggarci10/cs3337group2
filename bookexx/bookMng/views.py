from statistics import mean

from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from .models import MainMenu, Comment
from .forms import BookForm, ReviewForm, CommentForm
from django.http import HttpResponseRedirect
from .models import Book
from .models import Rate
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy


def index(request):
    # return HttpResponse("Hello World")
    return render(request,
                  'bookMng/index.html',
                  {
                      'item_list': MainMenu.objects.all()
                  })


def search_items(request):
    if request.method == "POST":
        searched = request.POST['searched']
        books = Book.objects.filter(name__contains=searched)

        return render(request,
                      'bookMng/search_items.html',
                      {'searched': searched,
                       'books': books}
                      )
    else:
        return render(request,
                      'bookMng/search_items.html', {})


def postbook(request):
    submitted = False
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            # form.save()
            book = form.save(commit=False)
            try:
                book.username = request.user
            except Exception:
                pass
            book.save()
            return HttpResponseRedirect('/postbook?submitted=True')
    else:
        form = BookForm()
        if 'submitted' in request.GET:
            submitted = True

    return render(request,
                  'bookMng/postbook.html',
                  {
                      'form': form,
                      'item_list': MainMenu.objects.all(),
                      'submitted': submitted
                  })


def displaybooks(request):
    books = Book.objects.all()
    for b in books:
        b.pic_path = b.picture.url[14:]
    return render(request,
                  'bookMng/displaybooks.html',
                  {
                      'item_list': MainMenu.objects.all(),
                      'books': books
                  })


def aboutus(request):
    return render(request,
                  'bookMng/aboutus.html',
                  {
                      'item_list': MainMenu.objects.all(),
                  })


def mybooks(request):
    if request.user.is_authenticated:
        books = Book.objects.filter(username=request.user)
        for b in books:
            b.pic_path = b.picture.url[14:]
        return render(request,
                      'bookMng/mybooks.html',
                      {
                          'item_list': MainMenu.objects.all(),
                          'books': books,
                      })
    else:
        return render(request,
                      'bookMng/mybooks.html',
                      {
                          'item_list': MainMenu.objects.all(),
                      })


def book_detail(request, book_id):
    book = Book.objects.get(id=book_id)
    book.pic_path = book.picture.url[14:]
    is_favorite = False
    is_rate = False
    is_comment = False
    if request.user.is_authenticated:
        if Comment.objects.filter(username=request.user, product__id=book_id).exists():
            is_comment = True
        if book.favorite.filter(id=request.user.id).exists():
            is_favorite = True
        if Rate.objects.filter(username=request.user, product__id=book_id).exists():
            is_rate = True
            avg = Rate.objects.filter(product__id=book_id).aggregate(Avg('rating'))
            comments = Comment.objects.filter(product__id=book_id)
            return render(request,
                          'bookMng/book_detail.html',
                          {
                              'item_list': MainMenu.objects.all(),
                              'book': book,
                              'is_favorite': is_favorite,
                              'is_comment': is_comment,
                              'rate': Rate.objects.get(username=request.user, product__id=book_id),
                              'is_rate': is_rate,
                              'avg': avg,
                              'comments': comments
                          })
        else:
            return render(request,
                          'bookMng/book_detail.html',
                          {
                              'item_list': MainMenu.objects.all(),
                              'book': book,
                              'is_favorite': is_favorite,
                              'is_rate': is_rate,
                              'is_comment': is_comment
                          })

    else:
        return render(request,
                      'bookMng/book_detail.html',
                      {
                          'item_list': MainMenu.objects.all(),
                          'book': book,

                      })


def favorites(request):
    if request.user.is_authenticated:
        books = Book.objects.filter(favorite=request.user)
        return render(request,
                      'bookMng/favorites.html',
                      {
                          'item_list': MainMenu.objects.all(),
                          'books': books,
                      })
    else:
        return render(request,
                      'bookMng/favorites.html',
                      {
                          'item_list': MainMenu.objects.all(),
                      })


def book_favorite(request, book_id):
    book = Book.objects.get(id=book_id)
    if book.favorite.filter(id=request.user.id).exists():
        is_favorite = True
        book.favorite.clear()
    else:
        book.favorite.add(request.user.id)
        is_favorite = False
    return render(request,
                  'bookMng/book_favorite.html',
                  {
                      'item_list': MainMenu.objects.all(),
                      'is_favorite': is_favorite
                  })


def book_delete(request, book_id):
    book = Book.objects.get(id=book_id)
    book.delete()
    return render(request,
                  'bookMng/book_delete.html',
                  {
                      'item_list': MainMenu.objects.all(),
                  })


class Register(CreateView):
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('register-success')


def form_valid(self, form):
    form.save()
    return HttpResponseRedirect(self.success_url)


def rate(request, book_id):
    book = Book.objects.get(id=book_id)
    book.pic_path = book.picture.url[14:]
    is_rate = False
    if Rate.objects.filter(username=request.user, product__id=book_id).exists():
        is_rate = True
    if request.method == "POST":
        try:
            review = Rate.objects.get(username=request.user, product__id=book_id)
            form = ReviewForm(request.POST, instance=review)
            form.save()
            return render(request,
                          'bookMng/rate.html',
                          {
                              'item_list': MainMenu.objects.all(),
                              'book': book,
                              'rate': Rate.objects.get(username=request.user, product__id=book_id),
                              'is_rate': is_rate
                          })
        except Rate.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = Rate()
                data.rating = form.cleaned_data['rating']
                data.product_id = book_id
                data.username_id = request.user.id
                data.save()
                return render(request,
                              'bookMng/book_favorite.html',
                              {
                                  'item_list': MainMenu.objects.all(),
                              })


def comment(request, book_id):
    book = Book.objects.get(id=book_id)
    book.pic_path = book.picture.url[14:]
    is_comment = False
    if Comment.objects.filter(username=request.user, product__id=book_id).exists():
        is_comment = True
    if request.method == "POST":
        try:
            c = Comment.objects.get(username=request.user, product__id=book_id)
            form = CommentForm(request.POST, instance=c)
            form.save()
            return render(request,
                          'bookMng/comment.html',
                          {
                              'item_list': MainMenu.objects.all(),
                              'book': book,
                              'rate': Comment.objects.get(username=request.user, product__id=book_id),
                              'is_comment': is_comment
                          })
        except Comment.DoesNotExist:
            form = CommentForm(request.POST)
            if form.is_valid():
                data = Comment()
                data.comment = form.cleaned_data['comment']
                data.product_id = book_id
                data.username_id = request.user.id
                data.save()
                return render(request,
                              'bookMng/comment.html',
                              {
                                  'item_list': MainMenu.objects.all(),
                              })
