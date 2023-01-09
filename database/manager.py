import sqlite3


def setup(db_name):
    connection = sqlite3.connect(db_name + '.db')
    cursor = connection.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS items (
    item_id INTEGER PRIMARY KEY,
    item_name varchar(40) NOT NULL,
    brand varchar(40) NOT NULL,
    item_type varchar(40) NOT NULL,
    retail REAL,
    currency varchar(40)
    )   
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS websites (
    website_id INTEGER PRIMARY KEY,
    website_name varchar(40) NOT NULL
    )   
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS urls (
    url_id INTEGER PRIMARY KEY,
    item_id INTEGER NOT NULL,
    url varchar(400) NOT NULL,
    website_id INTEGER NOT NULL,
    FOREIGN KEY (item_id) REFERENCES items (item_id),
    FOREIGN KEY (website_id) REFERENCES websites (website_id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS scraped_data (
    data_id INTEGER PRIMARY KEY,
    item_id INTEGER NOT NULL,
    website_id INTEGER NOT NULL,
    price REAL, 
    currency varchar(40),
    size varchar (40),
    date varchar(100),
    FOREIGN KEY (item_id) REFERENCES items (item_id),
    FOREIGN KEY (website_id) REFERENCES websites (website_id)
    )
    """)


def add_website(db_name, website_name):
    connection = sqlite3.connect(db_name + '.db')
    with connection:
        connection.execute("INSERT INTO websites(website_name) VALUES (?)",
                           (website_name,))


def add_item(db_name, item_name, brand, item_type, retail, currency):
    connection = sqlite3.connect(db_name + '.db')
    with connection:
        connection.execute("INSERT INTO items(item_name, brand, item_type, retail, currency) VALUES (?,?,?,?,?)",
                       (item_name, brand, item_type, retail, currency))


def add_url(db_name, item_id, url, website_id):
    connection = sqlite3.connect(db_name + '.db')
    with connection:
        connection.execute("INSERT INTO urls(item_id, url, website_id) VALUES (?,?,?)",
                           (item_id, url, website_id))


def add_data(db_name, item_id, website_id, price, currency, size, date):
    connection = sqlite3.connect(db_name + '.db')
    with connection:
        connection.execute("INSERT INTO scraped_data(item_id, website_id, price, currency, size, date) VALUES (?,?,?,?,?,?)",
                           (item_id, website_id, price, currency, size, date))


def get_urls_item_id(db_name, website_id):
    connection = sqlite3.connect(db_name + '.db')
    cursor = connection.cursor()
    cursor.execute(f"SELECT url, item_id FROM urls WHERE website_id = {website_id}")
    data = cursor.fetchall()
    urls_item_id = {}
    for url_item_id in data:
        urls_item_id.update({url_item_id[0] : url_item_id[1]})
    return urls_item_id


def get_table(db_name, table_name):
    connection = sqlite3.connect(db_name + '.db')
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM {table_name}")
    table_data = cursor.fetchall()
    return table_data


def get_website_id(db_name, website_name):
    connection = sqlite3.connect(db_name + '.db')
    cursor = connection.cursor()
    cursor.execute(f"SELECT website_id FROM websites WHERE website_name = '{website_name}'")
    website_id = cursor.fetchone()
    return int(website_id[0])
