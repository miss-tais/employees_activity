class ConfigFileNotFound(Exception):
    """Raise exception when configuration file not found"""


class ConfigFileError(Exception):
    """Raise exception when configuration file contains errors"""


class ConfigFileMissingAttribute(Exception):
    """Raise exception when specified attribute is missing in configuration file"""


class HubstaffAuthenticationError(Exception):
    """Raise exception when Hubstaff authentication failed"""


class HubstaffAPIError(Exception):
    """Raise exception when Hubstaff api request failed"""
