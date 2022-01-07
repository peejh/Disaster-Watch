import string
import numpy as np
from datetime import datetime


#-------------------------------------------------------------------------------------------------
# Twitter API keys

CONSUMER_KEY        = 'YOUR API CONSUMER KEY'
CONSUMER_SECRET     = 'YOUR API CONSUMER SECRET'
ACCESS_TOKEN        = 'YOUR API ACCESS TOKEN'
ACCESS_TOKEN_SECRET = 'YOUR API ACCESS TOKEN SECRET'

#-------------------------------------------------------------------------------------------------
# Global constants

BRAND_NAME = 'Rumble'

DASHMAIN_REFRESH_RATE = 600             # number of seconds between updates for main data in dashboard_main
DASHMAIN_LIVE_RATE = 10                 # number of seconds between updates for live components

DASHMAIN_MAP_DEFAULT_LOC = 257924275    # nomin_id of default location, if specified

DASHMAIN_MAP_DEFAULT_LAT = 23           # latitude for center of world map
DASHMAIN_MAP_DEFAULT_LON = 11           # longitude for center of world map
DASHMAIN_MAP_DEFAULT_ZOOM = 0.87        # default zoom for 1920x1080 screen
DASHMAIN_MAP_MARKER_COLORS = {
    'danger'    :'#D9534F',
    'secondary' :'#6C757D',
    'warning'   :'#F0AD4E',
    'info'      :'#5BC0DE',
    'success'   :'#5CB85C',
    'primary'   :'#0275D8'
}                                       # hex codes to categorize tweets by their confidence scores
DASHMAIN_TWEETS_MIN_CONF = 0.5          # default min confidence for selected tweets in main page

LIVEFEED_REFRESH_RATE = 600             # number of seconds between auto-refresh in livefeed

# Filler content
LOREM_IPSUM = '''
Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor 
incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud 
exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute 
irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla 
pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia 
deserunt mollit anim id est laborum.
'''

