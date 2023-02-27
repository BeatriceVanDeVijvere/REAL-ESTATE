from urllib3.filepost import writer
from usp.tree import sitemap_tree_for_homepage
import csv

file2 = 'original.csv'

def get_links_from_sitemap(homepage_url:'https://www.immoweb.be/nl', file2):
        ##use sitemap xml to get all the links on immoweb
        tree = sitemap_tree_for_homepage(homepage_url)
        ##go over all the links in the pages of the sitemap
        urls = [page.url for page in tree.all_pages()]
        ### if the beginning of the link matches  https://www.immoweb.be/nl/zoekertje we keep it
        prop_list = ["huis", "appartement", "industrie", "grond", "handelszaak", "kantoor",
                     "nieuwbouwproject-huizen", "nieuwbouwproject-appartementen", "garage", "vakantiehuis",
                     "opbrengsteigendom", "andere", "bed-and-breakfast", "stacaravan", "hotel", "camping",
                     "woonboot", "vakantiepark", "ander-huis"]
        i = 0
        file2 = open(file2, "w")
        for s in urls:
            for value in prop_list:
                substring = (f'https://www.immoweb.be/nl/zoekertje/{value}/te-koop')
                if substring in s:
                        i += 1
                        s = s.strip("https://")
                        file2.write(f'{s}\n')
                print(i)


get_links_from_sitemap('https://www.immoweb.be/nl', file2)


