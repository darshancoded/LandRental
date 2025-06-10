def read_land_data(file_name):
    """
    Reads land data from a text file and returns a list of dictionaries
    containing land information.
    """
    # Initialize an empty list to store land data
    land_data = []
    # Open the file in read mode
    with open(file_name, 'r') as file:
         # Iterate through each line in the file
        for line in file:
            # Remove leading/trailing spaces and split the line by comma and space
            land_info = line.strip().split(', ')
            # Create a dictionary for each land entry and append it to land_data list
            land_data.append({
                'kitta_number': int(land_info[0]), # Convert kitta_number to integer
                'city': land_info[1],# City name
                'direction': land_info[2],# Direction (i.e North, South)
                'area': int(land_info[3]), # Convert area to integer
                'price': int(land_info[4]),# Convert price to integer
                'availability': land_info[5]  # Availability status
            })
    # Return the list of dictionaries containing land information
    return land_data