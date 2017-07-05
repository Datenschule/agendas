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
        nextyear = response.css(".meta-slider::attr(data-nextyear)").extract_first()
        nextweek = response.css(".meta-slider::attr(data-nextweeknumber)").extract_first()
        #inspect_response(response, self)
        for table in response.css('table'):
            caption = table.css("caption::text").extract_first()
            session = re.search('(\d+)\. Sitzung', caption).group(1)
            #print(caption)
            #print(session)
            for tr in table.css("tbody tr")[1:-1]:  # dont use "Sitzungseroeffnung" and "Sitzungsende"
                number = tr.css("td:nth-child(2)::text").extract_first()
                number_clean = '' if number is None else number.strip()
                title_raw = tr.css("td:nth-child(3) a.bt-top-collapser::text").extract_first()
                title = '' if title_raw is None else title_raw.strip()
                description_raw = tr.css("td:nth-child(3) div.bt-top-collapse::text").extract_first()
                description = '' if description_raw is None else description_raw.strip()
                #inspect_response(response, self)
                # if (len(number_clean) > 0):
                yield {"number": number_clean,
                       "title": title.strip(),
                       "description": description.strip(),
                       "session": session,
                       "period": 18
                }

                # if prevweek ==
        print("------------")
        print(self.base_url.format(prevweek, prevyear))
        print(response.url)
        print(self.base_url.format(nextweek, nextyear))
        # if response.url == 'https://www.bundestag.de/apps/plenar/plenar/conferenceweekDetail.form?&week=48&year=2016':
            #inspect_response(response, self)
        yield scrapy.Request(response.urljoin(self.base_url.format(prevweek, prevyear)), callback=self.parse)