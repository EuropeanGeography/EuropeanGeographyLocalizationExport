#!/usr/bin/env python
import json
import os
import sys
import babelfish
import pycountry

output_directory = "output"


def append_to_file(path, string):
    with open(path, 'a') as output:
        output.write(string)


def get_path(alpha3t_code):
    language = babelfish.Language.fromalpha3t(alpha3t_code)
    output_path = output_directory
    directory = 'values-' + language.alpha2
    if language == babelfish.Language('eng'):
        directory = 'values'
    path = output_path + os.path.sep + directory + os.path.sep
    if not os.path.exists(path):
        os.makedirs(path)
    return path + 'strings.xml'


def format_string(prefix, suffix, text):
    pattern = '<string name=\"{0}_{1}\">{2}</string>\n'
    return pattern.format(str(prefix.encode('utf-8')), str(suffix.encode('utf-8')), str(text.encode('utf-8')))


def export_country_names(country):
    translations = country["translations"]
    for translation in translations.keys():
        append_to_file(get_path(translation),
                       format_string(country['cca2'].lower(), 'name_common', translations[translation]['common']) +
                       format_string(country['cca2'].lower(), 'name_official', translations[translation]['official']))
    append_to_file(get_path('eng'),
                   format_string(country['cca2'].lower(), 'name_common', country["name"]['common']) +
                   format_string(country['cca2'].lower(), 'name_official', country["name"]['official']))


def export_currencies_names(currencies):
    for currency in currencies:
        append_to_file(get_path('eng'),
                       format_string(currency.lower(), 'currency_name', pycountry.currencies.get(letter=currency).name))


def export_languages_names(languages):
    for key in languages.keys():
        append_to_file(get_path('eng'),
                       format_string(key.lower(), 'language_name', languages[key]))


def export_capital_names(country):
    capital = country["capital"]
    append_to_file(get_path('eng'),
                   format_string(country['cca2'].lower(), "capital", capital))


def main(source_path):
    countries = []

    values_to_exclude = ["translations", "landlocked", "demonym"]

    with open(source_path, 'r') as data_file:
        data = json.load(data_file)

    currencies = []
    languages = {}
    for country in data:
        new_country = {}
        if country["region"] == "Europe":
            currencies += country["currency"]
            languages.update(country["languages"])
            for value in country:
                if value not in values_to_exclude:
                    new_country[value] = country[value]
            countries.append(new_country)
            export_country_names(country)
            export_capital_names(country)

    export_currencies_names(set(currencies))
    export_languages_names(languages)

    with open('filtered_countries.json', 'w') as file:
        file.write(json.dumps(countries))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: filter.py source_file.json")
    else:
        main(source_path=sys.argv[1])