# Recommended Crisis Lexicon: https://crisislex.org/crisis-lexicon.html + additions
# ~450 keywords is too much for the streamer
CRISIS_LEXICON = [
    'accepting financial','accident','affected','affected areas','affected explosion','affected flooding',
    'affected hurricane','affected tornado','aftermath','alive','alive rubble','amazing rescue','another explosion',
    'appeal launched','arrest','assist people','attack','authorities','blast','blizzard','bodies recovered',
    'bomb','bomber','bombing','bombing case','bombing investigation','bombing shot','bombing suspect',
    'bombing victims','bombing witnesses','bombings reports','bombings saddened','braces','braces major',
    'braces river','breaking arrest','breaking enforcement','breaking news','breaking suspect','brought hurricane',
    'buried','buried alive','bushfire','casualties','catastrophe','city tornado','cleanup','climate change',
    'coast hurricane','collapse','collision','communities damaged','confirmed dead','cost deaths','counts flood',
    'crash','criminal','crisis','crisis deepens','crisis found','crisis rises','crisis unfolds','crisis worsens',
    'cross tornado','cyclone','damage','damaged','damaged hurricane','daring rescue','dead','dead explosion',
    'dead floods','dead hundreds','dead injured','dead missing','dead torrential','deadly','deadly explosion',
    'deadly tornado','dealing hurricane','death','death toll','deaths confirmed','debris','deepens death','destroyed',
    'destruction','devastating','devastating tornado','devastation','died','died explosions','disaster',
    'disaster relief','disasters txting','displaced','donate','donate cross','donate tornado','donated million',
    'donated victims','donation','donation help','donations assist','dozens','dramatic','drought','dying',
    'dying hurricane','earthquake','effected hurricane','emergency','enforcement','enforcement official',
    'entire crowd','epidemic','eruption','evacuate','evacuated','evacuation','evacuees','even scary','events',
    'explosion','explosion caught','explosion fertiliser','explosion fire','explosion injured','explosion registered',
    'explosion reported','explosion ripped','explosion victims','explosion video','explosion voted','explosions running',
    'facing flood','famine','fatal','fatalities','feared dead','fertilizer explosion','financial donations','fire',
    'fire explosion','fire fighters','fire flood','firefighters','firefighters police','first responders','flash flood',
    'flood','flood affected','flood alerts','flood appeal','flood claims','flood cost','flood crisis','flood damage',
    'flood death','flood disaster','flood emergency','flood hits','flood homeowners','flood levy','flood peak',
    'flood powerful','flood ravaged','flood recovery','flood relief','flood situation','flood threat','flood toll',
    'flood tornado','flood victims','flood warnings','flood waters','flood worsens','flood years','floods force',
    'floods kill','floodwaters','following explosion','footage','forestfire','free hotline','gets donated','girl died',
    'give online','government negligent','hail','hailstorm','hazard','heart prayers','heart praying','heat wave',
    'help affected','help flood','help rebuilt','help text','help tornado','help victims','high river','hijack',
    'hoisted flood','homeowners reconnect','homes inundated','hostage','hotline','hotline help','house flood',
    'huge explosion','hundreds homes','hundreds injured','hurricane','hurricane black','hurricane category',
    'hurricane coming','identified suspect','imminent','impacted','injured','injured explosion','injuries',
    'injuries reported','inundated','investigation','join praying','killed','killed injured','killed people',
    'killed police','killing','kills forces','landfall','landslide','large explosion','lava','leave town','levy',
    'life heart','live coverage','lives hurricane','loss','loss life','lost legs','lost lives','love prayers',
    'lurches fire','magnitude','major explosion','major flood','make donation','marathon explosions','mass shooting',
    'massacre','massive','massive explosion','massive manhunt','massive tornado','medical examiner','medical office',
    'memorial service','military','missing','missing explosion','missing flood','morning flood','murder',
    'name hurricane','names terrified','natural disaster','naturaldisaster','need terrifying','news flood',
    'nuclear meltdown','nursing','oil spill','opposed flood','outbreak','pandemic','path hurricane','peaks deaths',
    'people dead','people died','people injured','people killed','people trapped','photos flood','please join',
    'please stay','police','police officer','police people','police suspect','power supplies','powerful storms',
    'prayers','prayers affected','prayers city','prayers families','prayers involved','prayers people','prayers tonight',
    'prayers victims','praying','praying affected','praying community','praying families','praying victims',
    'prepare hurricane','public safety','rains severely','ravaged','rebuild','rebuilt','rebuilt communities','recede',
    'reconnect power','recover','redcross','redcross donate','redcross give','reels surging','refugee',
    'registered magnitude','release toxins','releases images','releases photos','relief','relief efforts',
    'relief fund','remember lives','reported dead','reported explosion','reported injured','reportedly dead','rescue',
    'rescue teenager','rescue women','rescuers','rescuers help','residents','responders','responders killed',
    'response disasters','return home','retweet donate','risk running','river peaks','robbery','rubble',
    'run massive','saddened','saddened loss','safe hurricane','safety','sandstorm','saying hurricane','seconds bombing',
    'seismic','send prayers','severe flooding','shocking video','shot killed','sinkhole','snowstorm','soldier',
    'someone captured','stay strong','storm','storms amazing','stream','structural failure','suicide bomb',
    'supplies waters','surging floods','surviving','survivor','survivor finds','suspect','suspect bombing',
    'suspect dead','suspect killed','suspect pinned','suspect run','teenager floods','terrible explosion',
    'terrified hurricane','terrifying','terror','terror attack','terrorist','text donation','text redcross',
    'thoughts prayers','thoughts victims','thousands homes','thunderstorm','time hurricane','toll','toll rises',
    'tornado','tornado damage','tornado disaster','tornado flood','tornado relief','tornado survivor','tornado victims',
    'torrential','torrential rains','toxins','toxins flood','tragedy','tragic','tragic events','trapped','troops',
    'troops lend','tsunami','twister','txting redcross','typhoon','unaccounted','unknown number','unknown soldier',
    'victim','victims','victims donate','victims explosion','victims lost','victims waters','video capturing',
    'video explosion','visiting flood','volunteer','volunteers','waiting hurricane','want help','warning',
    'watch hurricane','water rises','waters recede','wildfire','windstorm','witness','worsens eastern','wounded',
    'wreck'
]

# curated keyword list to cover more topics (77 so far)
TOP100_LEXICON = [
    'accident','attack','blizzard','bombing','bushfire','casualties','catastrophe','collapse','collision','crash',
    'criminal','cyclone','dead','death','debris','derail','destruction','devastation','disaster','drought',
    'earthquake','emergency','epidemic','eruption','evacuate','evacuation','explosion','famine','fatal','fire',
    'first responders','flood','forestfire','hail','hailstorm','hazard','heat wave','hijack','hostage','hurricane',
    'injured','killed','killing','landslide','lava','lightning','mass shooting','massacre','meltdown','murder',
    'naturaldisaster','oil spill','outbreak','pandemic','refugee','rescue','robbery','sandstorm','sinkhole',
    'snowstorm','storm','structural failure','suicide bomb','survivor','terrorist','thunderstorm','tornado',
    'tsunami','twister','typhoon','volcano','war zone','whirlwind','wildfire','windstorm','wounded','wreck'    
]

