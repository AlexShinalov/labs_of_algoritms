class Student:
    def __init__(self, id, full_name, age, room_number):
        self.id = id
        self.full_name = full_name
        self.age = age
        self.room_number = room_number

class Node:
    def __init__(self, student):
        self.student = student
        self.height = 1
        self.left = None
        self.right = None

class AVLTree:
    def height(self, node):
        if node is None:
            return 0
        return node.height

    def update_height(self, node):
        node.height = 1 + max(self.height(node.left), self.height(node.right))

    def get_balance(self, node):
        if node is None:
            return 0
        return self.height(node.left) - self.height(node.right)

    def rotate_right(self, y):
        x = y.left
        T = x.right

        x.right = y
        y.left = T

        self.update_height(y)
        self.update_height(x)

        return x

    def rotate_left(self, x):
        y = x.right
        T = y.left

        y.left = x
        x.right = T

        self.update_height(x)
        self.update_height(y)

        return y

    def rebalance(self, node):
        self.update_height(node)

        balance = self.get_balance(node)

        if balance > 1:
            if self.get_balance(node.left) < 0:
                node.left = self.rotate_left(node.left)
            return self.rotate_right(node)
        if balance < -1:
            if self.get_balance(node.right) > 0:
                node.right = self.rotate_right(node.right)
            return self.rotate_left(node)

        return node

    def insert(self, node, student):
        if node is None:
            return Node(student)

        if student.id < node.student.id:
            node.left = self.insert(node.left, student)
        elif student.id > node.student.id:
            node.right = self.insert(node.right, student)

        return self.rebalance(node)

    def find(self, node, id):
        if node is None:
            return None

        if id < node.student.id:
            return self.find(node.left, id)
        elif id > node.student.id:
            return self.find(node.right, id)
        else:
            return node.student

    def inorder_traversal(self, node, result):
        if node:
            self.inorder_traversal(node.left, result)
            result.append(node.student)
            self.inorder_traversal(node.right, result)

    def get_min_node(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current

    def delete_node(self, node, id):
        if node is None:
            return node

        if id < node.student.id:
            node.left = self.delete_node(node.left, id)
        elif id > node.student.id:
            node.right = self.delete_node(node.right, id)
        else:
            if node.left is None:
                temp = node.right
                node = None
                return temp
            elif node.right is None:
                temp = node.left
                node = None
                return temp

            temp = self.get_min_node(node.right)
            node.student = temp.student
            node.right = self.delete_node(node.right, temp.student.id)

        return self.rebalance(node)

class StudentDatabase:
    def __init__(self):
        self.root = None

    def insert(self, student):
        tree = AVLTree()
        self.root = tree.insert(self.root, student)

    def find(self, id):
        tree = AVLTree()
        return tree.find(self.root, id)

    def get_all_students(self):
        tree = AVLTree()
        result = []
        tree.inorder_traversal(self.root, result)
        return result


# Создаем базу данных студентов
database = StudentDatabase()

# Добавляем студентов
database.insert(Student(1, "Иванов Иван Иванович", 20, 101))
database.insert(Student(2, "Петров Петр Петрович", 21, 102))
database.insert(Student(3, "Сидоров Сидор Сидорович", 19, 103))
database.insert(Student(4, "Алексеев Алексей Алексеевич", 22, 104))

# Удаляем студента по ID
database.root = AVLTree().delete_node(database.root, 2)

# Печатаем оставшихся студентов
all_students = database.get_all_students()
for student in all_students:
    print(f"ID: {student.id}, ФИО: {student.full_name}, Возраст: {student.age}, Комната: {student.room_number}")
