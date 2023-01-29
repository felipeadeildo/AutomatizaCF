
from typing import Mapping
from wrappers.instagram import Instagram
from wrappers.whatsapp import Whatsapp
from .base import Wrapper

wrappers_map: Mapping[str, Wrapper] = {
    "instagram": Instagram,
    "whatsapp": Whatsapp,
}