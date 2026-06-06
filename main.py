import sqlite3

con = sqlite3.connect(store.db)
cursor = con.cursor()

cursor.execute(""" CREATE TABLE products ( 
    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    price REAL NOT NULL)
""" );

cursor.execute(""" CREATE TABLE customers ( 
  customer_id INTEGER PRIMARY KEY AUTOINCREMENT, 
  first_name TEXT NOT NULL, 
  last_name TEXT NOT NULL, 
  email TEXT NOT NULL UNIQUE) 
""" );

cursor.execute(""" CREATE TABLE orders ( 
  order_id INTEGER PRIMARY KEY AUTOINCREMENT, 
  customer_id INTEGER NOT NULL, 
  product_id INTEGER NOT NULL, 
  quantity INTEGER NOT NULL, 
  order_date DATE NOT NULL, 
  FOREIGN KEY (customer_id) REFERENCES customers(customer_id), 
  FOREIGN KEY (product_id) REFERENCES products(product_id))
""" );

while True:
  print("\n1. Додати товар")
  print("2. Додати клієнта")
  print("3. Створити замовлення")
  print("4. Показати товари")
  print("5. Показати клієнтів")
  print("6. Показати замовлення")
  print("7. Підвищити ціни смартфонів на 10%")
  print("8. Загальний обсяг продажів")
  print("9. Кількість замовлень кожного клієнта")
  print("10. Середній чек")
  print("11. Найпопулярніша категорія")
  print("12. Кількість товарів по категоріях")
  print("13. Вийти")
  
  choice = input("Оберіть пункт: ")
  
  if choice == "1":
    name = input("Введіть назву товару: ")
    category = input("Введіть категорію товару: ")
    price = input("Ввести ціну: ")

    cursor.execute("INSERT INTO products (name, category, price) VALUES (?, ?, ?)", (name, category, price))
    cursor.commit()

  if choice == "2":
    name = input("Введіть ім'я: ")
    lastname = input("Введіть прізвище: ")
    email = input("Введіть імейл: ")

    cursor.execute("INSERT INTO customers (firstname, lastname, email) VALUES (?, ?, ?)", (name, lastname, email))
    cursor.commit()

  if choice == "3":
    customer_id = input("Введіть айді: ")
    product_id = input("Введіть айді продукту: ")
    quantity = input("Введіть кількість продукту: ")

    cursor.execute("INSERT INTO orders (customer_id, product_id, quantity) VALUES (?, ?, ?)", (customer_id, product_id, quantity))
    cursor.commit()

  if choice == "4":
    cursor.execute("SELECT * FROM products")
    for product in cursor.fetchall():
      print(product)
  
  if choice == "5":
    cursor.execute("SELECT * FROM customers")
    for customer in cursor.fetchall():
      print(customer)

  if choice == "6":
    cursor.execute("SELECT * FROM orders")
    for order in cursor.fetchall():
      print(order)

  if choice == "7":
    cursor.execute("UPDATE products SET price = price * 1.1 WHERE category = 'smartphons' ")
    safe = input("Чи зберігти зміни?(так/ні): ")

    if safe.lower() == "так":
      con.commit()
    else:
      con.rollback()

  if choice == "8":
    cursor.execute(""" SELECT SUM(products.price * orders.quantity) 
                  FROM orders 
                  INNER JOIN products
                  ON orders.product_id = products.product_id""")
    total = cursor.fetchone()[0]
    
  if choice == "9":
    cursor.execute(""" SELECT customers.first_name, customers.last_name, COUNT(orders.order_id), 
                  FROM customers
                  INNER JOIN orders
                  ON customers.customer_id = orders.customer_id 
                  GROUP BY customers.customer_id""")
    results = cursor.fetchall()

    for i in results:
      print(f"{i[0]} {i[1]} - {i[2]} замовлень")
  
  if choice == "10":
    cursor.execute(""" SELECT AVG(products.price * orders.quantity)
                  FROM orders
                  INNER JOIN products
                  ON orders.product_id = products.product_id""")
    check = cursor.fetchone()[0]

  if choice == "11":
    cursor.execute(""" SELECT products.category, COUNT(*)
                  FROM orders
                  INNER JOIN products
                  ON orders.product_id = products.product_id
                  GROUP BY products.category
                  ORDER BY COUNT(*) DESC 
                  LIMIT 1""")
    category = cursor.fetchone()[0]
    print(category)

  if choice == "12":
    cursor.execute(""" SELECT category, COUNT(*)
                  FROM products
                  GROUP BY category""")
    results = cursor.fetchall()[0]
    print(results)

  if choice == "13":
    break
    
con.close()
