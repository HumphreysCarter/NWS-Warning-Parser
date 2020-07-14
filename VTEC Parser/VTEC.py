"""
NWS Valid Time Event Code (VTEC) string parser
Based on NWS Directive NWSI 10-1703: https://www.nws.noaa.gov/directives/sym/pd01017003curr.pdf
07/14/2020

--------------------------------------------------------------------------------
Copyright (c) 2020, Carter J. Humphreys (chumphre@oswego.edu)
All rights reserved.
"""

from datetime import datetime
import pytz

def find_nthIndex(fullString, find, n):
    start = fullString.find(find)
    while start >= 0 and n > 1:
        start = fullString.find(find, start+len(find))
        n -= 1
    return start

def parseVTEC(vtec_string): 
    # Product Class
    k=vtec_string[find_nthIndex(vtec_string, '/', 0)+1:find_nthIndex(vtec_string, '.', 0)]

    # Actions 
    aaa=vtec_string[find_nthIndex(vtec_string, '.', 1)+1:find_nthIndex(vtec_string, '.', 2)]

    # Office ID
    cccc=vtec_string[find_nthIndex(vtec_string, '.', 2)+1:find_nthIndex(vtec_string, '.', 3)]

    # Phenomena
    pp=vtec_string[find_nthIndex(vtec_string, '.', 3)+1:find_nthIndex(vtec_string, '.', 4)]

    # Significance
    s=vtec_string[find_nthIndex(vtec_string, '.', 4)+1:find_nthIndex(vtec_string, '.', 5)]

    # Event Tracking Number
    nnnn=vtec_string[find_nthIndex(vtec_string, '.', 5)+1:find_nthIndex(vtec_string, '.', 6)]
    nnnn=int(nnnn)

    # Date/Time Group
    utc = pytz.utc
    begin=vtec_string[find_nthIndex(vtec_string, '.', 6)+1:find_nthIndex(vtec_string, '-', 0)]
    if begin == '000000T0000Z':
        begin = None
    else:
        begin=datetime.strptime(begin, '%y%m%dT%H%MZ')
        begin=utc.localize(begin)
    end=vtec_string[find_nthIndex(vtec_string, '-', 0)+1:find_nthIndex(vtec_string, '/', 2)]
    end=datetime.strptime(end, '%y%m%dT%H%MZ')
    end=utc.localize(end)
    
    
    # Return data
    return {'VTEC':vtec_string, 'ProductClass':k, 'Actions':aaa, 'OfficeID':cccc, 'Phenomena':pp, 'Significance':s, 'ETN':nnnn, 'EventBeginning':begin, 'EventEnding':end}
