library =[]

def add_book(name, author, year):
    book = {
        "name": name,
        "author": author,
        "year": year
    }
    library.append(book)
    print(f"Đã thêm sách: {name} của tác giả {author} ({year}) thành công.")

def search_book_by_name(name):
    founds_books = [book for book in library if name.lower() in book["name"].lower()]
    if founds_books:
        for book in founds_books:
            print(f"{book['name']} - {book['author']} - {book['year']}")
    else:
        print("không tìm thấy sách")

def search_book_by_author(author):
    founds_books = [book for book in library if author.lower() in book["author"].lower()]
    if founds_books:
        for book in founds_books:
            print(f"{book['name']} - {book['author']} - {book['year']}")
    else:
        print("không tìm thấy sách")

def delete_book(name):
    global library
    library = [book for book in library if book["name"].lower() != name.lower()]
    print(f"Đã xóa sách {name} khỏi thư viện")

def update_book(name, new_name =None, new_author =None, new_year =None):
    for book in library:
        if book["name"].lower() == name.lower():
            if new_name:
                book["name"] = new_name
            if new_author:
                book["author"] = new_author
            if new_year:
                book["year"] = new_year
            print(f"Đã cập nhật sách: {book['name']} - {book['author']} - {book['year']}")
        else:
            print("Không tìm thấy sách")

def display_book():
    if library:
        for book in library:
            print("Name book - Author - Year")
            print(f"{book['name']} - {book['author']} - {book['year']}")
    else:
        print("Thư viện không có sách nào.")


def menu():
    while True:
        print("\n----------Quản lý thư viện sách------------")
        print("1. Thêm sách")
        print("2. Tìm sách theo tên")
        print("3. Tìm sách theo tên tác giả")
        print("4. Cập nhật sách bằng tên")
        print("5. Xóa sách")
        print("6. Hiển thị tất cả sách")
        print("7. Thoát")
        choice = input("Lựa chọn chức năng (1 - 7): ")

        if choice == "1":
            name = input("Nhập tên sách: ")
            author = input("Nhập tên tác giả: ")
            year = input("Nhập năm xuất bản: ")
            add_book(name,author, year)
        elif choice == "2":
            name = input("Nhập tên sách: ")
            search_book_by_name(name)
        elif choice == "3":
            author = input("Nhập tên tác giả: ")
            search_book_by_author(author)
        elif choice == "4":
            name = input("Nhập tên sách: ")
            new_name = input("Nhập tên sách mới: ")
            new_author = input("Nhập tên tác giả mới: ")
            new_year = input("Nhập năm xuất bản mới: ")
            update_book(new_name, new_author, new_year)
        elif choice == "5":
            name = input("Nhập tên sách: ")
            delete_book(name)
        elif choice == "6":
            display_book()
        elif choice == "7":
            print("Thoát khỏi chường trình")
            break
        else:
            print("Lựa chọn không hợp lệ")

menu()