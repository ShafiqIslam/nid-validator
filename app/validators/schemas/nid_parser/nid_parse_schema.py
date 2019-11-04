import typing

from marshmallow import Schema, fields, INCLUDE, validates, pre_load

from app.common import Request
from app.common.exceptions import InvalidRequestException
from app.common.helpers import log
from app.modules.nid_parser import BDNIDParser
from app.modules.nid_parser.bd.enums import Format, Side
from app.modules.nid_parser.exceptions.invalids import FormatNotExcepted
from app.modules.ocr.exceptions import FileNotSelectedException


class FILE(fields.Field):
    pass


def validateFormat(value):
    value = value.strip()
    if Format.has_value(value):
        return value
    else:
        raise InvalidRequestException('Format is invalid')


def validateSide(value):
    log(value)
    value = value.strip()
    if Side.has_value(value):
        return value
    else:
        raise InvalidRequestException('Side is invalid')


class FormatField(fields.Field):
    def _deserialize(
            self,
            value: typing.Any,
            attr: typing.Optional[str],
            data: typing.Optional[typing.Mapping[str, typing.Any]],
            **kwargs
    ):
        return validateFormat(value)


class SideField(fields.Field):
    def _deserialize(
            self,
            value: typing.Any,
            attr: typing.Optional[str],
            data: typing.Optional[typing.Mapping[str, typing.Any]],
            **kwargs
    ):
        return validateSide(value)


class NidParseSchema(Schema):
    format = FormatField(required=True)
    side = SideField(required=True)
    nid_image = FILE()

    class Meta:
        unknown = INCLUDE

    @pre_load
    def nid_image_validation(self, data, many, **kwargs):
        try:
            nid_image = Request.files['nid_image']

            if nid_image.filename == '':
                raise FileNotSelectedException()
            if nid_image and not BDNIDParser.allowed(nid_image.filename):
                raise FormatNotExcepted()
            data.nid_image = nid_image
            return data
        except Exception as e:
            raise e
