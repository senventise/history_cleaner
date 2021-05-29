import sqlite3
from pathlib import Path


HISTORY_PATH = f"{Path.home()}/.config/chromium/Default/History"
con = sqlite3.connect(HISTORY_PATH)
cur = con.cursor()


def search(keyword: str):
    for row in cur.execute("SELECT * FROM urls;"):
        if not row[1][:6] == "chrome":
            if keyword in row[1] or keyword in row[2]:
                print(f"{row[2]} ({row[1]})")


def delete(keyword: str):
    count: int = 0
    delete_id = []
    for row in cur.execute("SELECT * FROM urls;"):
        if not row[1][:6] == "chrome":
            if keyword in row[1] or keyword in row[2]:
                count += 1
                print(f"Deleting {row[2]}", end="\n")
                delete_id.append((row[0],))
    cur.executemany("DELETE FROM urls WHERE id = ?;", delete_id)
    con.commit()
    print(f"{count} items deleted.")


HELP = """\nUSAGE:
SEARCH [keyword]

DELETE [keyword]

QUIT\n"""

try:
    while True:
        print("> ", end="")
        inp = input().strip()
        if inp.split(" ")[0].upper() == "SEARCH":
            search(inp.split(" ")[1])
        elif inp.split(" ")[0].upper() == "DELETE":
            delete(inp.split(" ")[1])
        elif inp.split(" ")[0].upper() == "QUIT":
            break
        else:
            print(HELP)
except KeyboardInterrupt:
    print("see u")
con.close()
