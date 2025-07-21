```python
import sqlite3
from contextlib import closing

def init_db():
    with closing(sqlite3.connect("pwnagebox.db")) as conn:
        with conn, closing(conn.cursor()) as cursor:
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                module TEXT NOT NULL,
                result TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )""")
```
