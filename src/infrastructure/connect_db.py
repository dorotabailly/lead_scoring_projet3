import sqlalchemy

from src.infrastructure.config.config import config


class Connexion:
    def __init__(self):
        """
        config_file : dict
                The YAML file describing the connexion configuration to postgresql
        """

        param = config["postgresql"]
        self.db_user = param["username"]
        self.db_pass = param["password"]
        self.db_hostname = param["hostname"]
        self.db_port = param["port"]
        self.db_name = param["database"]

    def engine(self):
        """
        Explanation
        -----------
        the return object should be used with pd.read_sql()

        Example
        -------
        >>> import pandas as pd
        >>> engine = Connection(CONFIG_PATH).connect()
        >>> df = pd.read_sql("SELECT * FROM table;", engine)
        """

        url = "postgresql://{0}:{1}@{2}:{3}/{4}".format(
            self.db_user, self.db_pass, self.db_hostname, self.db_port, self.db_name
        )
        engine = sqlalchemy.create_engine(url)
        return engine
