import logging
from enum import Enum
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

# List of uniqueIds of devices that have been used in study in each week (manually checked)
ids_of_relevant_devices = {
    1: [
        '13E56C4E1FD98745',
        '39C0AE0A9852E5EE',
    ],
    2: [
        'F7D9D208C65ADE9B',
        'B1844314D756D84B',
        'BEC8B63351AC02EC',
    ],
    3: [
        '29E2D375B84AE67A',
        '04D7DC521AF6EC84',
        '6E628ADD7E9FB178',
    ],
    4: [
        '29E2D375B84AE67A',
        '6E628ADD7E9FB178',
        '04D7DC521AF6EC84',
    ]
}

def fancy_load_base_data(
        weeks: list[int],
):
    output_data = {}
    files = 0

    for week in weeks:
        grouped_data = {}
        for device in Device.values():
            data_file = f'data/week_{week}/{device_file_mapping[device]}'
            logger.info(f'Loading data from {data_file}')
            files += 1
            with open(data_file, 'r') as file:
                loaded_data = json.load(file)

                # Group data by uniqueId and filter out irrelevant devices
                for item in loaded_data:
                    if item['uniqueId'] in ids_of_relevant_devices[week]:
                        if item['uniqueId'] not in grouped_data:
                            grouped_data[item['uniqueId']] = []
                        grouped_data[item['uniqueId']].append(item)
        output_data[week] = grouped_data

    return output_data

def fancy_load_data_change_types(
        weeks: list[int],
):
    data = fancy_load_base_data(weeks)

    change_types = [ChangeType["PRIVACY_STATE_HUB"], ChangeType["PRIVACY_STATE_PROXY"]]

    # Filter out non-actual privacy state changes
    for week, week_data in data.items():
        for unique_id, device_data in week_data.items():
            filtered_data = []
            for index, item in enumerate(device_data):
                if index == 0:
                    filtered_data.append(item)
                elif item['privacyState'] != device_data[index - 1]['privacyState']:
                    filtered_data.append(item)
            logger.info(f'Filtered data of {unique_id} based on actual privacy state: before={len(device_data)}, after={len(filtered_data)}')
            data[week][unique_id] = filtered_data

    # Filter out change types
    for week, week_data in data.items():
        for unique_id, device_data in week_data.items():
            before = len(device_data)
            data[week][unique_id] = [item for item in device_data if item['changeType'] in change_types]
            logger.info(f'Filtered data of {unique_id} based on change types: before={before}, after={len(data[week][unique_id])}')

    return data