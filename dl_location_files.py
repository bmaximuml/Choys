#!/usr/bin/python3

import click
import json
import requests

@click.command()
def main():
    with open("/mnt/c/Users/Benjamin/Desktop/FourEels/Houses/Moving Out/" + \
              "Location Files/location_list", "r") as location_list:
        for location in location_list:
            location = location.replace(" ", "_").lower().strip()
            url = "https://www.home.co.uk/for_rent/{l}/current_rents?location={l}".format(l=location)
            print(url)
            click.echo("Downloading {} file...".format(location))
            r = requests.get(url)
            click.echo("Downloaded {} file.".format(location))
            click.echo("Writing {} file...".format(location))
            with open("/mnt/c/Users/Benjamin/Desktop/FourEels/Houses/Moving "+ \
                      "Out/Location Files/{}".format(location), "w") as loc_file:
                loc_file.write(r.text)
            click.echo("Written {} file.")
            #print(r.text)
            exit(0)
            #print(json.loads(r.json))
            #for ionkjjin r.json:
                #print(i)


if __name__ == '__main__':
    main()

