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
"""RPKI DOA implementation - draft-spaghetti-sidrops-rpki-doa."""

from __future__ import annotations

import logging

from typing import Any, Dict, Iterable, Optional, Tuple

from rpkimancer.asn1 import Content
from rpkimancer.asn1.mod import RpkiDiscardOriginAttestation_2021
from rpkimancer.resources import (AFI, IPNetwork,
                                  IpResourcesInfo, net_to_bitstring)
from rpkimancer.sigobj.base import EncapsulatedContent, SignedObject

from .communities import BgpCommunity

log = logging.getLogger(__name__)

DoaNetworkInfo = Tuple[IPNetwork, Optional[Tuple[int, int]]]
IPListRangeInfo = Iterable[DoaNetworkInfo]


class IPListRange(Content):
    """ASN.1 IPListRange type."""

    content_syntax = RpkiDiscardOriginAttestation_2021.IPListRange

    def __init__(self, ip_addr_blocks: IPListRangeInfo):
        """Initialise IPListRange instance."""
        data = list()
        for network, len_range in ip_addr_blocks:
            item = {"addressFamily": AFI[network.version],
                    "addressOrRange": ("addressPrefix",
                                       net_to_bitstring(network))}
            if len_range is not None:
                item["prefixLengthRange"] = {"minLength": len_range[0],
                                             "maxLength": len_range[1]}
            data.append(item)
        super().__init__(data)


class DiscardOriginAttestationEContent(EncapsulatedContent):
    """encapContentInfo for RPKI Discard Origin Attestations."""

    content_type = RpkiDiscardOriginAttestation_2021.id_ct_discardOriginAttestation  # noqa: E501
    content_syntax = RpkiDiscardOriginAttestation_2021.DiscardOriginAttestation
    file_ext = "doa"
    as_resources = None

    def __init__(self, *,
                 version: int = 0,
                 ip_addr_blocks: IPListRangeInfo,
                 origin_as: int,
                 peer_as_set: Optional[Iterable[int]] = None,
                 communities: Iterable[BgpCommunity]) -> None:
        """Initialise the encapContentInfo."""
        ip_addr_blocks_data = IPListRange(ip_addr_blocks).content_data
        data: Dict[str, Any] = {"version": version,
                                "ipAddrBlocks": ip_addr_blocks_data,
                                "originAsID": origin_as,
                                "communities": [c.choice_value()
                                                for c in communities]}
        if peer_as_set is not None:
            data["peerAsIDs"] = list(peer_as_set)
        super().__init__(data)
        self._ip_resources = [network for network, _ in ip_addr_blocks]

    @property
    def ip_resources(self) -> Optional[IpResourcesInfo]:
        """Get the IP Address Resources covered by this DOA."""
        return self._ip_resources


class DiscardOriginAttestation(SignedObject,
                               econtent_type=RpkiDiscardOriginAttestation_2021.ct_discardOriginAttestation):  # noqa: E501
    """CMS ASN.1 ContentInfo for RPKI Discard Origin Attestations."""

    econtent_cls = DiscardOriginAttestationEContent
