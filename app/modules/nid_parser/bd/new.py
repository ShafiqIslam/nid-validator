from app.modules.nid_parser.bd.enums import Side
from app.modules.nid_parser.nid_parser import NIDParser


class NewNidParser(NIDParser):

    def __init__(self, side=Side.FRONT.value):
        super().__init__(side)

    def preprocess(self, data):
        return data

    def parse_back_data(self, data):
        pass

    def parse_front_data(self, data):
        return data
