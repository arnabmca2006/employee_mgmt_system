import logging
from typing import Any
from sqlalchemy import URL, MetaData, Table, text, select, insert, update, delete
from sqlalchemy import create_engine
from sqlalchemy.exc import NoSuchTableError
from sqlalchemy.orm import sessionmaker
from ems.util.configuration import Configuration

app_config = Configuration()

class DBConnect:
    _instance = None
    _engine_created = False

    def __init__(self):
        if not self.__class__._engine_created:
            self._engine = None
            self.ssl_mode = app_config.configuration["db"].get("ssl_mode", False)
            self._create_db_engine()
            self.__class__._engine_created = True


    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance


    # def get_db_object(self):
    #     return self._instance

    def _create_db_engine(self):
        """
        This function create db engine based on the properties
        :return:
        """
        logging.info("Creating DB Engine")
        username = app_config.configuration["db"]["username"]
        password = app_config.configuration["db"]["password"]
        db_url = app_config.configuration["db"]["url"]
        db_port = app_config.configuration["db"]["port"]
        database = app_config.configuration["db"]["name"]

        ssl_root_ca = app_config.configuration["db"].get("root_ca", None)
        client_cert = app_config.configuration["db"].get("client_cert", None)
        client_key = app_config.configuration["db"].get("client_key", None)

        db_schema = app_config.configuration["db"]["schema"]
        connect_args = {'options': f'-c search_path={db_schema}'}
        if self.ssl_mode:
            connect_args.update({"sslmode": "require"})
            if client_cert and client_key:
                connect_args.update({"sslcert": client_cert, "sslkey": client_key})
            if ssl_root_ca:
                connect_args.update({"sslrootcert": ssl_root_ca})

        self._engine = create_engine(
            URL.create(drivername="postgresql+psycopg", username=username, password=password, host=db_url, database=database, port=db_port),
            connect_args=connect_args
        )
        logging.debug("Created DB engine")
        self.Session = sessionmaker(bind=self._engine)


    def execute_orm_query(self, table, joins=None, where=None, limit=None, order_by=None) -> list:
        """
        This function select data from table
        :param table:
        :param joins:
        :param where:
        :param limit:
        :param order_by:
        :return:
        """
        try:
            if type(table) is str:
                table = Table(table, MetaData(), autoload_with=self._engine)
            stmt = select(table)
            if joins:
                for join in joins:
                    stmt = stmt.select_from(join)
            if where is not None:
                stmt = stmt.where(where)
            if limit is not None:
                stmt = stmt.limit(limit)
            if order_by is not None:
                stmt = stmt.order_by(order_by)

            with self._engine.begin() as conn:
                logging.info(str(stmt))
                return conn.execute(stmt).fetchall()
        except NoSuchTableError:
            logging.error(f"Table '{table.name}' does not exist.")
            return None
        except Exception as ex:
            logging.error(f"Error while fetching data from db : {ex}")
            return None


    def execute_raw_query(self, query) -> list:
        """
        This function execute native sql query
        :param query:
        :return:
        """
        try:
            with self._engine.connect() as conn:
                res = conn.execute(text(query))
                return res.fetchall()
        except Exception as e:
            logging.error(f"Error executing raw query: {e}")


    def insert_data(self, table, values, session=None) -> Any:
        """
        This function insert data into table
        :param table:
        :param values:
        :param session:
        :return:
        """
        try:
            if type(table) is str:
                table = Table(table, MetaData(), autoload_with=self._engine)
                ins = table.insert().values(**values)
            else:
                ins = insert(table).values(**values)

            if session:
                session.execute(ins)
            else:
                with self._engine.begin() as conn:
                    res = conn.execute(ins)
                    return res
        except Exception as e:
            logging.error(f"Error inserting into table '{table}': {e}", exc_info=True)
            raise Exception(f"Error inserting into table {table} : {e}")


    def update_data(self, table, where, values, session=None) -> Any:
        """
        This function update data in a table
        :param table:
        :param where:
        :param values:
        :param session:
        :return:
        """
        try:
            if type(table) is str:
                table = Table(table, MetaData(), autoload_with=self._engine)
                update_stmt = table.update().where(text(where)).values(**values)
            else:
                update_stmt = update(table).where(where).values(**values)

            if session:
                result = session.execute(update_stmt)
            else:
                with self._engine.begin() as conn:
                    result = conn.execute(update_stmt)

            if result.rowcount == 0:
                raise Exception("There is no record with the provided parameters")
            return result
        except Exception as e:
            logging.error(f"Error updating table : {e}", exc_info=True)
            raise Exception(f"Error updating table : {str(e)}")


    def delete_data(self, table, where, session=None) -> Any:
        """
        This function delete data from table
        :param table:
        :param where:
        :param session:
        :return:
        """
        try:
            if type(table) is str:
                table = Table(table, MetaData(), autoload_with=self._engine)
                delete_stmt = table.update().where(text(where))
            else:
                delete_stmt = delete(table).where(where)

            if session:
                result = session.execute(delete_stmt)
            else:
                with self._engine.begin() as conn:
                    result = conn.execute(delete_stmt)

            if result.rowcount == 0:
                raise Exception("There is no record with the provided parameters")
            return result
        except Exception as e:
            logging.error(f"Error deleting from table '{table}': {e}", exc_info=True)
