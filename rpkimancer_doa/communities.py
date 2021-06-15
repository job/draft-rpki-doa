# Copyright (c) 2021 Ben Maddison. All rights reserved.
#
# The contents of this file are licensed under the MIT License
# (the "License"); you may not use this file except in compliance with the
# License.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.
"""BGP Communities."""

from __future__ import annotations

import dataclasses
from typing import Generator, Tuple


def from_str(community_str: str) -> BgpCommunity:
    """Construct a community from a string representation."""
    components = [int(c) for c in community_str.split(":")]
    if len(components) == 2:
        return StandardCommunity(*components)
    elif len(components) == 3:
        return LargeCommunity(*components)
    else:
        raise ValueError


class BgpCommunity:
    """Base class for BGP communities."""

    component_len: int
    choice_label: str

    def __iter__(self) -> Generator[int, None, None]:
        """Iterate over components."""
        for c in dataclasses.astuple(self):
            yield c

    def __str__(self) -> str:
        """Get `str` representation."""
        return ":".join(str(c) for c in self)

    def __repr__(self) -> str:
        """Get `repr` representation."""
        return self.__str__()

    def to_bytes(self) -> bytes:
        """Get community value as bytes."""
        return b"".join(c.to_bytes(length=self.component_len,
                                   byteorder="big")
                        for c in self)

    def choice_value(self) -> Tuple[str, bytes]:
        """Get (type, value) tuple for ASN.1 encoding."""
        return (self.choice_label, self.to_bytes())


@dataclasses.dataclass(repr=False)
class StandardCommunity(BgpCommunity):
    """RFC1997 BGP Standard Community."""

    component_len = 2
    choice_label = "bgpCommunity"

    adminstrator: int
    local: int


@dataclasses.dataclass
class LargeCommunity(BgpCommunity):
    """RFC8092 BGP Large Community."""

    component_len = 4
    choice_label = "bgpLargeCommunity"

    global_administrator: int
    local_data_1: int
    local_data_2: int


BLACKHOLE = StandardCommunity(0xFFFF, 666)
