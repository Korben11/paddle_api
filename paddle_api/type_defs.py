"""Type definitions."""
import typing
from dataclasses import dataclass, field

# TODO: try to replace dataclass_wizard with dacite https://github.com/konradhalas/dacite
#  or use Pydantic?
from dataclass_wizard import JSONWizard

T = typing.TypeVar("T", bound=JSONWizard)


@dataclass
class Pagination:
    per_page: int
    has_more: bool
    estimated_total: int
    next: typing.Optional[str] = None


@dataclass
class ResponseMeta:
    request_id: str
    pagination: typing.Optional[Pagination]


@dataclass
class Page(typing.Generic[T], JSONWizard):
    # data: typing.List[dict]
    # generics seems to not work yet with from_dict in libs: dataclass-wizard, dataclasses-json
    data: typing.List[T]
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
    # string<date-time>, Timestamp following the RFC 3339 standard
    created_at: str


@dataclass
class Product(_ProductDefaultsBase, _Product):
    pass


@classmethod
class Quantity:
    minimum: int
    maximum: int


@classmethod
class BillingCycle:
    interval: str
    frequency: int


@classmethod
class Money:
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


@classmethod
class UnitPriceOverride:
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


@dataclass
class _PriceDefaultBase:
    quantity: Quantity = None  # type: ignore  # issue when used with Optional
    billing_cycle: BillingCycle = None  # type: ignore
    # Cannot be used if billing_cycle is null
    # TODO: add some kind of validation for init?
    trial_period: typing.Any = None
    tax_mode: typing.Literal[
        "internal",
        "external",
        "account_setting",
    ] = None  # type: ignore
    unit_price_overrides: typing.List[typing.Any] = field(default_factory=list)
    # unit_price_overrides: typing.List[UnitPriceOverride] = field(default_factory=list)  # type: ignore


@dataclass
class _PriceCreateBase(JSONWizard):
    description: str
    product_id: str
    unit_price: Money


@dataclass
class _PriceBase(_PriceCreateBase):
    id: str
    status: typing.Literal["active", "archived"]
    product: Product


@dataclass
class PriceCreate(_PriceDefaultBase, _PriceCreateBase):
    pass


@dataclass
class Price(_PriceDefaultBase, _PriceBase):
    pass
