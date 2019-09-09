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
    ''' fixes the column 'category' by further grouping in 
    a few categories'''
    categories = {'[Mm]exican|[Tt]aco': 'mexican', '[Ss]andwich': 'sandwich', '[Pp]izza|[Ii]talian': 'italian', '[Cc]hicken': 'chicken', '[Ff]ish': 'fish', '[Aa]sian|[Ss]ushi': 'asian', '[Bb]urger': 'burger',
                  '[Ii]ce [Cc]ream': 'ice cream', '[Mm]editerranean': 'mediterranean', '[Bb]akery|[Bb]reakfast': 'bakery', '[Mm]iddle [Ee]ast': 'middle east', '[Hh]ot [Dd]og': 'hot dog', '[Ff]ast [Ff]ood|[Aa]merican': 'american fast food'}
    for cat in categories:
        if re.search(cat, text):
            return categories[cat]