# just major events
MAJOR_EVENTS_LEXICON = [
    'storm','earthquake','landslide','typhoon','hurricane','cyclone','flood','tsunami','volcano',
    'volcanic eruption','seismic activity','drought','blizzard','lightning','disaster','naturaldisaster'
]

# minimal keyword list for use during development
SIMPLE_LEXICON = ['naturaldisaster','storm','typhoon','earthquake','tsunami','volcano']

#-------------------------------------------------------------------------------------------------
# Utility methods

def create_markdown_link(url):
    return '[view](' + url + ')'

def extract_time_from_datetime(date):
    return str(date)

def extract_engagement_total(df):
    return df.loc[:,['reply_count', 'retweet_count', 'favorite_count']].sum(axis=1)

def extract_best_location(df):
    best_location_long = np.array([user_lon if np.isnan(lon) else lon 
                                   for lon, user_lon in zip(df.coordinates_long, df.user_coords_long)])
    best_location_lat = np.array([user_lat if np.isnan(lat) else lat 
                                  for lat, user_lat in zip(df.coordinates_lat, df.user_coords_lat)])

    return best_location_long, best_location_lat

def extract_tooltip_text(data):
    if not np.isnan(data['best_loc_lon']):
        tt_screen_name = '<b><i>@' + data['user_screen_name'] + '</i></b><br>'
        tt_prob = '<i>Confidence: <b>' + str(data['prob']) + '%</b></i>'

        wordlist = data['text'].split()
        lines = []
        line = ''
        for word in wordlist:
            line += word + ' '
            if len(line) > 60:
                line.strip()
                lines.append(line)
                line = ''
        lines.append(line)

        tt_text = '<br>'.join(lines) + '<br>'

        return tt_screen_name + tt_text + tt_prob + '<extra></extra>'
    else:
        return None

def get_pretty_int(num):
    return f'{num:,}'

def get_pretty_count(count):
    suffix = ['','K','M','B']
    n = 0
    while count / 1000 > 1:
        count /= 1000
        n += 1
    # count = '{:.1f}'.format(count) # use this for proper rounding
    count = int(count * 10) / 10 # use this for no rounding
    count_str = str(count)[:-len('.0')] if str(count).endswith('.0') else str(count)
    return count_str + suffix[n]

def get_pretty_timedelta(time_diff):
    days = time_diff.days
    
    if days > 0:
        if days >= 365:
            yrs, days = divmod(days, 365)
            return str(yrs) + ' year' + ('s' if yrs > 1 else '') + ' ago'
        elif days >= 30:
            mnts, days = divmod(days, 30)
            return str(mnts) + ' month' + ('s' if mnts > 1 else '') + ' ago'
        elif days >= 7:
            wks, days = divmod(days, 7)
            return str(wks) + ' week' + ('s' if wks > 1 else '') + ' ago'
        else:
            return str(days) + ' day' + ('s' if days > 1 else '') + ' ago'
    else:
        secs = time_diff.seconds
        hrs, secs = divmod(secs, 3600)
        mins, secs = divmod(secs, 60)

        if hrs > 0:
            return str(hrs) + ' hour' + ('s' if hrs > 1 else '') + ' ago'
        elif mins > 0:
            return str(mins) + ' minute' + ('s' if mins > 1 else '') + ' ago'
        elif secs > 0:
            return str(secs) + ' second' + ('s' if secs > 1 else '') + ' ago'
        else:
            return 'Just now'

def get_prob_class(prob):
    classes = ['danger','secondary','warning','info','success','primary','primary']
    prob -= 40
    prob = 0 if prob < 0 else prob
    return classes[int(prob / 10)]

def get_timeframe(index):
    # mins, hours, days
    choices = [
        [1,0,0],
        [5,0,0],
        [30,0,0],
        [0,1,0],
        [0,6,0],
        [0,12,0],
        [0,0,1],
        [0,0,3],
        [0,0,7]
    ]
    return choices[index]

def get_bbox(df, loc_id):
    lat_min = df.loc[df.nomin_id == loc_id,'bb_min_lat'].array[0]
    lat_max = df.loc[df.nomin_id == loc_id,'bb_max_lat'].array[0]
    lon_min = df.loc[df.nomin_id == loc_id,'bb_min_lon'].array[0]
    lon_max = df.loc[df.nomin_id == loc_id,'bb_max_lon'].array[0]
    return (lat_min, lat_max), (lon_min, lon_max)

def is_within_boundingBox(lat, lon, latitudes, longitudes):
    lat_min, lat_max = latitudes
    lon_min, lon_max = longitudes
    if lat < lat_min or lat > lat_max or lon < lon_min or lon > lon_max:
        return False
    return True