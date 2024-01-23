import scrapy
from scrapy import Request, Spider
from scrapy.crawler import CrawlerProcess
from urllib import parse
from scrapy import  Request


class Scrape(Spider):
    name = "my_spider"

    def __init__(self):
        self.base_url = "https://dea.gov.in/central-government-borrowings"


    
    def start_requests(self):
        yield Request(
            url=self.base_url,     #copies the entire data from start page
            callback=self.years,   #passing to next fuction i.e. years
        )



    def years(self, response):
        """
        collecting download url of pdfs and pasing to save_pdf function

        Args:
            response : body of base url page
        """
        inspect_response(response, self)
        pdf_links = response.css(".pdf_attachment ::attr(href)").extract()
        titles = response.css(".views-field-title::text").extract()
        titles = titles[1:]
        
        for link, title in zip(pdf_links, titles):
            yield Request(
                url=link,
                callback=self.save_pdf,
                meta={
                    "titles": title,
                },
            )
            
            #for multple pages
        if response.css(".pager-next"):
            self.logger.debug("REQUEST MADE TO NEXT PAGE")
            yield Request(
                url=parse.urljoin(
                    self.base_url, response.css(".pager-next a::attr(href)").get()
                ),
                callback=self.years,
            )
            
            #savig the path into the local machine
    def save_pdf(self, response):
        
        title = response.meta["titles"].strip()
        folder_path = r"C:\Users\putta\OneDrive\Desktop\Scrapped"
        with open(f"{folder_path}/{title}.pdf", "wb") as pdf_file:
            pdf_file.write(response.body)
        pdf_file.close()


      #calling all the functions ordered by            
def main():
    process = CrawlerProcess()
    process.crawl(Scrape)
    process.start()


if __name__ == "__main__":
    main()