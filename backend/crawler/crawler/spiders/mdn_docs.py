import scrapy
from urllib.parse import urljoin, urldefrag
import hashlib


class MdnDocsSpider(scrapy.Spider):
    name = "mdn_docs"

    allowed_domains = [
        "developer.mozilla.org"
    ]

    start_urls = [
        "https://developer.mozilla.org/en-US/docs/Web/JavaScript"
    ]

    custom_settings = {
        "DOWNLOAD_DELAY": 1,
        "ROBOTSTXT_OBEY": True,
        "CLOSESPIDER_PAGECOUNT": 100,
    }

    def normalize_url(self, url):
        url, _ = urldefrag(url)
        return url

    def parse(self, response):
        canonical_url = self.normalize_url(
            response.url
        )

        # Page title
        title = response.css(
            "h1"
        ).xpath("string(.)").get()

        # Main page content
        text_parts = response.css(
            "main p, main li"
        ).xpath("string(.)").getall()

        clean_title = (
            " ".join(title.split()).strip()
            if title
            else ""
        )

        clean_text = " ".join(
            " ".join(text_parts).split()
        )

        # Create document
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

        # Follow only JavaScript documentation pages
        for href in response.css(
            "a[href]"
        ).xpath("@href").getall():

            url = urljoin(
                response.url,
                href
            )

            url = self.normalize_url(url)

            if (
                url.startswith(
                    "https://developer.mozilla.org/en-US/docs/Web/JavaScript/"
                )
                and url != canonical_url
                and "#" not in url
            ):
                yield response.follow(
                    url,
                    callback=self.parse
                )