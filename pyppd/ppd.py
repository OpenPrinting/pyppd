import re

class PPD:
    """Represents a PostScript Description file."""
    def __init__(self, ppd_file):
        """Initializes a PPD object with the information at ppd_file string."""
        filename = re.search('PCFileName:\s*"(.+)"', ppd_file)
        language = re.search('LanguageVersion:\s*(.+)', ppd_file)
        manufacturer = re.search('Manufacturer:\s*"(.+)"', ppd_file)
        nickname = re.search('NickName:\s*"(.+)"', ppd_file)
        deviceid = re.search('1284DeviceID:\s*"(.+)"', ppd_file)

        if filename: self.name = "pyppd:" + str.strip(filename.group(1))
        if language: self.language = str.strip(language.group(1))
        if manufacturer: self.manufacturer = str.strip(manufacturer.group(1))
        if nickname: self.nickname = str.strip(nickname.group(1))
        if deviceid: self.deviceid = str.strip(deviceid.group(1))
        self.ppd = ppd_file

    def __str__(self):
        return '"%s" %s "%s" "%s" "%s"' % (self.name, self.language,
                                           self.manufacturer, self.nickname,
                                           self.deviceid)
