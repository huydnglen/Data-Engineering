# class Employee:
#     def __init__(self, name, salary):
#         self.name = name
#         self.salary = salary
#
#     def display_info(self):
#         print(f"Employee: {self.name}, Salary: {self.salary}")
#
# #Tạo đối tượng
# emp1 = Employee("Alice", 5000)
# emp2 = Employee("Bob", 7000)
#
# #hiển thị thông tin
# emp1.display_info()
# emp2.display_info()

# class Rectangle:
#     def __init__(self, width, height):
#         self.width = width
#         self.height = height
#
#     def area(self):
#         s = self.width*self.height
#         print(f"Dien tich là: {s}")
#     def perimeter(self):
#         c = (self.width + self.height)*2
#         print(f"Chu vi là: {c}")
#
# #Tạo đối tượng
# w = float(input("Nhập chiều rộng: "))
# h = float(input("Nhập chiều dài: "))
#
# rect = Rectangle(w, h)
#
# rect.area()
# rect.perimeter()

# class Student:
#     def __init__(self, name, score):
#         self.name = name
#         self.score = score
#     def is_passed(self):
#         return self.score >= 5
#
# # Danh sách sinh viên
# students = [
#     Student("An", 7),
#     Student("Bình", 4),
#     Student("Cường", 6)
# ]
#
# passed_students = [s.name for s in students if s.is_passed()]
# print("Sinh vien qua mon: ", passed_students)

# class Bankaccount:
#     def __init__(self, owner, balance):
#         self.owner = owner
#         self.balance = balance
#
#     def deposit(self, amount):
#         self.balance += amount
#         print(f"{self.owner} gui {amount} vao tai khoan.")
#     def widthdraw(self, amount):
#         if self.balance >= amount:
#             self.balance -= amount
#             print(f"{self.owner} da rut {amount}.")
#         else:
#             print("So du khong du")
#     def display_balance(self):
#         print(f"So du cua tai khoan la {self.balance}")
#
# acc = Bankaccount("nguyen van A", 1000)
# acc.deposit(500)
# acc.widthdraw(2000)
# acc.display_balance()

# class Book:
#     def __init__(self, title, author, year):
#         self.title = title
#         self.author = author
#         self.year = year
#     def display_info(self):
#         print(f"{self.title} - {self.author} - {self.year}")
# class Library:
#     def __init__(self):
#         self.books = []
#     def add_book(self, book):
#         self.books.append(book)
#     def display_book(self):
#         if not self.books:
#             print("Thu vien chua co sach")
#         else:
#             print("Danh sach sach trong thu vien: ")
#             for book in self.books:
#                 book.display_info()
#
# #tao sach va thu vien
# lib = Library()
# lib.add_book(Book("Python Basics", "John Doe", 2020))
# lib.add_book(Book("Machine Learning", "Andrew Ng", 2021))
# lib.display_book()

# class Person:
#     def __init__(self, name, age, gender):
#         self.name = name
#         self.age = age
#         self.gender = gender
#
#     def display_info(self):
#         print(f"Name: {self.name}, Age: {self.age}, Gender: {self.gender}")
#
# class Employee(Person):
#     def __init__(self, name, age, gender, salary, department):
#         super().__init__(name, age, gender)
#         self.salary = salary
#         self.department = department
#     def display_info(self):
#         super().display_info()
#         print(f"Salary: {self.salary}, Department: {self.department}")
#     def increase_salary(self, percent):
#         self.salary += self.salary * (percent/100)
#
# #tao danh sasch nhan vien
# employees = [
#     Employee("Alice", 30, "Female", 5000, "IT"),
#     Employee("Bob", 40, "Male", 7000, "HR"),
# ]
#
# # Tăng lương 10%
# for emp in employees:
#     emp.increase_salary(10)
#
# # Hiển thị thông tin sau khi tăng lương
# print("\nAfter salary increase:")
# for emp in employees:
#     emp.display_info()

class Flight:
    def __init__(self, flight_number, destination, seats_available):
        self.flight_number = flight_number
        self.destination = destination
        self.seats_available = seats_available
    def book_ticket(self):
        if self.seats_available > 0:
            self.seats_available -= 1
            return True
        else:
            return False

    def display_info(self):
        print(f"Flight {self.flight_number} to {self.destination} | Seats available: {self.seats_available}")

class Passenger:
    def __init__(self, name):
        self.name = name
        self.ticket_booked = False

    def book_flight(self, flight):
        if flight.book_ticket():
            self.ticket_booked = True
            print(f"{self.name} successfully booked a ticket on {flight.flight_number}")
        else:
            print(f"Sorry, {self.name}. No seats available on {flight.flight_number}")

flight1 = Flight("VN123", "Hà Nội", 2)

# Tạo hành khách và đặt vé
p1 = Passenger("John")
p2 = Passenger("Alice")
p3 = Passenger("Bob")

# Thử đặt vé
p1.book_flight(flight1)
p2.book_flight(flight1)
p3.book_flight(flight1)  # Không còn vé

# Hiển thị thông tin chuyến bay
flight1.display_info()