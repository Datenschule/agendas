import scrapy
import re
import urlparse

from scrapy.shell import inspect_response
from datetime import datetime


class AgendaSpider(scrapy.Spider):
    name = 'agendaspider'
    start_urls = ['https://www.bundestag.de/apps/plenar/plenar/conferenceweekDetail.form?&week=26&year=2017']
    base_url = "https://www.bundestag.de/apps/plenar/plenar/conferenceweekDetail.form?&week={}&year={}"

    @staticmethod
    def parse_title_detail(lines):
        result = []
        current_top = ''
        pattern = re.compile('^[a-z]+\s*\)')

        if len(lines) < 1:
            return ['']

        if pattern.search(lines[0].strip()):
            for line in lines:
                line = line.strip()
                if line == "Drucksache":
                    continue
                if pattern.search(line):
                    if current_top != '':
                        result.append(current_top)
                    current_top = re.sub(pattern, '', line)
                else:
                    current_top += '\n' + line
            result.append(current_top)
        else:
            result = ['\n'.join(lines)]

        return [item.strip() for item in result]

    @staticmethod
    def separate_top(topstring):
        topstring = topstring.replace('+', ',')
        tops = topstring.split(',')
        for index, value in enumerate(tops):
            value = value.strip()
            value = value.replace('TOP', '')
            only_protocol = re.search('\*$', value) is not None
            value = re.sub('\*$', '', value)
            print('{0} {1} {2}'.format(index, value, only_protocol))

    def parse(self, response):
        #inspect_response(response, self)
        prevyear = response.css(".meta-slider::attr(data-previousyear)").extract_first()
        prevweek = response.css(".meta-slider::attr(data-previousweeknumber)").extract_first()
        # nextyear = response.css(".meta-slider::attr(data-nextyear)").extract_first()
        # nextweek = response.css(".meta-slider::attr(data-nextweeknumber)").extract_first()
        for table in response.css('table'):
            caption = table.css("caption::text").extract_first()
            session = re.search('(\d+)\. Sitzung', caption).group(1)
            date_reg = re.search('(\d*)\. [A-Za-z]* \d*', caption)
            date = '' if date_reg is None else date_reg.group()
            for (index, tr) in enumerate(table.css("tbody tr")[1:-1]):  # dont use "Sitzungseroeffnung" and "Sitzungsende"
                number = tr.css('td[data-th="TOP"] p::text').extract_first()
                number_clean = '' if number is None else number.strip()
                title_raw = tr.css('td[data-th="Thema"] a.bt-top-collapser::text').extract_first()
                title = '' if title_raw is None else title_raw.strip()
                title_detail = tr.css('td[data-th="Thema"] .bt-top-collapse').extract_first()

                time = tr.css('td[data-th="Uhrzeit"] p::text').extract_first()
                time2 = table.css("tbody tr")[index + 1 + 1].css('td[data-th="Uhrzeit"] p::text').extract_first() # get next index, need to add 2 because we are starting at index 1
                FMT = '%H:%M'
                tdelta = datetime.strptime(time2, FMT) - datetime.strptime(time, FMT)

                # self.separate_top(number_clean)
                description_raw = tr.css('td[data-th="Status/ Abstimmung"] p::text').extract_first()
                description = '' if description_raw is None else description_raw.strip()

                # print(title_detail)
                yield {"number": number_clean,
                       "detail": title_detail,
                       "title": title.strip(),
                       "description": description.strip(),
                       "session": session,
                       "week": urlparse.parse_qs(urlparse.urlparse(response.url).query)['week'][0],
                       "year": urlparse.parse_qs(urlparse.urlparse(response.url).query)['year'][0],
                       "date": date,
                       "duration": tdelta.seconds / 60
                }

                #if session == "243" and number_clean == "9 + ZP 1-3":
                #    inspect_response(response, self)
        # print("------------")
        # print(self.base_url.format(prevweek, prevyear))
        # print(response.url)
        # print(self.base_url.format(nextweek, nextyear))
        # if response.url == 'https://www.bundestag.de/apps/plenar/plenar/conferenceweekDetail.form?&week=48&year=2016':
            #inspect_response(response, self)
        yield scrapy.Request(response.urljoin(self.base_url.format(prevweek, prevyear)), callback=self.parse)