#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2021 Jordi Mas i Hernandez <jmas@softcatala.org>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place - Suite 330,
# Boston, MA 02111-1307, USA.

import json
import sys
#import ijson

def save(values, append = False):
    with open('terms.json', 'w') as outfile:
        json.dump(values, outfile, skipkeys=True, indent=4, ensure_ascii=False)

def _load_wikidata():
    with open('wikidata/terms.json', 'r') as fh:
        wikidata = json.load(fh)

    print(f"Wikidata read {len(wikidata)} items")
    return wikidata

def _load_wordnet():
    with open('wordnet/terms.json', 'r') as fh:
        wordnet = json.load(fh)

    print(f"Wordnet read {len(wordnet)} items")
    return wordnet


#    wikidata = ijson.items('wikidata/terms.json', 'item', use_float=True)

#    print(f"Wikidata read")
 #   return wikidata


def _wordnet_todict(wordnet):
    id_item = {}
    for item in wordnet:
        id = item['id']
        new_id = item['id'][1:] + "-" + item['id'][0:1]
        item['id'] = new_id
        id_item[new_id] = item

    return id_item


def get_synset_id(item):
    
    synset_id = None

    property_keys = item['claims']['P8814']
#    print(data['datavalue']['value'])
    #['datavalue']['value']
    for property_key in property_keys:
#        print("key: " + str(property_key))
        if 'mainsnak' not in property_key:
            continue

        synset_id = property_key['mainsnak']['datavalue']['value']
        break

    return synset_id

def get_en_label_description(item):
    label = ''
    description = ''

    try:
        label = item['labels']['en']['value']
        if 'en' in item['descriptions']:
            description = item['descriptions']['en']['value']
        
    except:
        pass

    return label, description


def _wikidata_todict(items):
    id_item = {}
    
    for item in items:
        en_label, en_description = get_en_label_description(item)
        synset_id = get_synset_id(item)

        new_item = {}
        new_item['en_label'] = en_label
        new_item['en_description'] = en_description
        id_item[synset_id] = new_item

    return id_item

def main():
    wordnet_list = _load_wordnet()
    wordnet_dict = _wordnet_todict(wordnet_list)
    wikidata = _load_wikidata()
    wikidata_dict = _wikidata_todict(wikidata)

    items_found = 0
    for synset_id in wikidata_dict:
        if synset_id not in wordnet_dict:
            continue

        print("---")
        print(synset_id)
        print(f"wikidata: {wikidata_dict[synset_id]}")
        print(f"wordnet: {wordnet_dict[synset_id]}")
        items_found += 1

    print(f"items_found: {items_found}")
    
if __name__ == "__main__":
    print("Merge sources")
    main()
