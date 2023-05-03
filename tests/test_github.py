import unittest

from ghastoolkit.octokit.github import GitHub, Repository


class TestGitHub(unittest.TestCase):
    def setUp(self) -> None:
        return super().setUp()

    def tearDown(self) -> None:
        # reset
        GitHub.instance = "https://github.com"
        GitHub.api_rest = "https://api.github.com"
        GitHub.api_graphql = "https://api.github.com/graphql"

        return super().tearDown()

    def test_default(self):
        GitHub.init("GeekMasher/ghastoolkit")

        self.assertEqual(GitHub.instance, "https://github.com")
        self.assertEqual(GitHub.api_rest, "https://api.github.com")
        self.assertEqual(GitHub.api_graphql, "https://api.github.com/graphql")

    def test_server(self):
        GitHub.init("GeekMasher/ghastoolkit", instance="https://github.geekmasher.dev")

        self.assertEqual(GitHub.instance, "https://github.geekmasher.dev")
        self.assertEqual(GitHub.api_rest, "https://github.geekmasher.dev/api/v3")
        self.assertEqual(
            GitHub.api_graphql, "https://github.geekmasher.dev/api/v3/graphql"
        )

    def test_parseReference(self):
        repo = Repository.parseRepository("GeekMasher/ghastoolkit")
        self.assertEqual(repo.owner, "GeekMasher")
        self.assertEqual(repo.repo, "ghastoolkit")

        repo = Repository.parseRepository("GeekMasher/ghastoolkit@main")
        self.assertEqual(repo.owner, "GeekMasher")
        self.assertEqual(repo.repo, "ghastoolkit")
        self.assertEqual(repo.branch, "main")
        self.assertEqual(repo.reference, "refs/heads/main")


class TestRepository(unittest.TestCase):
    def setUp(self) -> None:
        GitHub.token = None
        GitHub.github_app = False

        return super().setUp()

    def test_branch(self):
        repo = Repository("GeekMasher", "ghastoolkit", reference="refs/heads/main")
        self.assertEqual(repo.reference, "refs/heads/main")
        self.assertEqual(repo.branch, "main")

    def test_pull_request(self):
        repo = Repository("GeekMasher", "ghastoolkit", reference="refs/heads/main")
        self.assertFalse(repo.isInPullRequest())

        repo = Repository("GeekMasher", "ghastoolkit", reference="refs/pull/1/merge")
        self.assertTrue(repo.isInPullRequest())
        self.assertEqual(repo.getPullRequestNumber(), 1)

    def test_clone_url(self):
        repo = Repository("GeekMasher", "ghastoolkit")
        self.assertEqual(
            repo.clone_url, "https://github.com/GeekMasher/ghastoolkit.git"
        )

        GitHub.token = "test_token"
        self.assertEqual(
            repo.clone_url, "https://test_token@github.com/GeekMasher/ghastoolkit.git"
        )

        GitHub.github_app = True
        GitHub.token = "test_token"
        self.assertEqual(
            repo.clone_url,
            "https://x-access-token:test_token@github.com/GeekMasher/ghastoolkit.git",
        )

    def test_clone_cmd(self):
        path = "/tml/ghastoolkit"
        repo = Repository("GeekMasher", "ghastoolkit")

        cmd = ["git", "clone", repo.clone_url, path]
        self.assertEqual(repo._cloneCmd(path), cmd)

        cmd = ["git", "clone", "--depth", "1", repo.clone_url, path]
        self.assertEqual(repo._cloneCmd(path, depth=1), cmd)

        repo.branch = "main"
        cmd = ["git", "clone", "-b", "main", repo.clone_url, path]
        self.assertEqual(repo._cloneCmd(path), cmd)

    def test_clone_file(self):
        path = "README.md"
        repo = Repository("GeekMasher", "ghastoolkit")
        repo.getFile(path)
