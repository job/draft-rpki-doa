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
"""rpkimancer_doa package tests."""

from __future__ import annotations

import glob
import os

import pytest


@pytest.fixture(scope="session")
def target_directory(tmpdir_factory):
    """Set up a tmp directory for writing artifacts."""
    return tmpdir_factory.mktemp("target")


class TestCli:
    """Test cases for rpkimancer CLI tools."""

    def test_conjure(self, target_directory):
        """Test the conjure subcommand."""
        from rpkimancer.cli.__main__ import main
        argv = ["conjure", "--output-dir", f"{target_directory}"]
        retval = main(argv)
        assert retval is None

    @pytest.mark.parametrize("fmt", (None, "-A", "-j", "-J", "-R"))
    def test_perceive(self, target_directory, fmt):
        """Test the perceive subcommand."""
        from rpkimancer.cli.__main__ import main
        pattern = os.path.join(str(target_directory), "**", "*.doa")
        paths = glob.glob(pattern, recursive=True)
        argv = ["perceive",
                "--signed-data",
                "--output", os.devnull]
        if fmt is not None:
            argv.append(fmt)
        argv.extend(paths)
        retval = main(argv)
        assert retval is None
