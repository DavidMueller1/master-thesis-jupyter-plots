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
def load_data(weeks, unique_id=None, device_types=None, change_types=None):
    """
    Load data from the specified file and filter based on the provided parameters.
    :param weeks: The week numbers
    :param unique_id: Optional unique ID to filter data
    :param device_types: Optional list of device types to filter data. If unique_id is provided, this parameter will be ignored
    :param change_types: Optional list of change types to filter data
    :return: The filtered data
    """
    logger.info(f'Loading data for weeks: {weeks} and device types: {device_types} and unique_id: {unique_id} and change_types: {change_types}')

    data = []
    files = 0

    if unique_id is not None or unique_id != '' or device_types is None or len(device_types) == 0:
        device_types = Device.values()

    logger.info(f'Loading data for device types: {device_types}')

    for week in weeks:
        for device in device_types:
            logger.info(f'Loading data for week {week} and device {device_name_mapping[device]}')
            data_file = f'data/week_{week}/{device_file_mapping[device]}'
            files += 1
            with open(data_file, 'r') as file:
                data.extend(json.load(file))

    logger.info(f'Loaded {len(data)} records from {files} files')


    # Filter data based on unique_id if provided
    if unique_id is not None and unique_id != '':
        data = [item for item in data if item['uniqueId'] == unique_id]

    logger.info(f'Filtered data based on unique_id: {len(data)} records remaining')


    # Filter data based on change_types if provided
    if change_types is not None:
        data = [item for item in data if item['changeType'] in change_types]

    logger.info(f'Filtered data based on change_types: {len(data)} records remaining')


    return data

def load_data_privacy_states(weeks, unique_id=None, device_types=None):
    """
    Load data from the specified file and filter based on the provided parameters.
    :param weeks: The week numbers
    :param unique_id: Optional unique ID to filter data
    :param device_types: Optional list of device types to filter data. If unique_id is provided, this parameter will be ignored
    :return: The filtered data
    """

    change_types = [ChangeType["PRIVACY_STATE_HUB"], ChangeType["PRIVACY_STATE_PROXY"]]

    logger.info(f'Loading data for weeks: {weeks} and device types: {device_types} and unique_id: {unique_id}')

    data = {}
    files = 0

    if unique_id is not None or unique_id != '' or device_types is None or len(device_types) == 0:
        device_types = Device.values()

    logger.info(f'Loading data for device types: {device_types}')

    for week in weeks:
        for device in device_types:
            logger.info(f'Loading data for week {week} and device {device_name_mapping[device]}')
            data_file = f'data/week_{week}/{device_file_mapping[device]}'
            files += 1
            with open(data_file, 'r') as file:
                loaded_data = json.load(file)

                for item in loaded_data:
                    uid = item['uniqueId']
                    if uid not in data:
                        data[uid] = []
                    data[uid].append(item)

    # Go over each entry in data
    for key in data.keys():
        current_device_data = data[key]

        filtered_data = []

        # Filter data based on actual privacy state change
        for index, item in enumerate(current_device_data):
            if index == 0:
                filtered_data.append(item)
            elif item['privacyState'] != current_device_data[index - 1]['privacyState']:
                filtered_data.append(item)

        logger.info(f'Filtered data based on privacy state: {len(filtered_data)} records remaining')

        data[key] = filtered_data

    # logger.info(f'Loaded {len(data)} records from {files} files')


    # Filter data based on unique_id if provided
    # if unique_id is not None and unique_id != '':
    #     data = [item for item in data if item['uniqueId'] == unique_id]

    logger.info(f'Filtered data based on unique_id: {len(data)} records remaining')


    # Filter data based on change_types if provided
    for key in data.keys():
        data[key] = [item for item in data[key] if item['changeType'] in change_types]
    # if change_types is not None:
    #     data = [item for item in data if item['changeType'] in change_types]

    logger.info(f'Filtered data based on change_types: {len(data)} records remaining')

    return_data = []
    for key in data.keys():
        return_data.extend(data[key])


    return return_data
