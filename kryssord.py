#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup

def gratiskryssord(word):
    return _gratiskryssord(word, 0, [])


def _gratiskryssord(word, page, output):
    res = requests.get(f"https://gratiskryssord.no/api/crosswordbook/scroll/{word}/-1/{page}")
    data = res.json()
    if data['success'] == 1 and data['data']:
        return _gratiskryssord(word, page+1, [*output, *data['data']])
    return output


def kryssordkjempen(word):
    res = requests.get(f"https://kryssordkjempen.no/synoapp/search.php?query={word}&pattern=")
    soup = BeautifulSoup(res.text, 'html.parser')
    results = soup.find("ul", "resultlist")
    out = []
    if "Søket ditt ga ingen treff" not in results.text:
        for letter in results.find_all("li", "header"):
            out.append({"strLength": letter.find("h2").text.split()[-2],
                         "list": [synonym.find("a").text for synonym in letter.find_all("li", "synonym")]})
    return out


def main():
    from pprint import pprint
    word = input("word: ")
    length = input("leng: ")
    contains = input("patt: ")

    # Get results
    if word == "":
        print("Error: you must provide a word!")
        return
    res = gratiskryssord(word)
    res2 = kryssordkjempen(word)
    if res is None and res2 is None:
        print("We could not find that word :(")
        return

    results = set()

    # Filter length
    if res is not None:
        if length != "":
            res_length = [x['list'] for x in res if x['strLength'] == str(length)]
        else:
            res_length = [x['list'] for x in res]
        res_flattened = [y for x in res_length for y in x]

        # Filter contains
        res_final = [x for x in res_flattened if contains in x]
    else:
        res_final = []

    # Filter length
    if res2 is not None:
        if length != "":
            res_length2 = [x['list'] for x in res2 if x['strLength'] == str(length)]
        else:
            res_length2 = [x['list'] for x in res2]
        res_flattened2 = [y for x in res_length2 for y in x]

        # Filter contains
        res_final2 = [x for x in res_flattened2 if contains in x]
    else:
        res_final2 = []

    # Print output
    final = set(res_final + res_final2)
    pprint(final, indent=4)


if __name__ == "__main__":
    main()
