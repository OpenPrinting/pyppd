import re

LANGUAGES = {'afar': 'aa', 'abkhazian': 'ab', 'afrikaans': 'af',
             'amharic': 'am', 'arabic': 'ar', 'assamese': 'as', 
             'aymara': 'ay', 'azerbaijani': 'az', 'bashkir': 'ba', 
             'byelorussian': 'be', 'bulgarian': 'bg', 'bihari': 'bh', 
             'bislama': 'bi', 'bengali': 'bn', 'bangla': 'bn', 
             'tibetan': 'bo', 'breton': 'br', 'catalan': 'ca', 
             'corsican': 'co', 'czech': 'cs', 'welsh': 'cy', 
             'danish': 'da', 'german': 'de', 'bhutani': 'dz', 
             'greek': 'el', 'english': 'en', 'esperanto': 'eo', 
             'spanish': 'es', 'estonian': 'et', 'basque': 'eu', 
             'persian': 'fa', 'finnish': 'fi', 'fiji': 'fj', 
             'faeroese': 'fo', 'french': 'fr', 'frisian': 'fy', 
             'irish': 'ga', 'scots gaelic': 'gd', 'galician': 'gl', 
             'guarani': 'gn', 'gujarati': 'gu', 'hausa': 'ha', 
             'hindi': 'hi', 'croatian': 'hr', 'hungarian': 'hu', 
             'armenian': 'hy', 'interlingua': 'ia', 'interlingue': 'ie', 
             'inupiak': 'ik', 'indonesian': 'in', 'icelandic': 'is', 
             'italian': 'it', 'hebrew': 'iw', 'japanese': 'ja', 
             'yiddish': 'ji', 'javanese': 'jw', 'georgian': 'ka', 
             'kazakh': 'kk', 'greenlandic': 'kl', 'cambodian': 'km', 
             'kannada': 'kn', 'korean': 'ko', 'kashmiri': 'ks', 
             'kurdish': 'ku', 'kirghiz': 'ky', 'latin': 'la', 
             'lingala': 'ln', 'laothian': 'lo', 'lithuanian': 'lt', 
             'latvian': 'lv','lettish': 'lv', 'malagasy': 'mg', 
             'maori': 'mi', 'macedonian': 'mk', 'malayalam': 'ml', 
             'mongolian': 'mn', 'moldavian': 'mo', 'marathi': 'mr', 
             'malay': 'ms', 'maltese': 'mt', 'burmese': 'my', 
             'nauru': 'na', 'nepali': 'ne', 'dutch': 'nl', 
             'norwegian': 'no', 'occitan': 'oc', '(afan) oromo': 'om', 
             'oriya': 'or', 'punjabi': 'pa', 'polish': 'pl', 
             'pashto': 'ps', 'pushto': 'ps', 'portuguese': 'pt', 
             'quechua': 'qu', 'rhaeto-romance': 'rm', 'kirundi': 'rn', 
             'romanian': 'ro', 'russian': 'ru', 'kinyarwanda': 'rw', 
             'sanskrit': 'sa', 'sindhi': 'sd', 'sangro': 'sg', 
             'serbo-croatian': 'sh', 'singhalese': 'si', 'slovak': 'sk', 
             'slovenian': 'sl', 'samoan': 'sm', 'shona': 'sn', 
             'somali': 'so', 'albanian': 'sq', 'serbian': 'sr', 
             'siswati': 'ss', 'sesotho': 'st', 'sundanese': 'su', 
             'swedish': 'sv', 'swahili': 'sw', 'tamil': 'ta', 
             'tegulu': 'te', 'tajik': 'tg', 'thai': 'th', 
             'tigrinya': 'ti', 'turkmen': 'tk', 'tagalog': 'tl', 
             'setswana': 'tn', 'tonga': 'to', 'turkish': 'tr', 
             'tsonga': 'ts', 'tatar': 'tt', 'twi': 'tw', 
             'ukrainian': 'uk', 'urdu': 'ur', 'uzbek': 'uz', 
             'vietnamese': 'vi', 'volapuk': 'vo', 'wolof': 'wo', 
             'xhosa': 'xh', 'yoruba': 'yo', 'chinese': 'zh', 
             'simplified chinese': 'zh_TW', 'traditional chinese': 'zh_CN',
             'zulu': 'zu', 'portuguese_brazil': 'pt_BR'}

class PPD(object):
    """Represents a PostScript Description file."""
    def __init__(self, filename, language, manufacturer, nickname, deviceid):
        """Initializes a PPD object with the information passed."""
        self.filename = filename
        self.language = language
        self.manufacturer = manufacturer
        self.nickname = nickname
        self.deviceid = deviceid

    def __str__(self):
        return '"%s" %s "%s" "%s" "%s"' % (self.filename, self.language,
                                           self.manufacturer, self.nickname,
                                           self.deviceid)


def parse(ppd_file, filename):
    """Parses ppd_file and returns an array with the PPDs it found.

    One ppd_file might result in more than one PPD. The rules are: if the file
    has an "1284DeviceID" entry, returns only one PPD with it. If not, returns
    one PPD for each "Product" entry, generating the deviceids as
    "MFG:<manufacturer>;MDL:<product>".
    """
    language_re     = re.search('LanguageVersion:\s*(.+)', ppd_file)
    manufacturer_re = re.search('Manufacturer:\s*"(.+)"', ppd_file)
    nickname_re     = re.search('NickName:\s*"(.+)"', ppd_file)
    deviceid_re     = re.search('1284DeviceID:\s*"(.+)"', ppd_file)

    try:
        language = LANGUAGES[str.strip(language_re.group(1)).lower()]
        manufacturer = str.strip(manufacturer_re.group(1))
        nickname = str.strip(nickname_re.group(1))
        if deviceid_re:
            deviceid = str.strip(deviceid_re.group(1))
            return [PPD(filename, language, manufacturer, nickname, deviceid)]
        else:
            ppds = []
            for product in re.findall('Product:\s*"\((.+)\)"', ppd_file):
                product = str.strip(product)
                deviceid = "MFG:%s;MDL:%s;" % (manufacturer, product)
                ppds += [PPD(filename, language, manufacturer, nickname, deviceid)]

            return ppds
    except:
        raise Exception, ("Error parsing PPD file '%s'" % filename)
