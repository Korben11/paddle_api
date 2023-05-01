"""Type definitions."""
import typing

from pydantic import BaseModel
from pydantic.generics import GenericModel

# TODO: try to replace dataclass_wizard with dacite https://github.com/konradhalas/dacite
#  or use Pydantic?

T = typing.TypeVar("T", bound=BaseModel)


class Pagination(BaseModel):
    per_page: int
    has_more: bool
    estimated_total: int
    next: typing.Optional[str] = None


class ResponseMeta(BaseModel):
    request_id: str
    pagination: typing.Optional[Pagination]


class _ProductBase(BaseModel):
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
    description: typing.Optional[str] = None
    image_url: typing.Optional[str] = None


class Page(GenericModel, typing.Generic[T]):
    # data: typing.List[dict]
    # generics seems to not work yet with from_dict in libs: dataclass-wizard, dataclasses-json
    data: typing.List[T]
    meta: ResponseMeta


class ProductCreate(_ProductBase):
    pass


class Product(_ProductBase):
    id: str
    status: typing.Literal["active", "archived"]
    # string<date-time>, Timestamp following the RFC 3339 standard
    created_at: str


class Quantity(BaseModel):
    minimum: int
    maximum: int


class BillingCycle(BaseModel):
    interval: str
    frequency: int


class Money(BaseModel):
    amount: str
    # ISO 4217 code of a currency
    currency_code: typing.Literal[
        "ARS",
        "AUD",
        "BRL",
        "CAD",
        "CHF",
        "CNY",
        "CZK",
        "DKK",
        "EUR",
        "GBP",
        "HKD",
        "HUF",
        "ILS",
        "INR",
        "JPY",
        "KRW",
        "MXN",
        "NOK",
        "NZD",
        "PLN",
        "RUB",
        "SEK",
        "SGD",
        "THB",
        "TRY",
        "TWD",
        "UAH",
        "USD",
        "ZAR",
    ]


class UnitPriceOverride(BaseModel):
    amount: str
    # ISO 3166-1 alpha-2 representation of a country
    currency_code: typing.Literal[
        "AD",
        "AE",
        "AF",
        "AG",
        "AI",
        "AL",
        "AM",
        "AN",
        "AO",
        "AR",
        "AS",
        "AT",
        "AU",
        "AW",
        "AX",
        "AZ",
        "BA",
        "BB",
        "BD",
        "BE",
        "BF",
        "BG",
        "BH",
        "BI",
        "BJ",
        "BM",
        "BN",
        "BO",
        "BQ",
        "BR",
        "BS",
        "BT",
        "BV",
        "BW",
        "BY",
        "BZ",
        "CA",
        "CC",
        "CF",
        "CG",
        "CH",
        "CI",
        "CK",
        "CL",
        "CM",
        "CN",
        "CO",
        "CR",
        "CU",
        "CV",
        "CW",
        "CX",
        "CY",
        "CZ",
        "DE",
        "DJ",
        "DK",
        "DM",
        "DO",
        "DZ",
        "EC",
        "EE",
        "EG",
        "EH",
        "ER",
        "ES",
        "ET",
        "FI",
        "FJ",
        "FK",
        "FM",
        "FO",
        "FR",
        "GA",
        "GB",
        "GD",
        "GE",
        "GF",
        "GG",
        "GH",
        "GI",
        "GL",
        "GM",
        "GN",
        "GP",
        "GQ",
        "GR",
        "GS",
        "GT",
        "GU",
        "GW",
        "GY",
        "HK",
        "HM",
        "HN",
        "HR",
        "HT",
        "HU",
        "ID",
        "IE",
        "IL",
        "IM",
        "IN",
        "IO",
        "IQ",
        "IR",
        "IS",
        "IT",
        "JE",
        "JM",
        "JO",
        "JP",
        "KE",
        "KG",
        "KH",
        "KI",
        "KM",
        "KN",
        "KP",
        "KR",
        "KW",
        "KY",
        "KZ",
        "LA",
        "LB",
        "LC",
        "LI",
        "LK",
        "LR",
        "LS",
        "LT",
        "LU",
        "LV",
        "LY",
        "MA",
        "MC",
        "MD",
        "ME",
        "MF",
        "MG",
        "MH",
        "MK",
        "ML",
        "MM",
        "MN",
        "MO",
        "MP",
        "MQ",
        "MR",
        "MS",
        "MT",
        "MU",
        "MV",
        "MW",
        "MX",
        "MY",
        "MZ",
        "NA",
        "NC",
        "NE",
        "NF",
        "NG",
        "NI",
        "NL",
        "NO",
        "NP",
        "NR",
        "NU",
        "NZ",
        "OM",
        "PA",
        "PE",
        "PF",
        "PG",
        "PH",
        "PK",
        "PL",
        "PM",
        "PN",
        "PR",
        "PS",
        "PT",
        "PW",
        "PY",
        "QA",
        "RE",
        "RO",
        "RS",
        "RU",
        "RW",
        "SA",
        "SB",
        "SC",
        "SD",
        "SE",
        "SG",
        "SH",
        "SI",
        "SJ",
        "SK",
        "SL",
        "SM",
        "SN",
        "SO",
        "SR",
        "ST",
        "SV",
        "SY",
        "SZ",
        "TC",
        "TD",
        "TF",
        "TG",
        "TH",
        "TJ",
        "TK",
        "TL",
        "TM",
        "TN",
        "TO",
        "TR",
        "TT",
        "TV",
        "TW",
        "TZ",
        "UA",
        "UG",
        "UM",
        "US",
        "UY",
        "UZ",
        "VA",
        "VC",
        "VE",
        "VG",
        "VI",
        "VN",
        "VU",
        "WF",
        "WS",
        "YE",
        "YT",
        "ZA",
        "ZM",
        "ZW",
    ]
    unit_price: Money


class _PriceBase(BaseModel):
    quantity: Quantity = None  # type: ignore  # issue when used with Optional
    billing_cycle: BillingCycle = None  # type: ignore
    # Cannot be used if billing_cycle is null
    # TODO: add some kind of validation for init?
    trial_period: typing.Any = None
    tax_mode: typing.Optional[
        typing.Literal[
            "internal",
            "external",
            "account_setting",
        ]
    ] = None
    unit_price_overrides: typing.Optional[typing.List[UnitPriceOverride]] = None
    description: str
    product_id: str
    unit_price: Money


class PriceCreate(_PriceBase):
    pass


class Price(_PriceBase):
    id: str
    status: typing.Literal["active", "archived"]
    product: Product
