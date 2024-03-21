import scrapy
from scrapy.crawler import CrawlerProcess
from urllib.parse import urljoin
from scrapy.shell import inspect_response



class Scrape(scrapy.Spider):
    name = "my_spider"
    base_url = "https://dea.gov.in/central-government-borrowings"

    def start_requests(self):
        yield scrapy.Request(
            url=self.base_url,
            callback=self.parse,
        )

    def parse(self, response):
        # inspect_response(response, self)
        pdf_links = response.css(".pdf_attachment ::attr(href)").getall()
        titles = response.css(".views-field-title::text").getall()
        titles = titles[1:] 

        for link, title in zip(pdf_links, titles):
            yield scrapy.Request(
                url=urljoin(self.base_url, link),
                callback=self.save_pdf,
                meta={"titles": title.strip()},
            )

        

        #Following next pages
        next_page = response.css(".pager-next a::attr(href)").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def save_pdf(self, response):
        title = response.meta["titles"]
        folder_path = "/Users/apple/Desktop/My_projects/Central Borrowings"
        try:
            with open(f"{folder_path}/{title}.pdf", "wb") as pdf_file:
                pdf_file.write(response.body)
        except Exception as e:
            self.logger.error(f"Failed to save PDF: {e}")

def main():
    process = CrawlerProcess()
    process.crawl(Scrape)
    process.start()

if __name__ == "__main__":
    main()
