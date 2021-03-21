"""
NWS Valid Time Event Code (VTEC) string parser
Based on NWS Directive NWSI 10-1703: https://www.nws.noaa.gov/directives/sym/pd01017003curr.pdf
07/14/2020, updated 03/20/2021

--------------------------------------------------------------------------------
Copyright (c) 2021, Carter J. Humphreys (carter.humphreys@lake-effect.dev)
https://github.com/HumphreysCarter/NWS-Warning-Parser
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
    
    # Office Info
    office=get_nws_office(cccc)

    # Phenomena
    pp=vtec_string[find_nthIndex(vtec_string, '.', 3)+1:find_nthIndex(vtec_string, '.', 4)]
    pp_str=get_product_str(pp)

    # Significance
    s=vtec_string[find_nthIndex(vtec_string, '.', 4)+1:find_nthIndex(vtec_string, '.', 5)]
    s_str=get_significance_str(s)

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
    return {'VTEC':vtec_string, 'ProductClass':k, 'Actions':aaa, 'OfficeID':cccc, 'Office':office, 'Phenomena':(pp, pp_str), 'Significance':(s, s_str), 'ETN':nnnn, 'EventBeginning':begin, 'EventEnding':end}

def get_product_str(pp):
    pp_to_str = {'AF':'Ashfall (land)',
            'AS':'Air Stagnation',
            'BH':'Beach Hazard',
            'BW':'Brisk Wind',
            'BZ':'Blizzard',
            'CF':'Coastal Flood',
            'DF':'Debris Flow',
            'DS':'Dust Storm',
            'EC':'Extreme Cold',
            'EH':'Excessive Heat',
            'EW':'Extreme Wind',
            'FA':'Areal Flood',
            'FF':'Flash Flood',
            'FG':'Dense Fog (land)',
            'FL':'Flood',
            'FR':'Frost',
            'FW':'Fire Weather',
            'FZ':'Freeze',
            'GL':'Gale',
            'HF':'Hurricane Force Wind',
            'HT':'Heat',
            'HU':'Hurricane',
            'HW':'High Wind',
            'HY':'Hydrologic',
            'HZ':'Hard Freeze',
            'IS':'Ice Storm',
            'LE':'Lake Effect Snow',
            'LO':'Low Water',
            'LS':'Lakeshore Flood',
            'LW':'Lake Wind',
            'MA':'Marine',
            'MF':'Dense Fog (marine)',
            'MH':'Ashfall (marine)',
            'MS':'Dense Smoke (marine)',
            'RB':'Small Craft for Rough Bar',
            'RP':'Rip Current Risk',
            'SC':'Small Craft',
            'SE':'Hazardous Seas',
            'SI':'Small Craft for Winds',
            'SM':'Dense Smoke (land)',
            'SQ':'Snow Squall',
            'SR':'Storm',
            'SS':'Storm Surge',
            'SU':'High Surf',
            'SV':'Severe Thunderstorm',
            'SW':'Small Craft for Hazardous Seas',
            'TO':'Tornado',
            'TR':'Tropical Storm',
            'TS':'Tsunami',
            'TY':'Typhoon',
            'UP':'Heavy Freezing Spray',
            'WC':'Wind Chill',
            'WI':'Wind',
            'WS':'Winter Storm',
            'WW':'Winter Weather',
            'ZF':'Freezing Fog',
            'ZR':'Freezing Rain',
            'ZY':'Freezing Spray'}

    return pp_to_str[pp]


def get_significance_str(s):
    s_to_str = {'W':'Warning', 'A':'Watch', 'Y':'Advisory', 'S':'Statement', 'F':'Forecast', 'O':'Outlook', 'S':'Synopsis'}
    
    return s_to_str[s]
        
        
def get_nws_office(cccc):
    office_ids = {'KABR':{'ShortID':'ABR', 'City':'Aberdeen', 'State':'SD'}, 
    'KALY':{'ShortID':'ALY', 'City':'Albany', 'State':'NY'}, 
    'KABQ':{'ShortID':'ABQ', 'City':'Albuquerque', 'State':'NM'}, 
    'KAMA':{'ShortID':'AMA', 'City':'Amarillo', 'State':'TX'}, 
    'KAFC':{'ShortID':'AFC', 'City':'Anchorage', 'State':'AK'}, 
    'KANC':{'ShortID':'ANC', 'City':'Anchorage', 'State':'AK'}, 
    'KFFC':{'ShortID':'FFC', 'City':'Atlanta', 'State':'GA'}, 
    'KEWX':{'ShortID':'EWX', 'City':'Austin/San Antonio', 'State':'TX'}, 
    'KBYZ':{'ShortID':'BYZ', 'City':'Billings', 'State':'MT'}, 
    'KBGM':{'ShortID':'BGM', 'City':'Binghamton', 'State':'NY'}, 
    'KBMX':{'ShortID':'BMX', 'City':'Birmingham', 'State':'AL'}, 
    'KBIS':{'ShortID':'BIS', 'City':'Bismarck', 'State':'ND'}, 
    'KRNK':{'ShortID':'RNK', 'City':'Blacksburg', 'State':'VA'}, 
    'KBOI':{'ShortID':'BOI', 'City':'Boise', 'State':'ID'}, 
    'KBOX':{'ShortID':'BOX', 'City':'Boston', 'State':'MA'}, 
    'KBRO':{'ShortID':'BRO', 'City':'Brownsville', 'State':'TX'}, 
    'KBUF':{'ShortID':'BUF', 'City':'Buffalo', 'State':'NY'}, 
    'KBTV':{'ShortID':'BTV', 'City':'Burlington', 'State':'VT'}, 
    'KCAR':{'ShortID':'CAR', 'City':'Caribou', 'State':'ME'}, 
    'KCHS':{'ShortID':'CHS', 'City':'Charleston', 'State':'SC'}, 
    'KRLX':{'ShortID':'RLX', 'City':'Charleston', 'State':'WV'}, 
    'KCYS':{'ShortID':'CYS', 'City':'Cheyenne', 'State':'WY'}, 
    'KLOT':{'ShortID':'LOT', 'City':'Chicago', 'State':'IL'}, 
    'KCLE':{'ShortID':'CLE', 'City':'Cleveland', 'State':'OH'}, 
    'KCAE':{'ShortID':'CAE', 'City':'Columbia', 'State':'SC'}, 
    'KCRP':{'ShortID':'CRP', 'City':'Corpus Christi', 'State':'TX'}, 
    'KFWD':{'ShortID':'FWD', 'City':'Dallas/Fort Worth', 'State':'TX'}, 
    'KBOU':{'ShortID':'BOU', 'City':'Denver/Boulder', 'State':'CO'}, 
    'KDMX':{'ShortID':'DMX', 'City':'Des Moines', 'State':'IA'}, 
    'KDTX':{'ShortID':'DTX', 'City':'Detroit', 'State':'MI'}, 
    'KDDC':{'ShortID':'DDC', 'City':'Dodge City', 'State':'KS'}, 
    'KDLH':{'ShortID':'DLH', 'City':'Duluth', 'State':'MN'}, 
    'KEPZ':{'ShortID':'EPZ', 'City':'El Paso', 'State':'TX'}, 
    'KLKN':{'ShortID':'LKN', 'City':'Elko', 'State':'NV'}, 
    'KEKA':{'ShortID':'EKA', 'City':'Eureka', 'State':'CA'}, 
    'KAFG':{'ShortID':'AFG', 'City':'Fairbanks', 'State':'AK'}, 
    'KFGZ':{'ShortID':'FGZ', 'City':'Flagstaff', 'State':'AZ'}, 
    'KAPX':{'ShortID':'APX', 'City':'Gaylord', 'State':'MI'}, 
    'KGGW':{'ShortID':'GGW', 'City':'Glasgow', 'State':'MT'}, 
    'KGLD':{'ShortID':'GLD', 'City':'Goodland', 'State':'KS'}, 
    'KFGF':{'ShortID':'FGF', 'City':'Grand Forks', 'State':'ND'}, 
    'KGJT':{'ShortID':'GJT', 'City':'Grand Junction', 'State':'CO'}, 
    'KGRR':{'ShortID':'GRR', 'City':'Grand Rapids', 'State':'MI'}, 
    'KGYX':{'ShortID':'GYX', 'City':'Gray', 'State':'ME'}, 
    'KTFX':{'ShortID':'TFX', 'City':'Great Falls', 'State':'MT'}, 
    'KGRB':{'ShortID':'GRB', 'City':'Green Bay', 'State':'WI'}, 
    'KGSP':{'ShortID':'GSP', 'City':'Greer', 'State':'SC'}, 
    'KGUM':{'ShortID':'GUM', 'City':'Guam', 'State':'GU'}, 
    'KHNX':{'ShortID':'HNX', 'City':'Hanford', 'State':'CA'}, 
    'KGID':{'ShortID':'GID', 'City':'Hastings', 'State':'NE'}, 
    'KHFO':{'ShortID':'HFO', 'City':'Honolulu', 'State':'HI'}, 
    'KHGX':{'ShortID':'HGX', 'City':'Houston', 'State':'TX'}, 
    'KHUN':{'ShortID':'HUN', 'City':'Huntsville', 'State':'AL'}, 
    'KIND':{'ShortID':'IND', 'City':'Indianapolis', 'State':'IN'}, 
    'KJAN':{'ShortID':'JAN', 'City':'Jackson', 'State':'MS'}, 
    'KJKL':{'ShortID':'JKL', 'City':'Jackson', 'State':'KY'}, 
    'KJAX':{'ShortID':'JAX', 'City':'Jacksonville', 'State':'FL'}, 
    'KAJK':{'ShortID':'AJK', 'City':'Juneau', 'State':'AK'}, 
    'KEAX':{'ShortID':'EAX', 'City':'Kansas City', 'State':'MO'}, 
    'KEYW':{'ShortID':'EYW', 'City':'Key West', 'State':'FL'}, 
    'KARX':{'ShortID':'ARX', 'City':'La Crosse', 'State':'WI'}, 
    'KLCH':{'ShortID':'LCH', 'City':'Lake Charles', 'State':'LA'}, 
    'KVEF':{'ShortID':'VEF', 'City':'Las Vegas', 'State':'NV'}, 
    'KILX':{'ShortID':'ILX', 'City':'Lincoln', 'State':'IL'}, 
    'KLZK':{'ShortID':'LZK', 'City':'Little Rock', 'State':'AR'}, 
    'KLOX':{'ShortID':'LOX', 'City':'Los Angeles', 'State':'CA'}, 
    'KLMK':{'ShortID':'LMK', 'City':'Louisville', 'State':'KY'}, 
    'KLUB':{'ShortID':'LUB', 'City':'Lubbock', 'State':'TX'}, 
    'KMQT':{'ShortID':'MQT', 'City':'Marquette', 'State':'MI'}, 
    'KMFR':{'ShortID':'MFR', 'City':'Medford', 'State':'OR'}, 
    'KMLB':{'ShortID':'MLB', 'City':'Melbourne', 'State':'FL'}, 
    'KMEG':{'ShortID':'MEG', 'City':'Memphis', 'State':'TN'}, 
    'KMFL':{'ShortID':'MFL', 'City':'Miami', 'State':'FL'}, 
    'KMAF':{'ShortID':'MAF', 'City':'Midland/Odessa', 'State':'TX'}, 
    'KMKX':{'ShortID':'MKX', 'City':'Milwaukee', 'State':'WI'}, 
    'KMSO':{'ShortID':'MSO', 'City':'Missoula', 'State':'MT'}, 
    'KMOB':{'ShortID':'MOB', 'City':'Mobile', 'State':'AL'}, 
    'KMHX':{'ShortID':'MHX', 'City':'Morehead City', 'State':'NC'}, 
    'KMRX':{'ShortID':'MRX', 'City':'Morristown', 'State':'TN'}, 
    'KPHI':{'ShortID':'PHI', 'City':'Mount Holly', 'State':'NJ'}, 
    'KOHX':{'ShortID':'OHX', 'City':'Nashville', 'State':'TN'}, 
    'KLIX':{'ShortID':'LIX', 'City':'New Orleans', 'State':'LA'}, 
    'KOKX':{'ShortID':'OKX', 'City':'New York City', 'State':'NY'}, 
    'KOUN':{'ShortID':'OUN', 'City':'Norman', 'State':'OK'}, 
    'KLBF':{'ShortID':'LBF', 'City':'North Platte', 'State':'NE'}, 
    'KIWX':{'ShortID':'IWX', 'City':'Nrn. Indiana', 'State':'IN'}, 
    'KOAX':{'ShortID':'OAX', 'City':'Omaha', 'State':'NE'}, 
    'KPAH':{'ShortID':'PAH', 'City':'Paducah', 'State':'KY'}, 
    'KPDT':{'ShortID':'PDT', 'City':'Pendleton', 'State':'OR'}, 
    'KPSR':{'ShortID':'PSR', 'City':'Phoenix', 'State':'AZ'}, 
    'KPBZ':{'ShortID':'PBZ', 'City':'Pittsburgh', 'State':'PA'}, 
    'KPIH':{'ShortID':'PIH', 'City':'Pocatello', 'State':'ID'}, 
    'KPQR':{'ShortID':'PQR', 'City':'Portland', 'State':'OR'}, 
    'KPUB':{'ShortID':'PUB', 'City':'Pueblo', 'State':'CO'}, 
    'KDVN':{'ShortID':'DVN', 'City':'Quad Cities', 'State':'IA'}, 
    'KRAH':{'ShortID':'RAH', 'City':'Raleigh', 'State':'NC'}, 
    'KUNR':{'ShortID':'UNR', 'City':'Rapid City', 'State':'SD'}, 
    'KREV':{'ShortID':'REV', 'City':'Reno', 'State':'NV'}, 
    'KRIW':{'ShortID':'RIW', 'City':'Riverton', 'State':'WY'}, 
    'KSTO':{'ShortID':'STO', 'City':'Sacramento', 'State':'CA'}, 
    'KSLC':{'ShortID':'SLC', 'City':'Salt Lake City', 'State':'UT'}, 
    'KSJT':{'ShortID':'SJT', 'City':'San Angelo', 'State':'TX'}, 
    'KSGX':{'ShortID':'SGX', 'City':'San Diego', 'State':'CA'}, 
    'KMTR':{'ShortID':'MTR', 'City':'San Francisco', 'State':'CA'}, 
    'KSJU':{'ShortID':'SJU', 'City':'San Juan', 'State':'PR'}, 
    'KSEW':{'ShortID':'SEW', 'City':'Seattle', 'State':'WA'}, 
    'KSHV':{'ShortID':'SHV', 'City':'Shreveport', 'State':'LA'}, 
    'KFSD':{'ShortID':'FSD', 'City':'Sioux Falls', 'State':'SD'}, 
    'KOTX':{'ShortID':'OTX', 'City':'Spokane', 'State':'WA'}, 
    'KSGF':{'ShortID':'SGF', 'City':'Springfield', 'State':'MO'}, 
    'KLSX':{'ShortID':'LSX', 'City':'St. Louis', 'State':'MO'}, 
    'KCTP':{'ShortID':'CTP', 'City':'State College', 'State':'PA'}, 
    'KLWX':{'ShortID':'LWX', 'City':'Sterling', 'State':'VA'}, 
    'KTAE':{'ShortID':'TAE', 'City':'Tallahassee', 'State':'FL'}, 
    'KTBW':{'ShortID':'TBW', 'City':'Tampa Bay Area', 'State':'FL'}, 
    'KTOP':{'ShortID':'TOP', 'City':'Topeka', 'State':'KS'}, 
    'KTWC':{'ShortID':'TWC', 'City':'Tucson', 'State':'AZ'}, 
    'KTSA':{'ShortID':'TSA', 'City':'Tulsa', 'State':'OK'}, 
    'KMPX':{'ShortID':'MPX', 'City':'Twin Cities', 'State':'MN'}, 
    'KAKQ':{'ShortID':'AKQ', 'City':'Wakefield', 'State':'VA'}, 
    'KICT':{'ShortID':'ICT', 'City':'Wichita', 'State':'KS'}, 
    'KILM':{'ShortID':'ILM', 'City':'Wilmington', 'State':'NC'}, 
    'KILN':{'ShortID':'ILN', 'City':'Wilmington', 'State':'OH'}}
    
    return office_ids[cccc]
