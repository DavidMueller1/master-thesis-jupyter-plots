import logging
from enum import Enum
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# class Device(Enum):
#     CONTACT_SENSOR = 0
#     PLUG = 1


# class ChangeType(Enum):
#     CONNECTION_STATUS = 0
#     PRIVACY_STATE_HUB = 1
#     PRIVACY_STATE_PROXY = 2
#     DEVICE_EVENT_HUB = 3
#     DEVICE_EVENT_THIRD_PARTY = 4
#     DEVICE_EVENT_DEVICE = 5


Device = {
    "CONTACT_SENSOR": 0,
    "PLUG": 1
}


ChangeType = {
    "CONNECTION_STATUS": 0,
    "PRIVACY_STATE_HUB": 1,
    "PRIVACY_STATE_PROXY": 2,
    "DEVICE_EVENT_HUB": 3,
    "DEVICE_EVENT_THIRD_PARTY": 4,
    "DEVICE_EVENT_DEVICE": 5
}


device_file_mapping = {
    Device["CONTACT_SENSOR"]: 'PrivacyhubDB.contactsensorstates.json',
    Device["PLUG"]: 'PrivacyhubDB.onoffpluginunitstates.json'
}


device_name_mapping = {
    Device["CONTACT_SENSOR"]: 'Contact Sensor',
    Device["PLUG"]: 'Plug'
}


#
def load_data(week, device_type=None, unique_id=None, change_types=None):
    """
    Load data from the specified file and filter based on the provided parameters.
    :param week: The week number
    :param device_type: The device type enum. If None, data from all devices will be loaded
    :param unique_id: Optional unique ID to filter data
    :param change_types: Optional list of change types to filter data
    :return: The filtered data
    """

    data = []

    # Load JSON data from the specified file
    if device_type is None:
        for device in Device:
            data_file = f'data/week_{week}/{device_file_mapping[device]}'
            with open(data_file, 'r') as file:
                data.extend(json.load(file))
    else:
        data_file = f'data/week_{week}/{device_file_mapping[device_type]}'
        with open(data_file, 'r') as file:
            data.extend(json.load(file))

    logger.info(f'Loaded {len(data)} records from "{data_file}"')


    # Filter data based on unique_id if provided
    if unique_id is not None:
        data = [item for item in data if item['uniqueId'] == unique_id]

    logger.info(f'Filtered data based on unique_id: {len(data)} records remaining')


    # Filter data based on change_types if provided
    if change_types is not None:
        data = [item for item in data if item['changeType'] in change_types]

    logger.info(f'Filtered data based on change_types: {len(data)} records remaining')


    return data
