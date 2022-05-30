from django.contrib import admin

# Register your models here.
from .models import Author, Book, Genre, Language, Status, BookInstanse

#admin.site.register(Author)
#Определение к классу администратор
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name')
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]
#Зарегистрируйте класс admin с соответствующей моделью
admin.site.register(Author, AuthorAdmin)
#admin.site.register(Book)

class BooksInstanseInline(admin.TabularInline):
    model = BookInstanse
#Регистрируем классы администратора для книг
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'genre', 'language', 'display_author')
    list_filter = ('genre', 'author')
    inlines = [BooksInstanseInline]
admin.site.register(Genre)
admin.site.register(Language)
admin.site.register(Status)
#admin.site.register(BookInstanse)
#Регистрируем классы администратора для экземпляра книг
@admin.register(BookInstanse)
class BookInstanseAdmin(admin.ModelAdmin):
    list_display = ('book', 'status', 'borrower', 'due_back', 'id')
    list_filter = ('status', 'due_back')
    fieldsets = (
        ('Экземпляр книги', {
            'fields': ('book', 'imprint', 'inv_nom')
        }),
        ('Статус и окончание его действия', {
            'fields': ('status', 'due_back', 'borrower')
        }),
    )
