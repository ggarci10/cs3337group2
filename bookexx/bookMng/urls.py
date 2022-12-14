from django.urls import path
from . import views
from bookMng.views import Register

urlpatterns = [

    path('', views.index, name='index'),
    path('postbook', views.postbook, name='postbook'),
    path('displaybooks', views.displaybooks, name='displaybooks'),
    path('book_detail/<int:book_id>', views.book_detail, name='book_detail'),
    path('mybooks', views.mybooks, name='mybooks'),
    path('book_delete/<int:book_id>', views.book_delete, name='book_delete'),
    path('favorites/', views.favorites, name='favorites'),
    path('book_favorite/<int:book_id>', views.book_favorite, name='book_favorite'),
    path('search_items', views.search_items, name='search_items'),
    path('aboutus', views.aboutus, name='aboutus'),
    path('rate/<int:book_id>', views.rate, name='rate'),
    path('comment/<int:book_id>', views.comment, name='comment'),
]