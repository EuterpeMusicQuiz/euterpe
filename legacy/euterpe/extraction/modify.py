# -*- coding: utf-8 -*-

"""
Various functions to modify metadata represented as dictionary.
Operations available are :
- replacement
- completion
"""

def replace_metadata(data, new_data):
    '''
    Replaces <data> fields with <new_data> fields
    Except for empty fields and 'PATH' field
    '''
    for field in new_data:
        if field == 'PATH' or new_data[field] == None:
            continue
        data[field] = new_data[field]

def complete_metadata(data, new_data):
    '''
    Completes <data> fields with <new_data> fields
    Except for empty fields and 'PATH' field
    '''
    for field in new_data:
        if field == 'PATH' or new_data[field] == None or data[field] != None:
            continue
        data[field] = new_data[field]
