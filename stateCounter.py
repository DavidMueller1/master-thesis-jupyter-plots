import json


def load_json(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
    return data

def count_privacy_state_changes(data):
    # Dictionary to store the count of privacy state changes for each uniqueId
    privacy_state_changes = {}

    for record in data:
        unique_id = record["uniqueId"]
        privacy_state = record["privacyState"]

        # Initialize the dictionary entry if not present
        if unique_id not in privacy_state_changes:
            privacy_state_changes[unique_id] = {
                "last_privacy_state": privacy_state,
                "change_count": 0
            }
        else:
            # Check if the privacyState has changed compared to the last recorded state
            if privacy_state_changes[unique_id]["last_privacy_state"] != privacy_state:
                privacy_state_changes[unique_id]["change_count"] += 1
                privacy_state_changes[unique_id]["last_privacy_state"] = privacy_state

    # Extract only the change counts for the final output
    change_counts = {unique_id: info["change_count"] for unique_id, info in privacy_state_changes.items()}

    return change_counts

# Load the JSON data from the file
data = load_json('data/week_4/PrivacyhubDB.onoffpluginunitstates.json')

# Run the function with the loaded data
change_counts = count_privacy_state_changes(data)
print(change_counts)
