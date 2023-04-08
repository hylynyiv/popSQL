import sqlite3

class DB:
    def __init__(self, db: str = None) -> None:
        self.db = db


    def decor(func):
        def sql(self, *args):
            """'create' requires 2 arguments: table, columns.
                F.i. create("users", ("id", "name"))

            'insert' requires 2 arguments: table, columns.
                F.i. insert("users", ("01", "Garfield"))

            'delete' requires 3 arguments: table, column, value.
                F.i. delete("users", "name", "Garfield")

            'update' requires 5 arguments: table, s_column, s_value, w_column, w_value.
                F.i. update("users", "id", "02", "name", "Garfield")
                I.e. change "id" to "02" where "name" is "Garfield".

            'view' requires 1 argument: table.
                F.i. view("users")
                """

            self.conn = sqlite3.connect(self.db)
            self.cur = self.conn.cursor()
            self.cur.execute(func(self, *args))
            try: rows = self.cur.fetchall()
            except: pass
            self.conn.commit()
            self.conn.close()
            if rows: return rows
        return sql


    @decor
    def create(self,
                table: str,
                columns: tuple[str, int, list, dict, tuple, set]) -> str:
        return f"CREATE TABLE IF NOT EXISTS {table} {columns};"    

    @decor
    def insert(self,
                table: str,
                data: tuple) -> str:
        return f"INSERT INTO {table} VALUES {data}"

    @decor
    def delete(self,
                table: str,
                column: str,
                value) -> str:
        if type(value)==str: value = f"'{value}'"
        return f"DELETE FROM {table} WHERE {column} = {value};"

    @decor
    def update(self,
                table: str,
                s_column: str,
                s_value,
                w_column: str,
                w_value) -> str:
        if type(w_value)==str: w_value = f"'{w_value}'"
        if type(s_value)==str: s_value = f"'{s_value}'"
        return f"UPDATE {table} SET {s_column}={s_value} WHERE {w_column}={w_value};"

    @decor
    def view(self,
            table: str) -> str:
        return f"SELECT * FROM {table};"
