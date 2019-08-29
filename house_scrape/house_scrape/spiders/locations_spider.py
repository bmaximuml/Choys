import scrapy

class LocationsSpider(scrapy.Spider):
    name = "locations"
    start_urls = [
#            'https://www.home.co.uk/for_rent/current_rents_by_town.htm'
            'https://www.home.co.uk/for_rent/abridge/current_rents?location=abridge',
            'https://www.home.co.uk/for_rent/theydon_bois/current_rents?location=theydon_bois',
    ]

    def parse(self, response):
        yield {
            'location_name' : response.css('title::text').re(
                    '(?!Home\.co\.uk:)[A-Za-z\- ]*(?=Market Rent Summary)')[0].strip()
            'total_properties' : response.css('div:nth-child(3) \
                    tr:nth-child(1) td:nth-child(2)::text').get(),
            'average_rent' : response.css('div:nth-child(3) tr:nth-child(3) \
                    td:nth-child(2)::text').get(),
            'rent_under_250' : response.css('div:nth-child(6) tr:nth-child(2) \
                    td:nth-child(2)::text').get(),
            'rent_250_to_500' : reponse.css('div:nth-child(6) tr:nth-child(3) \
                    td:nth-child(2)').get(),
        }
        page = response.url.split("/")[-2]
        filename = 'locations-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)
