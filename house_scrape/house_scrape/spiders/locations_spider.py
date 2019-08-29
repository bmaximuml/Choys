import logging
import scrapy


class LocationsSpider(scrapy.Spider):
    name = "locations"
    start_urls = [
            'https://www.home.co.uk/for_rent/current_rents_by_town.htm'
            # 'https://www.home.co.uk/for_rent/abridge/current_rents?location=abridge',
            # 'https://www.home.co.uk/for_rent/theydon_bois/current_rents?location=theydon_bois',
    ]

    def parse(self, response):
        logger = logging.getLogger()
        # for page in current_rents_by_town
            # if market rent summary:
                # yield, then continue
            # else
                # for page in page
                # if MRS, etc
        if 'Market Rents' in response.css('title::text').get():
            for li in response.css('li a::attr(href)').getall():
                yield response.follow(li, callback=self.parse)
        elif 'Market Rent Summary' in response.css('title::text').get():
            current_location = response.css('title::text').re(
                '(?!Home\.co\.uk:)[A-Za-z\- ]*(?=Market Rent Summary)')[0].strip()
            logger.info(f'Crawling {current_location}')
            yield {
                'location_name': current_location,
                'total_properties': response.css('div:nth-child(3) \
                        tr:nth-child(1) td:nth-child(2)::text').get(),
                'average_rent': response.css('div:nth-child(3) tr:nth-child(3) \
                        td:nth-child(2)::text').re('(?!£)[0-9,]*(?= pcm)')[0],
                'rent_under_250': response.css('div:nth-child(6) tr:nth-child(2) \
                        td:nth-child(2)::text').get(),
                'rent_250_to_500': response.css('div:nth-child(6) tr:nth-child(3) \
                        td:nth-child(2)::text').get(),
            }
        # if 'MyHome Login' in response.css('title::text').get():
        elif 'Website Error' in response.css('title::text').get():
            logger.warning('Website error detected.')
        else:
            yield {}
        page = response.url.split("/")[-2]
        filename = 'Location Files/locations-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)
