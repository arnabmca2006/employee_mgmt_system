from abc import ABC
from ems.util.db_operations import DBConnect


class BaseLayer(ABC):

    def __init__(self):
        """
        default initialization
        """
        self.db_ob = DBConnect()
