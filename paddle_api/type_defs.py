"""Type definitions."""
import typing
from dataclasses import dataclass

from dataclass_wizard import JSONWizard


@dataclass
class Pagination:
    per_page: int
    has_more: bool
    estimated_total: int
    next: typing.Optional[str] = None


@dataclass
class ResponseMeta:
    request_id: str
    pagination: Pagination


@dataclass
class Page(JSONWizard):
    data: typing.List[dict]
    # generics seems to not work yet with from_dict in libs: dataclass-wizard, dataclasses-json
    # data: typing.List[T]
    meta: ResponseMeta


@dataclass
class _ProductBase(JSONWizard):
    name: str
    tax_category: typing.Literal[
        "standard",
        "saas",
        "ebooks",
        "digital-goods",
        "website-hosting",
        "human-services",
        "implementation-services",
        "training-services",
        "professional-services",
        "software-programming-services",
    ]


@dataclass
class _ProductDefaultsBase:
    description: typing.Optional[str] = None
    image_url: typing.Optional[str] = None


@dataclass
class ProductCreate(_ProductDefaultsBase, _ProductBase):
    pass


@dataclass
class _Product(_ProductBase):
    id: str
    status: bool
    created_at: str


@dataclass
class Product(_ProductDefaultsBase, _Product):
    pass
