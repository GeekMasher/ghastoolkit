import os
import logging
from string import Template
from typing import Optional
from requests import Session

from ghastoolkit.octokit.github import GitHub, Repository


logger = logging.getLogger("ghastoolkit.octokit")

__OCTOKIT_PATH__ = os.path.dirname(os.path.realpath(__name__))

__OCTOKIT_ERRORS__ = {401: "Authentication Issue"}


class Octokit:
    @staticmethod
    def route(path: str, repository: Repository, rtype: str = "rest", **options) -> str:
        """Generate Route string"""
        formatted_path = Octokit.formatPath(path, repository, **options)

        if not formatted_path.startswith("/"):
            formatted_path = "/" + formatted_path
        url = GitHub.api_rest if rtype == "rest" else GitHub.api_graphql
        return f"{url}{formatted_path}"

    @staticmethod
    def formatPath(path: str, repo: Repository, **options) -> str:
        formatted_path = path.format(
            owner=repo.owner, org=repo.owner, repo=repo.repo, **options
        )
        return formatted_path


class RestRequest:
    PER_PAGE = 100
    VERSION: str = "2022-11-28"

    def __init__(self, repository: Optional[Repository] = None) -> None:
        self.repository = repository
        self.session = Session()
        # https://docs.github.com/en/rest/overview/authenticating-to-the-rest-api
        self.session.headers = {
            "Accept": "application/vnd.github.v3+json",
            "X-GitHub-Api-Version": RestRequest.VERSION,
            "Authorization": f"token {GitHub.token}",
        }

    def get(
        self,
        path: str,
        parameters: dict = {},
        expected: int = 200,
        authenticated: bool = False,
    ) -> dict | list[dict]:
        repo = self.repository or GitHub.repository
        if not repo:
            raise Exception("Repository needs to be set")

        url = Octokit.route(path, repo, rtype="rest", **parameters)
        logger.debug(f"Fetching content from URL :: {url}")

        if authenticated and not self.session.headers.get("Authorization"):
            raise Exception(f"GitHub Token required for this request")

        result = []
        params = parameters
        params["per_page"] = RestRequest.PER_PAGE

        page = 1  # index starts at 1

        while True:
            params["page"] = page

            responce = self.session.get(url, params=params)
            responce_json = responce.json()

            if responce.status_code != expected:
                logger.error(f"Error code from server :: {responce.status_code}")
                known_error = __OCTOKIT_ERRORS__.get(responce.status_code)
                if known_error:
                    raise Exception(known_error)
                raise Exception("REST Request failed :: non-expected server error")

            if isinstance(responce_json, dict) and responce_json.get("errors"):
                logger.error(responce_json.get("message"))
                raise Exception("REST Request failed :: error from server")

            if isinstance(responce_json, dict):
                return responce_json

            result.extend(responce_json)
            # if the page is not full, we must have hit the end
            if len(responce_json) < RestRequest.PER_PAGE:
                break

            page += 1

        return result

    def postJson(self, path: str, data: dict, expected: int = 200):
        repo = self.repository or GitHub.repository
        if not repo:
            raise Exception("Repository needs to be set")

        url = Octokit.route(path, repo, rtype="rest")
        logger.debug(f"Posting content from URL :: {url}")

        response = self.session.post(url, json=data)

        if response.status_code != expected:
            raise Exception(f"Failed to post data")


class GraphQLRequest:
    locations: list[str] = [os.path.join(__OCTOKIT_PATH__, "queries")]

    @staticmethod
    def query(name: str, **options):
        query_content = GraphQLRequest.loadQuery(name)
        if not query_content:
            return
        query = GraphQLRequest.formatQuery(query_content, **options)
        return {}

    @staticmethod
    def loadQuery(name: str) -> Optional[str]:
        return

    @staticmethod
    def formatQuery(query: str, **options):
        return Template(query).substitute(**options)
