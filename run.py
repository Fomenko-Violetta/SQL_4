
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Animal, Product, Customer, Order, OrderDetail
from sqlalchemy.orm import joinedload, lazyload

# Підключення до бази даних через зазначену конект-стрічку
DATABASE_URL = "mysql+pymysql://avnadmin:AVNS_hyEK_ZTRmq86zeLCAa4@mysql-32c408f5-ladbsbd.g.aivencloud.com:27163/Zooshop"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

# Функція для створення таблиць у БД
def create_database():
    Base.metadata.create_all(engine)
    print("База даних створена або оновлена.")

def create_database():
    Base.metadata.create_all(engine)
    print("База даних створена або оновлена.")

# Функція для виведення даних з усіх таблиць
def display_table_data():
    print("\nТварини:")
    animals = session.query(Animal).all()
    for animal in animals:
        print(f"ID: {animal.AnimalID}, Name: {animal.Name}, Type: {animal.Type}, Age: {animal.Age}, Price: {animal.Price}")

    print("\nПродукти:")
    products = session.query(Product).all()
    for product in products:
        print(f"ID: {product.ProductID}, Name: {product.Name}, Category: {product.Category}, Quantity: {product.Quantity}, Price: {product.Price}")

    print("\nКористувачі:")
    customers = session.query(Customer).all()
    for customer in customers:
        print(f"ID: {customer.CustomerID}, Name: {customer.Name}, Phone: {customer.Phone}, Email: {customer.Email}, City: {customer.City}")

    print("\nЗамовлення:")
    orders = session.query(Order).all()
    for order in orders:
        print(f"Order ID: {order.OrderID}, Customer ID: {order.CustomerID}, Order Date: {order.OrderDate}, Total Amount: {order.TotalAmount}")

    print("\nДеталі замовлень:")
    order_details = session.query(OrderDetail).all()
    for detail in order_details:
        print(f"OrderDetailID: {detail.OrderDetailID}, OrderID: {detail.OrderID}, ProductID: {detail.ProductID}, Quantity: {detail.Quantity}, Price: {detail.Price}")

# Функція для демонстрації Lazy Loading
def display_lazy_loading():
    print("\nLazy Loading - Продукти:")
    products = session.query(Product).all()  # Дані завантажуються лише при зверненні до атрибутів
    for product in products:
        print(f"ID: {product.ProductID}, Name: {product.Name}, Category: {product.Category}")

def display_eager_loading():
    print("\nEager Loading - Замовлення з деталями:")
    orders = session.query(Order).options(joinedload(Order.details)).all()
    for order in orders:
        print(f"Order ID: {order.OrderID}, Total: {order.TotalAmount}")
        for detail in order.details:
            print(f"  Product ID: {detail.ProductID}, Quantity: {detail.Quantity}")

# Функція для демонстрації Explicit Loading
def display_explicit_loading():
    print("\nExplicit Loading - Користувачі та їх замовлення:")
    customers = session.query(Customer).options(joinedload(Customer.orders)).all()
    for customer in customers:
        print(f"Customer ID: {customer.CustomerID}, Name: {customer.Name}")
        for order in customer.orders:
            print(f"  Order ID: {order.OrderID}, Total: {order.TotalAmount}")

# Запит, що виконує агрегацію, сортування та фільтрацію
def aggregate_query():
    print("\nАгрегація, сортування та фільтрація - Топ продукти за ціною:")
    top_products = (session.query(Product)
                    .filter(Product.Price > 20)
                    .order_by(Product.Price.desc())
                    .limit(5)
                    .all())
    for product in top_products:
        print(f"ID: {product.ProductID}, Name: {product.Name}, Price: {product.Price}")

# Додати нові функції до меню
def menu():
    while True:
        print("\nМеню:")
        print("1. Вивести дані таблиць")
        print("2. Lazy Loading (Продукти)")
        print("3. Eager Loading (Замовлення)")
        print("4. Explicit Loading (Користувачі)")
        print("5. Агрегація, сортування та фільтрація")
        print("0. Вихід")

        choice = input("Оберіть опцію: ")

        if choice == "1":
            display_table_data()
        elif choice == "2":
            display_lazy_loading()
        elif choice == "3":
            display_eager_loading()
        elif choice == "4":
            display_explicit_loading()
        elif choice == "5":
            aggregate_query()
        elif choice == "0":
            print("Вихід з програми.")
            break
        else:
            print("Невірний вибір. Спробуйте ще раз.")

if __name__ == "__main__":
    create_database()
    menu()
