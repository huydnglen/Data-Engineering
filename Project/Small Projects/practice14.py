# customers = [
#     {"name": "Alice", "age": 25, "spending": 500},
#     {"name": "Bob", "age": 30, "spending": 700},
#     {"name": "Charlie", "age": 22, "spending": 200},
#     {"name": "David", "age": 30, "spending": 1000},
#     {"name": "Eve", "age": 25, "spending": 300}
# ]
#
# filterdf = list(filter(lambda x:x["age"]>25 , customers))
# arrange = list(sorted(customers, key = lambda x: x["spending"], reverse=True))
# namelist = list(map(lambda x:x["name"], customers))
# agelist = set(map(lambda x:x["age"], customers))
# print(map(lambda x:x["age"], customers))

# products = [
#     ("Laptop", 1200, 5),
#     ("Smartphone", 800, 10),
#     ("Tablet", 500, 8),
#     ("Monitor", 300, 12),
#     ("Keyboard", 50, 30),
#     ("Mouse", 30, 50)
# ]
# arrange = list(sorted(products, key= lambda x:x[1], reverse=False))
# filproduct = list(filter(lambda x:x[1]>500, products))
# namelst = list(map(lambda x:x[0], products))
# total = list(map(lambda x:x[1]*x[2], products))
# sort = list(sorted(products, key = lambda x:x[1], reverse=True))
# most_expensive = max(products, key=lambda x: x[1])
# print(most_expensive)

# students = [
#     ("Alice", 85, 90, 88),
#     ("Bob", 70, 65, 80),
#     ("Charlie", 95, 100, 92),
#     ("David", 60, 75, 70),
#     ("Eve", 80, 85, 78)
# ]
# # 1. Tính điểm trung bình của từng sinh viên
# students_avg = list(map(lambda x: (x[0], (x[1] + x[2] + x[3]) / 3), students))
# diem = list(map(lambda x:(x[1]+x[2]+x[3])/3, students))
# sapxep = sorted(map(lambda x:(x[1]+x[2]+x[3])/3, students), reverse=True)
# top = max(students_avg,key =lambda x:x[1])
# fil = list(filter(lambda x:x[1]>80, students_avg))
# namlst = list(map(lambda x:x[0], students))
# print(namlst)

from collections import Counter
text = "Python is great. Python is powerful. Python is used in data science, machine learning, and web development."

# 1. Tách thành danh sách từ
words = text.replace(".", "").replace(",", "").split()

# 2. Chuyển về chữ thường
words_lower = list(map(str.lower, words))

# 3. Tạo tập hợp từ duy nhất
unique_words = set(words_lower)

# 4. Đếm số lần xuất hiện của từng từ
word_counts = Counter(words_lower)

# 5. Sắp xếp từ theo số lần xuất hiện giảm dần
sorted_word_counts = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)

print(words_lower)
print(unique_words)
print(word_counts)
print(sorted_word_counts)


