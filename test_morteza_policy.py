import copy
import unittest
from morteza_policy import audit


class PolicyTests(unittest.TestCase):
    def setUp(self):
        self.config = {"services": {"api": {"user": "10001:10001", "read_only": True, "cap_drop": ["ALL"], "security_opt": ["no-new-privileges:true"], "healthcheck": {"test": ["CMD", "true"]}, "ports": [{"host_ip": "127.0.0.1", "target": 8080}], "mem_limit": 134217728, "pids_limit": 64}}}

    def test_safe_configuration(self):
        self.assertEqual(audit(self.config), [])

    def test_each_unsafe_setting_is_rejected(self):
        variants = {"user": "0:0", "privileged": True, "read_only": False, "cap_drop": [], "cap_add": ["SYS_ADMIN"], "security_opt": [], "healthcheck": {"disable": True}, "ports": [{"host_ip": "0.0.0.0"}], "network_mode": "host", "pid": "host", "volumes": [{"type": "bind", "source": "/var/run/docker.sock"}], "mem_limit": 0, "pids_limit": 0}
        for key, value in variants.items():
            with self.subTest(key=key):
                config = copy.deepcopy(self.config)
                config["services"]["api"][key] = value
                self.assertTrue(audit(config), key)

    def test_empty_config_rejected(self):
        self.assertTrue(audit({}))

    def test_disabled_healthcheck_rejected(self):
        self.config["services"]["api"]["healthcheck"] = {"test": ["NONE"]}
        self.assertTrue(audit(self.config))


if __name__ == "__main__":
    unittest.main()
