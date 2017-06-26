import scrapy
import re

from scrapy.shell import inspect_response


class AgendaSpider(scrapy.Spider):
    name = 'agendaspider'
    start_urls = ['https://www.bundestag.de/apps/plenar/plenar/conferenceweekDetail.form?&week=26&year=2017']
    base_url = "https://www.bundestag.de/apps/plenar/plenar/conferenceweekDetail.form?&week={}&year={}"

    def parse(self, response):
        prevyear = response.css(".meta-slider::attr(data-previousyear)").extract_first()
        prevweek = response.css(".meta-slider::attr(data-previousweeknumber)").extract_first()

        for table in response.css('table'):
            caption = table.css("caption::text").extract_first()
            session = re.search('(\d+)\. Sitzung', caption).group(1)

            numbers = [entry.strip() for entry in table.css("tbody tr td:nth-child(2) *::text").extract()]
            titles = ["\n".join([a.strip() for a in td.css("*::text").extract()]) for td in table.css("tbody tr td:nth-child(3)")]
            # inspect_response(response, self)

            assert len(numbers) == len(titles)

            agenda = [{"number": number,
                       "title": title.strip(),
                       "session": session,
                       "period": 18} for number, title in zip(numbers, titles) if number]
            for item in agenda:
                yield item

        yield scrapy.Request(response.urljoin(self.base_url.format(prevweek, prevyear)), callback=self.parse)