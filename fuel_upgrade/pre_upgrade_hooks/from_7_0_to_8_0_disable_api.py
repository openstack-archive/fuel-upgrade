# -*- coding: utf-8 -*-

#    Copyright 2015 Mirantis, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import json
import re

from fuel_upgrade.engines.host_system import HostSystemUpgrader
from fuel_upgrade.pre_upgrade_hooks.base import PreUpgradeHookBase

from fuel_upgrade.utils import compare_version
from fuel_upgrade.utils import exec_cmd_iterator
from fuel_upgrade.utils import safe_exec_cmd


class DisableNailgunAPI(PreUpgradeHookBase):
    """Disable Nailgun API

    For the purposes of integrity of database dump, we need to
    disable Nailgun API and prevent extrnal entities from writing
    to the DB.

    This hook required only for backup command of fuel-upgrade tool.
    """

    enable_for_engines = []

    def __init__(self, *args, **kwargs):
        super(DisableNailgunAPI, self).__init__(*args, **kwargs)

        from_version = self.config.from_version
        self._container = 'fuel-core-{0}-nailgun'.format(from_version)

    def check_if_required(self):
        # not required if fuel version is not 7.0
        if compare_version('7.0', self.config.from_version) == 0:
            return True
        return False

    def _stop_container(self):
        safe_exec_cmd('docker stop {0}'.format(self._container))

    def run(self):
        self._stop_container()
