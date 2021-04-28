import asyncio
import time
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

    @classmethod
    async def fill_database(cls):
        data = [cls.model(**item) for item in cls.data]
        db_items = []
        for item in data:
            result = await cls.data_creation_function(item)
            db_items.append(result)
        cls.data = db_items
        time.sleep(3)


class AttributesData(DataContainer):
    model = Attribute
    data_creation_function = create_attribute
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
    model = Tag
    data_creation_function = create_tag
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


class BrandsData(DataContainer):
    model = Brand
    data_creation_function = create_brand
    data = [
        {
            'name': 'Brand1'
        },
        {
            'name': 'Brand2'
        },
        {
            'name': 'Brand3'
        },
        {
            'name': 'Brand4'
        },
        {
            'name': 'Brand5'
        }
    ]


class ProductsData(DataContainer):
    model = Product
    data_creation_function = create_product
    data = [
        {
            'name': 'Product1',
            'brand': {
                'name': 'Brand1'
            },
            'tags': [
                {
                    'name': 'Tag1'
                },
                {
                    'name': 'Tag2'
                },
                {
                    'name': 'Tag3'
                }
            ],
            'variants': [
                {
                    'name': 'var1',
                    'attributes_values': [
                        {
                            'name': 'att3',
                            'value': 'Val1'
                        },
                        {
                            'name': 'att4',
                            'value': 'Val2'
                        }
                    ]
                }
            ]
        },
        {
            'name': 'Product2',
            'brand': {
                'name': 'Brand1'
            },
            'tags': [
                {
                    'name': 'Tag1'
                },
                {
                    'name': 'Tag2'
                }
            ],
            'variants': [
                {
                    'name': 'var1',
                    'attributes_values': [
                        {
                            'name': 'att1',
                            'value': 'Val1'
                        },
                        {
                            'name': 'att2',
                            'value': 'Val2'
                        }
                    ]
                },
                {
                    'name': 'var2',
                    'attributes_values': [
                        {
                            'name': 'att2',
                            'value': 'Val2'
                        },
                        {
                            'name': 'att4',
                            'value': 'Val3'
                        }
                    ]
                }
            ]
        },
        {
            'name': 'Product3',
            'brand': {
                'name': 'Brand2'
            },
            'tags': [
                {
                    'name': 'Tag2'
                },
                {
                    'name': 'Tag3'
                }
            ],
            'variants': [
                {
                    'name': 'var1',
                    'attributes_values': [
                        {
                            'name': 'att3',
                            'value': 'Val1'
                        },
                        {
                            'name': 'att5',
                            'value': 'Val2'
                        }
                    ]
                },
                {
                    'name': 'var2',
                    'attributes_values': [
                        {
                            'name': 'att2',
                            'value': 'Val2'
                        },
                        {
                            'name': 'att5',
                            'value': 'Val3'
                        }
                    ]
                }
            ]
        },
    ]
