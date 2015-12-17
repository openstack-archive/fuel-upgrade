# -*- coding: utf-8 -*-

#    Copyright 2014 Mirantis, Inc.
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
import logging
import shotgun

from fuel_upgrade.clients import SupervisorClient
from fuel_upgrade.engines.base import UpgradeEngine

logger = logging.getLogger(__name__)


class BackupManager(UpgradeEngine):
    """Backup manager for the Fuel Admin system

    Required for data-driven upgrade of the Admin
    node.

    * prepare configuration for Shotgun tool
    * run shotgun
    """
    def __init__(self, *args, **kwargs):
        """Extract some base parameters and save it internally."""
        super(BackupManager, self).__init__(*args, **kwargs)
        self.backup_config = self.config.backup_config
        self.cobbler_config_path = self.config.cobbler_config_path
        self.supervisor = SupervisorClient(self.config,
                                           self.config.from_version)

    def upgrade(self):
        """Run upgrade process."""
        self.run_shotgun()
        self.supervisor.start('nailgun')

    def rollback(self):
        """Rollback all the changes, usually used in case of failed upgrade"""
        logger.debug("Backup failed, starting container nailgun")
        self.supervisor.start('nailgun')

    def required_free_space(self):
        """Required free space for upgrade

        Must return dict where key is path to directory
        and value is required free space in megabytes.

        Example:
          {
            "/var/www/nailgun": 2000,
            "/var/lib/docker": 5000,
            "/etc/supervisor.d": 10,
          }
        """
        return {
            self.config.working_directory: 200
        }

    def run_shotgun(self):
        config = shotgun.config.Config(self.backup_config)
        manager = shotgun.manager.Manager(config)
        backup_file = manager.snapshot()
        logger.debug("Backup saved to %s", backup_file)
