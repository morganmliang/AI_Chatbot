import sqlite3 as sql

conn = sql.connect('database.db')
print("Opened database successfully")

# conn.execute("""CREATE TABLE cinemas (
#         c_id INTEGER PRIMARY KEY NOT NULL, 
#         name TEXT, 
#         address TEXT, 
#         phone TEXT)


#         """)

# conn.execute("""CREATE TABLE movies (
#         c_id INTEGER, 
#         m_id INTEGER,
#         m_name TEXT, 
#         description TEXT, 
#         FOREIGN KEY(c_id) REFERENCES cinemas(c_id)
#         )
#         """)

# conn.execute("""CREATE TABLE snacks (
#         c_id INTEGER,
#         s_name TEXT, 
#         FOREIGN KEY(c_id) REFERENCES cinemas(c_id)
#         )
#         """)

# print("Tables created successfully")


# con = sql.connect("database.db")
# con.row_factory = sql.Row

# cur = con.cursor()

# cur.execute("INSERT INTO students (name,addr,city,pin) VALUES (?,?,?,?)",("jake","aus","sydney","000") )
# cur.execute("INSERT INTO students (name,addr,city,pin) VALUES (?,?,?,?)",("craig","chn","hongkong","123") )

# cur.execute("select * from students")

# rows = cur.fetchall()

# d = {}


# for row in rows:
#     d[row['name']] = {}
#     d[row['name']]['addr'] = row['addr'] 
#     d[row['name']]['city'] = row['city'] 
#     d[row['name']]['pin'] = row['pin'] 

# print(d)

conn.close()