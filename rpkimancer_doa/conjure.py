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
"""rpkincant conjure plugins for RPKI Discard Origin Authorizations."""

from __future__ import annotations

import ipaddress
import logging
from typing import Any, TYPE_CHECKING

from rpkimancer.cli import Args
from rpkimancer.cli.conjure import (ConjurePlugin,
                                    DEFAULT_CA_AS_RESOURCES,
                                    DEFAULT_CA_IP_RESOURCES,
                                    META_AS, META_IP,
                                    PluginReturn)

from .communities import BLACKHOLE, from_str

if TYPE_CHECKING:
    from rpkimancer.cert import CertificateAuthority
    from .sigobj import DoaNetworkInfo

log = logging.getLogger(__name__)

META_IP_MINMAXLEN = f"{META_IP}[-minlen-maxlen]"
META_COMMUNITY = "<community>"


class ConjureDoa(ConjurePlugin):
    """rpkincant conjure plugin for RPKI Discard Origin Authorizations."""

    def init_parser(self) -> None:
        """Set up command line argument parser."""
        self.parser.add_argument("--doa-networks",
                                 nargs="+", type=self._doa_network,
                                 default=[(ipaddress.ip_network(net), None)
                                          for net in DEFAULT_CA_IP_RESOURCES],
                                 metavar=META_IP_MINMAXLEN,
                                 help="IP prefixes to include in DOA "
                                      "(default: %(default)s)")
        self.parser.add_argument("--doa-origin-as",
                                 type=int,
                                 default=DEFAULT_CA_AS_RESOURCES[0],
                                 metavar=META_AS,
                                 help="ASN to include in DOA originAsID "
                                      "(default: %(default)s)")
        self.parser.add_argument("--doa-peer-as",
                                 nargs="*", type=int,
                                 metavar=META_AS,
                                 help="ASNs to include in DOA peerAsIDs "
                                      "(default: %(default)s)")
        self.parser.add_argument("--doa-communities",
                                 nargs="+", type=from_str,
                                 default=[BLACKHOLE],
                                 metavar=META_COMMUNITY,
                                 help="Communities to include in DOA "
                                      "(default: %(default)s)")

    def run(self, parsed_args: Args, ca: CertificateAuthority,
            *args: Any, **kwargs: Any) -> PluginReturn:
        """Run with the given arguments."""
        # create DOA object
        from .sigobj import DiscardOriginAuthorization
        log.info("creating DOA object")
        DiscardOriginAuthorization(issuer=ca,
                                   ip_addr_blocks=parsed_args.doa_networks,
                                   origin_as=parsed_args.doa_origin_as,
                                   peer_as_set=parsed_args.doa_peer_as,
                                   communities=parsed_args.doa_communities)
        return None

    @staticmethod
    def _doa_network(input_str: str) -> DoaNetworkInfo:
        """Convert input string to DoaNetworkInfo tuple."""
        try:
            network, minlen, maxlen = input_str.split("-", 2)
            return (ipaddress.ip_network(network), (int(minlen), int(maxlen)))
        except ValueError:
            return (ipaddress.ip_network(input_str), None)
