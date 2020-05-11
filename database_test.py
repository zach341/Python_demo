import MySQLdb

db = MySQLdb.connect('10.66.99.77','root','123','test_zach', charset = 'utf8')
#db.query("CREATE DATABASE NIHAO")
cursor = db.cursor()
cursor.execute("SELECT * FROM customers")

for data in cursor.fetchall():
    print(len(data)*"%s\t"%data)
# cursor.execute("SHOW TABLES")
# #cursor.execute("")
# #cursor.execute("ALTER TABLE orderitems ADD CONSTRAINT fk_orders_customers FOREIGN KEY (order_num) REFERENCES orders (order_num)")
# #cursor.execute("ALTER TABLE orderitems ADD CONSTRAINT fk_orderitems_products FOREIGN KEY(prod_id) REFERENCES products (prod_id)")
# #cursor.execute("ALTER TABLE orders ADD CONSTRAINT fk_orders_customers2 FOREIGN KEY (cust_id) REFERENCES customers (cust_id);")
# #cursor.execute("ALTER TABLE products ADD CONSTRAINT fk_products_vendors FOREIGN KEY (vend_id) REFERENCES vendors (vend_id);")
# #cursor.execute("SHOW CREATE TABLE orderitems;")
# data = cursor.fetchall()
# # for n_data in data:
# #     for nn_data in n_data:
# #         print(nn_data)
# print(data)
db.commit()
cursor.close()