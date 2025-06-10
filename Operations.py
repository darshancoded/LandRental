def display_available_lands(lands):
    """
    Displays available lands from the provided list of land dictionaries in a tabular format with a structured box-like structure.
    """
    print("\n    Discover Our Available Lands: A Selection of Exceptional Properties")
    print("                           Available Lands:")
    print("+---------------+----------------+------------+--------------+--------------+")
    print("| Kitta Number  | City           | Direction  | Area (anna)  | Price (NPR)  |")
    print("|---------------|----------------|------------|--------------|--------------|")
    # Iterate through each land dictionary in the list
    for land in lands:
         # Check if the land is available
        if land['availability'] == 'Available':
             # Print land details in tabular format
            print(f"| {land['kitta_number']:13} | {land['city']:14} | {land['direction']:10} | {land['area']:12} | {land['price']:12} |")
    # Print footer for available lands
    print("+---------------+----------------+------------+--------------+--------------+")

def rent_land(lands, kitta_number):
    """
    Handles renting of land and updates land availability status.
    """
    # Iterate through each land dictionary in the list
    for land in lands:
         # Check if the land has the provided kitta number and is available
        if land['kitta_number'] == kitta_number and land['availability'] == 'Available':
             # Change availability status to 'Not Available'
            land['availability'] = 'Not Available'
            # Return the rented land
            return land
    # If land with provided kitta number is not found or is not available, return None
    return None

def display_rented_lands(lands):
    """
    Displays available lands from the provided list of land dictionaries in a tabular format with a structured box-like structure.
    """
    print("\nPresenting Our Rented Lands: Experience the Vibrancy of our Occupied Properties")
    print("                             Rented Lands:")
    print("+---------------+----------------+------------+--------------+--------------+")
    print("| Kitta Number  | City           | Direction  | Area (anna)  | Price (NPR)  |")
    print("|---------------|----------------|------------|--------------|--------------|")
     # Iterate through each land dictionary in the list
    for land in lands:
         # Check if the land is rented
        if land['availability'] == 'Not Available':
            # Print rented land details in tabular format
            print(f"| {land['kitta_number']:13} | {land['city']:14} | {land['direction']:10} | {land['area']:12} | {land['price']:12} |")
     # Print footer for rented lands
    print("+---------------+----------------+------------+--------------+--------------+")

def return_land(lands, kitta_number, exceed_month, duration):
    """
    Handles returning of land and updates land availability status.
    """
    returned_land = None  # Initialize returned_land to None
    kitta_numbers = [land['kitta_number'] for land in lands]  # Extract all kitta numbers from lands
    if kitta_number not in kitta_numbers:
        print(f"Land with kitta number {kitta_number} does not exist.")
        return None
    
    for land in lands:
        if land['kitta_number'] == kitta_number and land['availability'] == 'Not Available':
            fine_amount = 0
            if exceed_month > 0:
                fine_amount = exceed_month * 1000  # Assuming the fine is 1000 NPR per month
                land['fine'] = fine_amount  # Store the fine amount in the land dictionary
                print(f"Fined {fine_amount} NPR for {exceed_month} months of delay.")
            # Calculate the total amount including overdue months and fine
            total_exceeded_amount = land['price'] * duration + fine_amount
            print(f"The total amount is: {total_exceeded_amount} NPR")
            # Update land availability status
            land['availability'] = 'Available'
            returned_land = land  # Store the rented land
            break  # Exit the loop once the land is found
    if returned_land is None:
        print(f"Land with kitta number {kitta_number} is not rented or does not exist.")
    return returned_land





