import json

# Класс для представления книги
class Book:
    def __init__(self, title, author, year, genre):
        self.title = title
        self.author = author
        self.year = year
        self.genre = genre

    def __str__(self):
        return f"{self.title} автор: {self.author} ({self.year}) - жанр: {self.genre}"

    def __eq__(self, other):
        return (
            self.title == other.title
            and self.author == other.author
            and self.year == other.year
            and self.genre == other.genre
        )

# Класс для представления читателя
class Reader:
    def __init__(self, name, reader_id):
        self.name = name
        self.reader_id = reader_id
        self.borrowed_books = []

    def borrow_book(self, book):
        self.borrowed_books.append(book)

    def return_book(self, book):
        if book in self.borrowed_books:
            self.borrowed_books.remove(book)
        else:
            raise ValueError("Эта книга не была взята данным читателем.")

    def __str__(self):
        return f"{self.name} (ID: {self.reader_id})"

# Класс для управления библиотекой
class Library:
    def __init__(self, name):
        self.name = name
        self.books = []
        self.readers = []

    def add_book(self, book):
        self.books.append(book)

    def remove_book(self, book):
        if book in self.books:
            self.books.remove(book)
        else:
            raise ValueError("Этой книги нет в библиотеке.")

    def register_reader(self, reader):
        self.readers.append(reader)

    def lend_book(self, reader_id, book_title):
        reader = self.find_reader_by_id(reader_id)
        book = self.find_book_by_title(book_title)
        if book and book in self.books:
            reader.borrow_book(book)
            self.books.remove(book)
        else:
            raise ValueError("Книга недоступна для выдачи.")

    def return_book(self, reader_id, book_title):
        reader = self.find_reader_by_id(reader_id)
        book = self.find_book_by_title(book_title)
        if book:
            reader.return_book(book)
            self.books.append(book)
        else:
            raise ValueError("Эта книга не была взята данным читателем.")

    def find_book_by_title(self, title):
        for book in self.books:
            if book.title == title:
                return book
        return None

    def find_reader_by_id(self, reader_id):
        for reader in self.readers:
            if reader.reader_id == reader_id:
                return reader
        return None

    def get_reader_books(self, reader_id):
        reader = self.find_reader_by_id(reader_id)
        if reader:
            return reader.borrowed_books
        else:
            raise ValueError("Читатель не найден.")

    def save_to_file(self, filename):
        data = {
            "name": self.name,
            "books": [
                {"title": book.title, "author": book.author, "year": book.year, "genre": book.genre}
                for book in self.books
            ],
            "readers": [
                {
                    "name": reader.name,
                    "reader_id": reader.reader_id,
                    "borrowed_books": [
                        {"title": book.title, "author": book.author, "year": book.year, "genre": book.genre}
                        for book in reader.borrowed_books
                    ],
                }
                for reader in self.readers
            ],
        }
        with open(filename, "w") as f:
            json.dump(data, f)

    def load_from_file(self, filename):
        with open(filename, "r") as f:
            data = json.load(f)
        self.name = data["name"]
        self.books = [Book(**book_data) for book_data in data["books"]]
        self.readers = []
        for reader_data in data["readers"]:
            reader = Reader(reader_data["name"], reader_data["reader_id"])
            reader.borrowed_books = [Book(**book_data) for book_data in reader_data["borrowed_books"]]
            self.readers.append(reader)

def main():
    library = Library("Городская библиотека")

    while True:
        print("\nМеню:")
        print("1. Добавить книгу")
        print("2. Удалить книгу")
        print("3. Зарегистрировать читателя")
        print("4. Выдать книгу читателю")
        print("5. Принять книгу от читателя")
        print("6. Поиск книги по названию")
        print("7. Показать книги, взятые читателем")
        print("8. Сохранить библиотеку в файл")
        print("9. Загрузить библиотеку из файла")
        print("0. Выход")

        choice = input("Выберите действие: ")

        try:
            if choice == "1":
                title = input("Введите название книги: ")
                author = input("Введите автора книги: ")
                year = int(input("Введите год издания книги: "))
                genre = input("Введите жанр книги: ")
                book = Book(title, author, year, genre)
                library.add_book(book)
                print("Книга добавлена.")

            elif choice == "2":
                title = input("Введите название книги для удаления: ")
                book = library.find_book_by_title(title)
                if book:
                    library.remove_book(book)
                    print("Книга удалена.")
                else:
                    print("Книга не найдена.")

            elif choice == "3":
                name = input("Введите имя читателя: ")
                reader_id = input("Введите ID читателя: ")
                reader = Reader(name, reader_id)
                library.register_reader(reader)
                print("Читатель зарегистрирован.")

            elif choice == "4":
                reader_id = input("Введите ID читателя: ")
                book_title = input("Введите название книги для выдачи: ")
                library.lend_book(reader_id, book_title)
                print("Книга выдана читателю.")

            elif choice == "5":
                reader_id = input("Введите ID читателя: ")
                book_title = input("Введите название книги для возврата: ")
                library.return_book(reader_id, book_title)
                print("Книга возвращена в библиотеку.")

            elif choice == "6":
                title = input("Введите название книги для поиска: ")
                book = library.find_book_by_title(title)
                if book:
                    print("Книга найдена:", book)
                else:
                    print("Книга не найдена.")

            elif choice == "7":
                reader_id = input("Введите ID читателя: ")
                books = library.get_reader_books(reader_id)
                print("Книги, взятые читателем:")
                for book in books:
                    print(book)

            elif choice == "8":
                filename = input("Введите имя файла для сохранения: ")
                library.save_to_file(filename)
                print("Данные библиотеки сохранены.")

            elif choice == "9":
                filename = input("Введите имя файла для загрузки: ")
                library.load_from_file(filename)
                print("Данные библиотеки загружены.")

            elif choice == "0":
                print("Выход из программы.")
                break
            else:
                print("Неверный выбор. Попробуйте еще раз.")

        except ValueError as e:
            print("Ошибка:", e)

if __name__ == "__main__":
    main()
