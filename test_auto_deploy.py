#!/usr/bin/python

import auto_deploy
from mock import MagicMock
import pytest


class TestAutoDeploy():

    def setup(self):
        self.mock_json()
        self.mock_logging()
        self.moke_subpro_returncode(0)

    def moke_subpro_returncode(self, returncode):

        self.t_pipeopen = MagicMock()

        self.t_pipeopen.PIPE = 0

        self.subprc = MagicMock()

        self.subprc.returncode = returncode

        subprc_dict = {"communicate.return_value": [0], "wait.return_value": 0}

        self.subprc.configure_mock(**subprc_dict)

        t_pipeopen_dict = {"Popen.return_value": self.subprc}

        self.t_pipeopen.configure_mock(**t_pipeopen_dict)

#        print t_pipeopen.Popen([1, 2, 2], 55)

    def mock_logging(self):

        self.infologer = MagicMock()

        t_infologer_dict = {"error.return_value": 0}

        self.infologer.configure_mock(**t_infologer_dict)

    def mock_json(self):

        self.t_info_json = MagicMock()

        t_info_json_dict = {"loads.return_value": 0}

        self.t_info_json.configure_mock(**t_info_json_dict)

    def test_get_node_info_expect(self):

        self.moke_subpro_returncode(1)

        testdeploy = auto_deploy.deployment(
            self.t_pipeopen, self.infologer, self.t_info_json)

        with pytest.raises(SystemExit):
            testdeploy.get_node_info()

    def test_get_node_info_jsondata(self):

        self.moke_subpro_returncode(0)

        testdeploy = auto_deploy.deployment(
            self.t_pipeopen, self.infologer, self.t_info_json)

        assert testdeploy.get_node_info() == 0

    def test_get_cluster_info_expect(self):

        self.moke_subpro_returncode(1)

        testdeploy = auto_deploy.deployment(
            self.t_pipeopen, self.infologer, self.t_info_json)

        with pytest.raises(SystemExit):
            testdeploy.get_cluster_info()

    def test_get_cluster_info_jsondata(self):

        self.moke_subpro_returncode(0)

        testdeploy = auto_deploy.deployment(
            self.t_pipeopen, self.infologer, self.t_info_json)

        assert testdeploy.get_node_info() == 0

    def test_get_node_num(self):

        testdeploy = auto_deploy.deployment(
            self.t_pipeopen, self.infologer, self.t_info_json)

        testdeploy.nodeinfo_json = [1, 2, 2, 3]

        testdeploy.get_node_num()

        assert testdeploy.node_num != 3

    def test_store_node_id_expect(self):

        testdeploy = auto_deploy.deployment(
            self.t_pipeopen, self.infologer, self.t_info_json)

        testdeploy.node_num = 1

        testdeploy.nodeinfo_json = [{'status': 'stop', 'id': 0}]

        with pytest.raises(SystemExit):
            testdeploy.store_node_id()

    def test_store_node_id(self):

        testdeploy = auto_deploy.deployment(
            self.t_pipeopen, self.infologer, self.t_info_json)

        testdeploy.node_num = 1

        testdeploy.nodeinfo_json = [{'status': 'ready', 'id': 0}]

        testdeploy.store_node_id()

        assert testdeploy.id_list[0] == '0'

    def test_get_env_num(self):

        testdeploy = auto_deploy.deployment(
            self.t_pipeopen, self.infologer, self.t_info_json)

        testdeploy.nodeinfo_json = [{'cluster': 0}]

        testdeploy.get_env_num()

        assert testdeploy.cluster == 0

    def test_get_env_net_cfg_to_file_expect(self):

        self.moke_subpro_returncode(1)

        testdeploy = auto_deploy.deployment(
            self.t_pipeopen, self.infologer, self.t_info_json)

        testdeploy.cluster = 0

        testdeploy.path = './'

        with pytest.raises(SystemExit):
            testdeploy.get_env_net_cfg_to_file()

    def test_get_env_setting_cfg_to_file_expect(self):

        self.moke_subpro_returncode(1)

        testdeploy = auto_deploy.deployment(
            self.t_pipeopen, self.infologer, self.t_info_json)

        testdeploy.cluster = 0

        testdeploy.path = './'

        with pytest.raises(SystemExit):
            testdeploy.get_env_setting_cfg_to_file()

    def test_get_env_deploy_cfg_to_file_expect(self):

        self.moke_subpro_returncode(1)

        testdeploy = auto_deploy.deployment(
            self.t_pipeopen, self.infologer, self.t_info_json)

        testdeploy.cluster = 0

        testdeploy.path = './'

        with pytest.raises(SystemExit):
            testdeploy.get_env_setting_cfg_to_file()

    def mock_get_node_cfg_to_file(self, idx):

        pass

    def test_get_node_cfg_to_file(self):
        self.moke_subpro_returncode(0)

        testdeploy = auto_deploy.deployment(
            self.t_pipeopen, self.infologer, self.t_info_json)

        testdeploy.get_node_net_cfg_to_file = self.mock_get_node_cfg_to_file

        testdeploy.get_node_attr_cfg_to_file = self.mock_get_node_cfg_to_file

        testdeploy.get_node_disk_cfg_to_file = self.mock_get_node_cfg_to_file

        testdeploy.node_num = 1

        assert testdeploy.get_node_cfg_to_file() == 1

    def test_get_node_net_cfg_to_file_except(self):

        self.moke_subpro_returncode(1)

        testdeploy = auto_deploy.deployment(
            self.t_pipeopen, self.infologer, self.t_info_json)

        testdeploy.path = './'

        testdeploy.id_list = [0]

        with pytest.raises(SystemExit):
            testdeploy.get_node_net_cfg_to_file(0)

    def test_get_node_attr_cfg_to_file_except(self):
        self.moke_subpro_returncode(1)

        testdeploy = auto_deploy.deployment(
            self.t_pipeopen, self.infologer, self.t_info_json)

        testdeploy.path = './'

        testdeploy.id_list = [0]

        with pytest.raises(SystemExit):
            testdeploy.get_node_attr_cfg_to_file(0)

    def test_get_node_disk_cfg_to_file_except(self):
        self.moke_subpro_returncode(1)

        testdeploy = auto_deploy.deployment(
            self.t_pipeopen, self.infologer, self.t_info_json)

        testdeploy.path = './'

        testdeploy.id_list = [0]

        with pytest.raises(SystemExit):
            testdeploy.get_node_disk_cfg_to_file(0)


