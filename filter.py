#!/usr/bin/env python
import json
import os
import babelfish
import pycountry

# todo currency export - code + translation
# there will be only code of currency attached to Country
def export_translations(country):
    translations = country["translations"]
    for translation in translations.keys():
        language = babelfish.Language.fromalpha3t(translation)
        directory = 'values-' + language.alpha2
        path = directory + os.path.sep + 'strings.xml'
        if not os.path.exists(directory):
            os.mkdir(directory)
        with open(path, 'a') as output:
            output.write('<string name=\"{0}_name_{1}\">{2}</string>\n'
                         .format(country['cca2'].lower(), 'common',
                                 str(translations[translation]['common'].encode('utf-8'))))
            output.write('<string name=\"{0}_name_{1}\">{2}</string>\n'
                         .format(country['cca2'].lower(), 'official',
                                 str(translations[translation]['official'].encode('utf-8'))))


countries = []

values_to_copy = ["area", "cca2", "cioc", "name", "borders"]
values_to_exclude = ["translations", "landlocked", "demonym"]

with open('countries.json', 'r') as data_file:
    data = json.load(data_file)

for country in data:
    new_country = {}
    if country["region"] == "Europe":
        for value in values_to_copy:
            new_country[value] = country[value]
        countries.append(new_country)
        export_translations(country)

with open('filtered_countries.json', 'w') as file:
    file.write(json.dumps(countries))
