import json

# Initialize an empty dictionary
user_dict = {}

# Prompt the user for input
num_entries = int(input("How many key-value pairs do you want to enter? "))

# Loop to input keys and values
for i in range(num_entries):
    key = input("Enter key {}: ".format(i + 1))
    value = input("Enter value for {}: ".format(key))
    
    # Add key-value pair to dictionary
    user_dict[key] = value

# Print the dictionary
print("User dictionary:", user_dict)

# Write dictionary to JSON file
json_file_name = input("Enter the name of the JSON file to save the dictionary: ")

with open(json_file_name, 'w') as json_file:
    json.dump(user_dict, json_file)

print("Dictionary saved to", json_file_name)
