import scrapy
from urllib.parse import urljoin, urldefrag
import hashlib


class PythonDocsSpider(scrapy.Spider):
    name = "python_docs"
    allowed_domains = ["docs.python.org"]

    start_urls = [
        "https://docs.python.org/3/tutorial/"
    ]

    custom_settings = {
        "DOWNLOAD_DELAY": 1,
        "ROBOTSTXT_OBEY": True,
    }

    def normalize_url(self, url):
        url, _ = urldefrag(url)

        # These URLs represent the same page
        if url.rstrip("/") in [
            "https://docs.python.org/3/tutorial",
            "https://docs.python.org/3/tutorial/index.html",
        ]:
            return "https://docs.python.org/3/tutorial/"

        return url

    def parse(self, response):
        canonical_url = self.normalize_url(response.url)

        content = response.css("div.body")

        title = content.css("h1").xpath("string(.)").get()

        text_parts = content.css(
            "p, li"
        ).xpath("string(.)").getall()

        clean_title = (
            " ".join(title.split()).replace("¶", "").strip()
            if title
            else ""
        )

        clean_text = " ".join(
            " ".join(text_parts).split()
        )

        if clean_title and clean_text:

            document_id = hashlib.md5(
                canonical_url.encode()
            ).hexdigest()

            yield {
                "id": document_id,
                "title": clean_title,
                "url": canonical_url,
                "description": clean_text[:3000],
            }

        # Follow tutorial pages
        for href in response.css("a.reference.internal::attr(href)").getall():

            url = urljoin(response.url, href)
            url = self.normalize_url(url)

            if (
                url.startswith("https://docs.python.org/3/tutorial/")
                and url != canonical_url
                and "#" not in url
            ):
                yield response.follow(
                    url,
                    callback=self.parse
                )