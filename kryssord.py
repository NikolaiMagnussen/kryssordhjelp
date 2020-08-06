#!/usr/bin/env python3
import requests

def gratiskryssord(word):
    return _gratiskryssord(word, 0, [])

def _gratiskryssord(word, page, output):
    res = requests.get(f"https://gratiskryssord.no/api/crosswordbook/scroll/{word}/-1/{page}")
    data = res.json()
    if data['success'] == 1 and data['data']:
        return _gratiskryssord(word, page+1, [*output, *data['data']])
    return output



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
    if res is None:
        print("We could not find that word :(")
        return

    # Filter length
    if length != "":
        res_length = [x['list'] for x in res if x['strLength'] == str(length)]
    else:
        res_length = [x['list'] for x in res]
    res_flattened = [y for x in res_length for y in x]

    # Filter contains
    res_final = [x for x in res_flattened if contains in x]

    pprint(res_final, indent=4)


if __name__ == "__main__":
    main()
