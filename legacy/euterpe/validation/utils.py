# -*- coding: utf-8 -*-

from unicodedata import normalize, combining

## Dictionaries ##

AncientGreek = {
'α': 'a',
'β': 'b',
'γ': 'g',
'δ': 'd',
'ε': 'é',
'ζ': 'z',
'η': 'ê',
'θ': 'th',
'ι': 'i',
'κ': 'k',
'λ': 'l',
'μ': 'm',
'ν': 'n',
'ξ': 'x',
'ο': 'o',
'π': 'p',
'ρ': 'r',
'σ': 's',
'τ': 't',
'υ': 'u',
'φ': 'ph',
'χ': 'ch',
'ψ': 'ps',
'ω': 'o',
'Α': 'A',
'Β': 'B',
'Γ': 'G',
'Δ': 'D',
'Ε': 'É',
'Ζ': 'Z',
'Η': 'Ê',
'Θ': 'TH',
'Ι': 'I',
'Κ': 'K',
'Λ': 'L',
'Μ': 'M',
'Ν': 'N',
'Ξ': 'X',
'Ο': 'O',
'Π': 'P',
'Ρ': 'R',
'Σ': 'S',
'Τ': 'T',
'Υ': 'U',
'Φ': 'PH',
'Χ': 'CH',
'Ψ': 'PS',
'Ω': 'O'
}

## Functions used to simplify strings ##

def without_space(string):
    ''' Returns <string> without its spaces'''
    return string.replace(" ", "")

def without_accents(string):
    ''' Returns <string> with accents replaced by unaccented letters'''
    nfkd_form = normalize('NFKD', string)
    return u"".join([c for c in nfkd_form if not combining(c)])

def without_dots(string):
    ''' Returns <string> without its dots'''
    return string.replace(".", "")

def without_slashes(string):
    ''' Returns <string> without its slashes'''
    return string.replace("/", "")

def replace_special_characters(string):
    return string.replace("ø", "o").replace("Ø", "O").replace("œ", "oe").replace("Œ", "OE").replace("æ", "ae").replace("Æ", "AE")

def replace_ancient_greek_characters(string):
    for c in string:
        if c in AncientGreek:
            string = string.replace(c, AncientGreek[c])
    return string

## Combination of all previous functions ##

def simplify_str(string):
    return without_slashes(without_dots(without_accents(without_space(replace_ancient_greek_characters(replace_special_characters(string))).lower())))
