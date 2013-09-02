import re
import logging

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
    def __init__(self, uri, language, manufacturer, nickname, deviceid):
        """Initializes a PPD object with the information passed."""
        self.uri = uri
        self.language = language
        self.manufacturer = manufacturer
        self.nickname = nickname
        self.deviceid = deviceid

    def __str__(self):
        return '"%s" %s "%s" "%s" "%s"' % (self.uri, self.language,
                                           self.manufacturer, self.nickname,
                                           self.deviceid)


def parse(ppd_file, filename):
    """Parses ppd_file and returns an array with the PPDs it found.

    One ppd_file might result in more than one PPD. The rules are: return an
    PPD for each "1284DeviceID" entry, and one for each "Product" line, if it
    creates an unique (Manufacturer, Product) DeviceID.
    """

    def standardize(model_name):
        # Consider it the same model if the product name differs only by
        # upper/lower case and by the presence/absence of the manufacturer
        # name
        return model_name.lower().replace("Hewlett-Packard ".lower(), "").replace("%s " % manufacturer.lower(), "").strip()

    logging.debug('Parsing %s.' % filename)
    language_re     = re.search(b'\*LanguageVersion:\s*(.+)', ppd_file)
    manufacturer_re = re.search(b'\*Manufacturer:\s*"(.+)"', ppd_file)
    nickname_re     = re.search(b'\*NickName:\s*"(.+)"', ppd_file)
    deviceids       = re.findall(b'\*1284DeviceID:\s*"(.+)"', ppd_file)

    try:
        language = LANGUAGES[language_re.group(1).decode('UTF-8', errors='replace').strip().lower()]
        manufacturer = manufacturer_re.group(1).strip().decode('UTF-8', errors='replace')
        nickname = nickname_re.group(1).strip().decode('UTF-8', errors='replace')
        logging.debug('Language: "%s", Manufacturer: "%s", Nickname: "%s".' %
                      (language, manufacturer, nickname))
        ppds = []
        models = []
        drventry = None
        line = 0
        num_device_ids = 0
        num_products = 0
        if deviceids:
            for deviceid in deviceids:
                deviceid = deviceid.decode('UTF-8', errors='replace')
                logging.debug('1284DeviceID: "%s".' % deviceid)
                if (not deviceid.endswith(";")):
                    deviceid += ";"
                uri = "%d/%s" % (line, filename)
                # Save a DRV field (from Foomatic) and use it for all entries
                # of this PPD
                newdrventry = re.findall(".*DRV:\s*(.*?)\s*;.*", deviceid, re.I)
                if (len(newdrventry) > 0):
                    drventry = newdrventry[0]
                elif (drventry != None):
                    deviceid += "DRV:%s;" % drventry
                newmodels = re.findall(".*(?:MODEL|MDL):\s*(.*?)\s*;.*", deviceid, re.I)
                if (newmodels):
                    newmodels = list(map(standardize, newmodels))
                if (len(newmodels) > 0):
                    # Consider only IDs with a MODEL/MDL field
                    ppds += [PPD(uri, language, manufacturer, nickname, deviceid.strip())]
                    models += newmodels
                    num_device_ids += 1
                    line += 1

        for product in re.findall(b'\*Product:\s*"\(\s*(.+?)\s*\)"', ppd_file):
            product = product.strip().decode('UTF-8', errors='replace')

            # Don't add a new entry if there's already one for the same
            # product/model
            product_standardized = standardize(product)
            if product_standardized in models:
                logging.debug('Ignoring already found *Product: "%s".' %
                              product)
                continue

            logging.debug('Product: "%s"' % product)
            deviceid = "MFG:%s;MDL:%s;" % (manufacturer, product)
            if (drventry != None):
                deviceid += "DRV:%s;" % drventry
            uri = "%d/%s" % (line, filename)
            ppds += [PPD(uri, language, manufacturer, nickname, deviceid)]
            num_products += 1
            line += 1
            models += [product_standardized]

        if (num_products == 1 and num_device_ids > 0):
            # If there is at least one device ID and only one Product line, do
            # not consider the Product line as another model than the one
            # represented by the device ID and use only the data of the device
            # ID.
            ppds.pop()

        return ppds
    except:
        raise Exception("Error parsing PPD file '%s'" % filename)
