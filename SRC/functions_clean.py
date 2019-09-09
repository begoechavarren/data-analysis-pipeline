import re


def state_fixer(text):
    ''' fixes the column 'state' by including the state name
    instead of its abbreviation'''
    states = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AS': 'American Samoa',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'GU': 'Guam',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MP': 'Northern Mariana Islands',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NA': 'National',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'PR': 'Puerto Rico',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VI': 'Virgin Islands',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'}
    return states[text]


def category_fixer(text):
    if re.search('[Mm]exican|[Tt]aco', text):
        return 'mexican'
    if re.search('[Ss]andwich', text):
        return 'sandwich'
    if re.search('[Pp]izza|[Ii]talian', text):
        return 'italian'
    if re.search('[Cc]hicken', text):
        return 'chicken'
    if re.search('[Ff]ish', text):
        return 'fish'
    if re.search('[Aa]sian|[Ss]ushi', text):
        return 'asian'
    if re.search('[Bb]urger', text):
        return 'burger'
    if re.search('[Ii]ce [Cc]ream', text):
        return 'ice cream'
    if re.search('[Mm]editerranean', text):
        return 'mediterranean'
    if re.search('[Bb]akery|[Bb]reakfast', text):
        return 'bakery'
    if re.search('[Mm]iddle [Ee]ast', text):
        return 'middle east'
    if re.search('[Hh]ot [Dd]og', text):
        return 'hot dog'
    if re.search('[Ff]ast [Ff]ood|[Aa]merican', text):
        return 'american fast food'
