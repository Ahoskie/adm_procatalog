from pydantic import BaseModel

from models.tag import Tag
from models.attribute import Attribute
from models.product import Product
from models.brand import Brand
from services.attributes import create_attribute
from services.tags import create_tag
from services.products import create_product
from services.brands import create_brand


class DataContainer:
    data = list()
    model: BaseModel
    data_creation_function = None

    def fill_database(self):
        data = [self.model(**item) for item in self.data]
        db_items = []
        for item in data:
            db_items.append(self.data_creation_function(item))
        DataContainer.data = db_items


class AttributesData(DataContainer):
    model = Tag
    data_creation_function =
    data = [
        {
            'name': 'Attr1'
        },
        {
            'name': 'Attr2'
        },
        {
            'name': 'Attr3'
        },
        {
            'name': 'Attr4'
        },
        {
            'name': 'Attr5'
        }
    ]


class TagsData(DataContainer):

    data = [
        {
            'name': 'Tag1',
            'attrs': [
                {
                    'name': 'att1'
                },
                {
                    'name': 'att2'
                }
            ]
        },
        {
            'name': 'Tag2',
            'attrs': [
                {
                    'name': 'att3'
                },
                {
                    'name': 'att4'
                }
            ]
        },
        {
            'name': 'Tag3',
            'attrs': [
                {
                    'name': 'att2'
                },
                {
                    'name': 'att5'
                }
            ]
        },
        {
            'name': 'Tag4',
            'attrs': [
                {
                    'name': 'att3'
                },
                {
                    'name': 'att6'
                },
                {
                    'name': 'att7'
                }
            ]
        },
    ]
