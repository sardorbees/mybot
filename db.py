import sqlite3

def init_db():
    conn = sqlite3.connect("applications.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            username TEXT,
            phone TEXT,
            site_type TEXT,
            package TEXT,
            price TEXT,
            comment TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_application(name, username, phone, site_type, package, price, comment):
    conn = sqlite3.connect("applications.db")
    c = conn.cursor()
    c.execute('''
        INSERT INTO applications (name, username, phone, site_type, package, price, comment)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (name, username, phone, site_type, package, price, comment))
    conn.commit()
    conn.close()

def get_all_applications():
    conn = sqlite3.connect("applications.db")
    c = conn.cursor()
    c.execute("SELECT * FROM applications")
    data = c.fetchall()
    conn.close()
    return data
