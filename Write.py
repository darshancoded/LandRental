def write_land_data(file_name, land_data):
    """
    Writes land data to a text file from the provided list of land dictionaries.
    """
    # Open the file in write mode
    with open(file_name, 'w') as file:
         # Iterate through each land dictionary in the list
        for land in land_data:
            # Write land information to the file
            file.write(f"{land['kitta_number']}, {land['city']}, {land['direction']}, {land['area']}, {land['price']}, {land['availability']}\n")
