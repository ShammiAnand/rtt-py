import markdownify
import requests


class UrlParser:
    """
    this module with GET the url and fetch its html content
    then use markdownify to convert the html content to markdown
    """

    def __init__(self, url: str):
        self.url = UrlParser.__validate_url(url)
        self.html = ""
        self.markdown = ""

    @staticmethod
    def __validate_url(url: str) -> str:
        """validates the url to ensure it is a valid url"""

        if not url.startswith("http"):
            raise ValueError(f"{url} is not a valid url")

        return url

    def convert(self, default_ext: str = ".md") -> str:
        """
        fetches the url and converts it to markdown
        then writes the markdown to a file with default_ext
        and returns the path to the file
        """

        response = requests.get(self.url)
        self.html = response.text
        self.markdown = markdownify.markdownify(self.html, heading_style="ATX")

        with open(f"rtt{default_ext}", "w") as f:
            f.write(self.markdown)

        return f"rtt{default_ext}"
