class SqlExtractor:
    def __init__(self, connection):
        self.connection = connection

    def get_data(self, data_class, table: str, batch_size: int = 100):
        curs = self.connection.cursor()
        curs.execute(f"SELECT * FROM {table};")

        while True:
            batch = curs.fetchmany(batch_size)
            if not batch:
                break
            rows = []
            for b in batch:
                row = data_class(**b)
                rows.append(row)
            yield rows
