#!/usr/bin/python3

import click
import json
import requests

@click.command()
def main():
    #location_files = "/mnt/c/Users/Benjamin/Desktop/FourEels/Houses/" + \
    #       "Moving Out/Location Files/"
    #location_files = "/media/benji/OS/Users/Benjamin/Desktop/FourEels/" + \
    #        "Houses/Moving Out/Location Files/"
    location_files = "/home/benji/Documents/HouseScrape/Location Files/"
    with open(f"{location_files}location_list", "r") as location_list:
        for location in location_list:
            location = location.replace(" ", "_").lower().strip()
            url = f"https://www.home.co.uk/for_rent/{location}/current_rents?location={location}"
            click.echo("Downloading {} file...".format(location))
            payload = {"location" : location}
            headers = {
                #"Host" : "www.home.co.uk",
                #"Connection" : "keep-alive",
                "DNT" : "1",
                'User-Agent': 'My User Agent 1.0',
                #'From': 'youremail@domain.com'
            }
            r = requests.request(
                    method="get",
                    url=url,
                    #params=payload,
                    allow_redirects=False,
                    headers=headers
            )
            if r.ok:
                click.echo(f"Downloaded {location} file.")
                click.echo(f"Writing {location_files}{location}.html file...")
                with open(f"{location_files}{location}.html", "w") as loc_file:
                    loc_file.write(r.text)
                click.echo(f"Written {location} file.")
            else:
                click.echo(f"Request returned {r.status_code}")
            exit(0)


if __name__ == '__main__':
    main()

