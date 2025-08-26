"""Test pagination functionality in the Octokit module."""

import unittest
from ghastoolkit.octokit.octokit import RestRequest


class TestPagination(unittest.TestCase):
    """Test case for pagination functionality in the RestRequest class."""

    def test_parse_link_header_empty(self):
        """Test parsing an empty Link header."""
        result = RestRequest.parse_link_header("")
        self.assertEqual({}, result)

    def test_parse_link_header_invalid(self):
        """Test parsing an invalid Link header."""
        result = RestRequest.parse_link_header("invalid-link-header")
        self.assertEqual({}, result)

    def test_parse_link_header_single(self):
        """Test parsing a Link header with a single link."""
        link_header = '<https://api.github.com/repositories/1/issues?page=2>; rel="next"'
        result = RestRequest.parse_link_header(link_header)
        self.assertEqual({
            "next": "https://api.github.com/repositories/1/issues?page=2"
        }, result)

    def test_parse_link_header_multiple(self):
        """Test parsing a Link header with multiple links."""
        link_header = (
            '<https://api.github.com/repositories/1/issues?page=2>; rel="next", '
            '<https://api.github.com/repositories/1/issues?page=5>; rel="last", '
            '<https://api.github.com/repositories/1/issues?page=1>; rel="first"'
        )
        result = RestRequest.parse_link_header(link_header)
        self.assertEqual({
            "next": "https://api.github.com/repositories/1/issues?page=2",
            "last": "https://api.github.com/repositories/1/issues?page=5",
            "first": "https://api.github.com/repositories/1/issues?page=1"
        }, result)

    def test_extract_cursor_from_link_none(self):
        """Test extracting cursor from None."""
        result = RestRequest.extract_cursor_from_link(None)
        self.assertIsNone(result)

    def test_extract_cursor_from_link_without_after(self):
        """Test extracting cursor from a link without an after parameter."""
        link = "https://api.github.com/repositories/1/issues?page=2"
        result = RestRequest.extract_cursor_from_link(link)
        self.assertIsNone(result)

    def test_extract_cursor_from_link_with_after(self):
        """Test extracting cursor from a link with an after parameter."""
        link = "https://api.github.com/repositories/1/issues?page=2&after=Y3Vyc29yOjI="
        result = RestRequest.extract_cursor_from_link(link)
        self.assertEqual("Y3Vyc29yOjI=", result)

    def test_extract_cursor_from_link_with_after_and_more_params(self):
        """Test extracting cursor from a link with an after parameter and additional params."""
        link = "https://api.github.com/repositories/1/issues?page=2&after=Y3Vyc29yOjI=&per_page=100"
        result = RestRequest.extract_cursor_from_link(link)
        self.assertEqual("Y3Vyc29yOjI=", result)

    def test_extract_cursor_from_link_with_invalid_after(self):
        """Test extracting cursor from a link where after is a URL."""
        link = "https://api.github.com/repositories/1/issues?page=2&after=https://example.com"
        result = RestRequest.extract_cursor_from_link(link)
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
