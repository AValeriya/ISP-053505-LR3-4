from django.shortcuts import render
from django.http import HttpResponse
from .models import Book, Author, BookInstanse, Genre
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import *
from .forms import AuthorsForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Book
import asyncio
import logging
from asgiref.sync import sync_to_async
# Create your views here.


# получение данных из БД и загрузка шаблона authors_add.html
def authors_add(request):
    author = Author.objects.all()
    authorsform = AuthorsForm()
    return render(request, "catalog/authors_add.html",
                  {"form": authorsform, "author": author})
logger = logging.getLogger(__name__)
# сохранение данных об авторах в БД
def create(request):
    if request.method == "POST":
        author = Author()
        author.first_name = request.POST.get("first_name")
        author.last_name = request.POST.get("last_name")
        author.date_of_birth = request.POST.get("date_of_birth")
        author.date_of_death = request.POST.get("date_of_death")
        author.save()
	logger.error("Test!")
        return HttpResponseRedirect("/authors_add/")

# удаление авторов из БД
def delete(request, id):
    try:
        author = Author.objects.get(id=id)
	author = asyncio.run(get_author_by_user_id(id))
        author.delete()
        return HttpResponseRedirect("/authors_add/")
    except Author.DoesNotExist:
        return HttpResponseNotFound("<h2>Автор не найден</h2>")

# изменение данных в БД
def edit1(request, id):
    author = Author.objects.get(id=id)
    if request.method == "POST":
        author.first_name = request.POST.get("first_name")
        author.last_name = request.POST.get("last_name")
        author.date_of_birth = request.POST.get("date_of_birth")
        author.date_of_death = request.POST.get("date_of_death")
        author.save()
        return HttpResponseRedirect("/authors_add/")
    else:
        return render(request, "edit1.html", {"author": author})

def index(request):
    # Генерация "количеств" некоторых главных объектов
    num_books = Book.objects.all().count()
    num_instances = BookInstanse.objects.all().count()
    # Доступные книги (статус = 'На складе')
    # Здесь метод 'all()' применен по умолчанию.
    num_instances_available = BookInstanse.objects.filter(status__exact=2).count()
    # Авторы книг,
    num_authors = Author.objects.count()

    # Количество посещений этого view, подсчитанное
    # в переменной session
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    # Отрисовка HTML-шаблона index.html с данными
    # внутри переменной context
    return render(request, 'index.html', context={
                                         'num_books': num_books,
                                         'num_instances': num_instances,
                                         'num_instances_available': num_instances_available,
                                         'num_authors': num_authors,
                                         'num_visits': num_visits})

@sync_to_async
def get_author_by_user_id(id):
    return Author.objects.get(user_id=id)

class BookListView(generic.ListView):
    model = Book

class BookDetailView(generic.DetailView):
    model = Book

class BookListView(generic.ListView):
    model = Book
    paginate_by = 3

class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 4

class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """
    Универсальный класс представления списка книг,
    находящихся в заказе у текущего пользователя.
    """
    model = BookInstanse
    template_name = 'catalog/bookinstanse_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstanse.objects.filter(borrower=self.request.user).filter(status__exact='2').order_by('due_back')


class BookCreate(CreateView):
    model = Book
    fields = '__all__'
    success_url = reverse_lazy('books')


class BookUpdate(UpdateView):
    model = Book
    fields = '__all__'
    success_url = reverse_lazy('books')


class BookDelete(DeleteView):
    model = Book
    success_url = reverse_lazy('books')