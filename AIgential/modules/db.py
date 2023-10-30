import psycopg2

class PostgresDB:
    def __init__(self):
        self.conn = None
        self.cur = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def connect_with_url(self, url):
        self.conn = psycopg2.connect(url)
        self.cur = self.conn.cursor()

    def upsert(self, table_name, _dict):
        columns = _dict.keys()
        values = tuple(_dict.values())
        query = f"INSERT INTO {table_name} ({','.join(columns)}) VALUES ({','.join(['%s']*len(values))}) ON CONFLICT (id) DO UPDATE SET {','.join([f'{col}=EXCLUDED.{col}' for col in columns if col != 'id'])}"
        self.cur.execute(query, values)
        self.conn.commit()

    def delete(self, table_name, _id):
        query = f"DELETE FROM {table_name} WHERE id = %s"
        self.cur.execute(query, (_id,))
        self.conn.commit()

    def get(self, table_name, _id):
        query = f"SELECT * FROM {table_name} WHERE id = %s"
        self.cur.execute(query, (_id,))
        return self.cur.fetchone()

    def get_all(self, table_name):
        query = f"SELECT * FROM {table_name}"
        self.cur.execute(query)
        return self.cur.fetchall()

    def run_sql(self, sql):
        self.cur.execute(sql)
        return self.cur.fetchall()

    def get_table_definitions(self, table_name):
        query = f"SELECT column_name, data_type FROM information_schema.columns WHERE table_name = '{table_name}'"
        self.cur.execute(query)
        columns = self.cur.fetchall()
        return_val = f"CREATE TABLE {table_name} ({','.join([f'{col[0]} {col[1]}' for col in columns])});"
        return return_val

    def get_all_table_names(self):
        query = "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' AND table_type = 'BASE TABLE'"
        self.cur.execute(query)
        return_val = [table[0] for table in self.cur.fetchall()]
        return return_val

    def get_table_definitions_for_prompt(self):
        table_defs = [self.get_table_definitions(table_name) for table_name in self.get_all_table_names()]
        return_val = '\n'.join(table_defs)
        return return_val

    def close(self):
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close()