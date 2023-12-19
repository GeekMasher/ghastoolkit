import unittest
from datetime import datetime, timedelta

from ghastoolkit.octokit.github import GitHub
from ghastoolkit.octokit.secretscanning import (
    SecretAlert,
    SecretScanning,
)


class TestSecretScanning(unittest.TestCase):
    def setUp(self) -> None:
        GitHub.init("GeekMasher/ghastoolkit")
        return super().setUp()

    def test_secretscanning_default(self):
        ss = SecretScanning()
        self.assertEqual(ss.repository.display(), "GeekMasher/ghastoolkit")

        ss = SecretScanning(GitHub.repository)
        self.assertEqual(ss.repository.display(), "GeekMasher/ghastoolkit")

        GitHub.init("Sample/Repo")
        ss = SecretScanning(GitHub.repository)
        self.assertEqual(ss.repository.display(), "Sample/Repo")


class TestSecretAlert(unittest.TestCase):
    def test_load_alert(self):
        data = {
            "number": 23,
            "created_at": "2020-11-06T18:18:30Z",
            "state": "open",
            "secret_type": "mailchimp_api_key",
            "secret_type_display_name": "Mailchimp API Key",
            "secret": "ABCDEFG",
            "validity": "active",
        }
        alert = SecretAlert(**data)
        self.assertEqual(alert.number, 23)
        self.assertEqual(alert.state, "open")
        self.assertEqual(alert.secret_type, "mailchimp_api_key")
        self.assertEqual(alert.secret, "ABCDEFG")
        self.assertEqual(alert.validity, "active")

    def test_mttr(self):
        data = {
            "number": 23,
            "created_at": "2020-11-06T18:18:30Z",
            "state": "open",
            "secret_type": "mailchimp_api_key",
            "secret_type_display_name": "Mailchimp API Key",
            "secret": "ABCDEFG",
            "validity": "active",
        }
        alert = SecretAlert(**data)
        self.assertEqual(alert.mttr, None)

        data["resolved_at"] = "2020-11-06T18:18:30Z"
        alert = SecretAlert(**data)
        self.assertEqual(alert.mttr, timedelta(seconds=0))

        data["resolved_at"] = "2020-11-06T18:18:31Z"
        alert = SecretAlert(**data)
        self.assertEqual(alert.mttr, timedelta(seconds=1))

        data["resolved_at"] = "2020-11-06T18:19:30Z"
        alert = SecretAlert(**data)
        self.assertEqual(alert.mttr, timedelta(seconds=60))

        data["resolved_at"] = "2020-11-06T19:19:30Z"
        alert = SecretAlert(**data)
        self.assertEqual(alert.mttr, timedelta(seconds=3660))
