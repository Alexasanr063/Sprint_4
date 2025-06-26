import pytest
from main import BooksCollector

class TestBooksCollector:

    @pytest.fixture
    def collector(self):
        return BooksCollector()

    # Параметризованные тесты для add_new_book
    @pytest.mark.parametrize('name, expected', [
        ('Война и мир', True),
        ('X' * 40, True),
        ('', False),
        ('X' * 41, False)
    ])
    def test_add_new_book_valid(self, collector, name, expected):
        collector.add_new_book(name)
        assert (name in collector.get_books_genre()) == expected

    @pytest.mark.parametrize('invalid_input', [None, 42, [], {}])
    def test_add_new_book_invalid_types(self, collector, invalid_input):
        try:
            collector.add_new_book(invalid_input)
            # Если не возникло исключение, проверяем что книга не добавилась
            assert invalid_input not in collector.get_books_genre()
        except (TypeError, AttributeError):
            # Ожидаемое поведение для неподдерживаемых типов
            pass

    # Тесты для set_book_genre и get_book_genre
    def test_set_and_get_book_genre(self, collector):
        collector.add_new_book('1984')
        collector.set_book_genre('1984', 'Фантастика')
        assert collector.get_book_genre('1984') == 'Фантастика'

    def test_set_book_genre_with_invalid_genre(self, collector):
        collector.add_new_book('Книга')
        collector.set_book_genre('Книга', 'Несуществующий жанр')
        assert collector.get_book_genre('Книга') == ''

    # Тест для get_books_with_specific_genre
    def test_get_books_with_specific_genre(self, collector):
        collector.add_new_book('Шерлок Холмс')
        collector.add_new_book('Пуаро')
        collector.set_book_genre('Шерлок Холмс', 'Детективы')
        collector.set_book_genre('Пуаро', 'Детективы')
        assert set(collector.get_books_with_specific_genre('Детективы')) == {'Шерлок Холмс', 'Пуаро'}

    # Тест для get_books_genre
    def test_get_books_genre(self, collector):
        collector.add_new_book('Книга1')
        collector.add_new_book('Книга2')
        assert collector.get_books_genre() == {'Книга1': '', 'Книга2': ''}

    # Параметризованные тесты для get_books_for_children
    @pytest.mark.parametrize('genre, expected', [
        ('Фантастика', True),
        ('Ужасы', False),
        ('Комедии', True),
        ('Несуществующий', False)
    ])
    def test_get_books_for_children(self, collector, genre, expected):
        collector.add_new_book('Детская книга')
        collector.set_book_genre('Детская книга', genre)
        assert ('Детская книга' in collector.get_books_for_children()) == expected

    # Тесты для работы с избранным
    def test_add_and_get_favorites(self, collector):
        collector.add_new_book('Избранная книга')
        collector.add_book_in_favorites('Избранная книга')
        assert 'Избранная книга' in collector.get_list_of_favorites_books()

    def test_add_not_existing_book_to_favorites(self, collector):
        collector.add_book_in_favorites('Несуществующая книга')
        assert 'Несуществующая книга' not in collector.get_list_of_favorites_books()

    def test_delete_from_favorites(self, collector):
        collector.add_new_book('Книга')
        collector.add_book_in_favorites('Книга')
        collector.delete_book_from_favorites('Книга')
        assert 'Книга' not in collector.get_list_of_favorites_books()