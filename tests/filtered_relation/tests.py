from django.db.models import Q
from django.test import TestCase

from .models import Author, Book


class FilteredRelationTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author1 = Author.objects.create(name='Alice')
        cls.author2 = Author.objects.create(name='Jane')

        cls.book1 = Book.objects.create(title='Poem by Alice',
                                        editor='A',
                                        author=cls.author1)

        cls.book2 = Book.objects.create(title='The book by Jane A',
                                        editor='B',
                                        author=cls.author2)

        cls.book3 = Book.objects.create(title='The book by Jane B',
                                        editor='B',
                                        author=cls.author2)

        cls.book4 = Book.objects.create(title='The book by Alice',
                                        editor='A',
                                        author=cls.author1)

    def test_filtered_relation_wo_join(self):
        self.assertQuerysetEqual(
            Author.objects
            .filtered_relation(
                'book', alias='book_alice',
                condition=Q(book__title__iexact='poem by alice')),
            ["<Author: Alice>", "<Author: Jane>"])

    def test_filered_relation_with_join(self):
        self.assertQuerysetEqual(
            Author.objects
            .filtered_relation(
                'book', alias='book_alice',
                condition=Q(book__title__iexact='poem by alice'))
            .filter(book_alice__isnull=False),
            ["<Author: Alice>"])

    def test_filtered_relation_alias_mapping(self):
        queryset = (Author.objects
                    .filtered_relation(
                        'book', alias='book_alice',
                        condition=Q(book__title__iexact='poem by alice'))
                    .filter(book_alice__isnull=False))
        self.assertIn('INNER JOIN "filtered_relation_book" book_alice ON', str(queryset.query))

    def test_filtered_relation_with_multiple_filter(self):
        self.assertQuerysetEqual(
            Author.objects
            .filtered_relation('book', alias='book_editor_a',
                               condition=Q(book__title__icontains='book',
                                           book__editor='A'))
            .filter(book_editor_a__isnull=False),
            ["<Author: Alice>"])

    def test_exclude_relation_with_join(self):
        self.assertQuerysetEqual(
            Author.objects
            .filtered_relation(
                'book', alias='book_alice',
                condition=~Q(book__title__icontains='alice'))
            .filter(book_alice__isnull=False)
            .distinct(),
            ["<Author: Jane>"])
