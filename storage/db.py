import sqlite3,json

def init():
    conn = sqlite3.connect("results.db")
    conn.execute("CREATE TABLE IF NOT EXISTS scans(target TEXT, data TEXT, report TEXT)")
    conn.commit()
    conn.close()

def save_result(target, data, report):
    init()
    conn = sqlite3.connect("results.db")
    conn.execute("INSERT INTO scans VALUES(?,?,?)", 
                 (target, json.dumps(data), report))
    conn.commit()
    conn.close()

    
