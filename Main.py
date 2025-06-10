# Import necessary functions from other files
from Read import read_land_data
from Write import write_land_data
from Operations import display_available_lands, display_rented_lands, rent_land, return_land

def generate_invoice(lands, customer_name, transaction_type, duration=None, exceed_month=None, fine_amount=0):
    """
    Generates an invoice for the transaction.
    """
    total_amount = 0
    invoice = "                        ==============================\n"
    invoice += "                                   INVOICE\n"
    invoice += "                        ==============================\n"
    invoice += f"                              Customer: {customer_name}\n"
    invoice += "                        -------------------------------\n"
    
    # Add transaction type to the invoice
    invoice += f"                           Transaction Type: {transaction_type}\n"
    invoice += f"                             Duration: {duration} months\n"
    if transaction_type == "Return":
        invoice += f"                             Exceeded Months: {exceed_month} months\n"
        invoice += f"                           Fine Amount: {fine_amount} NPR\n"
    
    # Add header for land details table
    invoice += "\n                               Land Details:\n"
    invoice += "+--------------+----------------+------------+--------------+--------------+\n"
    invoice += "| Kitta Number | City/District  | Direction  | Area (anna)  | Price (NPR)  |\n"
    invoice += "+--------------+----------------+------------+--------------+--------------+\n"
    
    # Ensure duration and exceed_month have valid integer values
    if duration is None:
        duration = 0
    if exceed_month is None:
        exceed_month = 0
    
    # Loop through each rented land to create land details table
    for land in lands:
        original_price = land['price']  # Preserve the original price
        if transaction_type == "Rent":
            # Calculate the total price based on the duration of the rental
            land_price = original_price * duration
        else:
            # Calculate the total price including any additional charges for exceeding the rental duration
            land_price = (original_price * duration) + (original_price * exceed_month) + fine_amount
        invoice += "| {:<12} | {:<14} | {:<10} | {:<12} | {:<12} |\n".format(land['kitta_number'], land['city'], land['direction'], land['area'], original_price)
        total_amount += land_price  # Add the price of each rented land to the total amount
    
    # Add footer for land details table
    invoice += "+--------------+----------------+------------+--------------+--------------+\n"
    
    # Add total amount to the invoice
    invoice += "                       ==============================\n"
    invoice += f"                           Total Amount: {total_amount} NPR\n"
    invoice += "                       ==============================\n"

    return invoice

# Define a function to write the invoice to a file
def write_invoice_to_file(invoice, customer_name):
    """
    Writes the invoice to a new text file.
    """
    try:
        # Read the count of existing invoices from a file, or set it to 0 if the file doesn't exist
        with open("invoice_count.txt", "r") as count_file:
            count = int(count_file.read().strip())
    except FileNotFoundError:
        count = 0
    
    # Increment the count for the new invoice file
    count += 1
    file_name = f"{customer_name}_invoice_{count}.txt"
    # Write the invoice content to the new file
    with open(file_name, "w") as file:
        file.write(invoice)
    
    # Update the count file with the new count
    with open("invoice_count.txt", "w") as count_file:
        count_file.write(str(count))
    
    print(f"Invoice saved to {file_name}")

# Define the main function to interact with the land rental system
def main():
    lands = read_land_data("C:\\Users\\himan\\OneDrive - London Metropolitan University\\Python\\Coursework\\land_data.txt")
    
    # Main loop for interacting with the land rental system
    while True:
        print("\n                     Namaste!!")
        print("\nWe Techno Property Nepal Welcome you to our Land Rental System")
        print("               1. Discover Available Lands")
        print("               2. Secure your Land")
        print("               3. Explore Rented Lands")
        print("               4. Release Your Land")
        print("               5. Happy Departure")
        
        # Take user input for action selection
        choice = input("   Kindly choice the service you want experience: ")
        print("=============================================================================================")
        # Execute corresponding actions based on user input
        if choice == '1':
            display_available_lands(lands)
            print("=============================================================================================")
        elif choice == '2':
            try:
                kitta_numbers = input("Please input the kitta numbers of the lands you wish to rent, separating each with a comma: ")
                if any(int(k) < 0 for k in kitta_numbers.split(',')):
                    print("Could you please enter positive values for kitta numbers.")
                    continue
                kitta_numbers = [int(k) for k in kitta_numbers.split(',')]
                rented_lands = []
                
                # Attempt to rent each requested land
                for kitta_number in kitta_numbers:
                    land = rent_land(lands, kitta_number)
                    if land:
                        rented_lands.append(land)
                    else:
                        print(f"Land with kitta number {kitta_number} is not available for rent.")
                        # If any land is not available, cancel the transaction for all lands
                        rented_lands = []
                        break
                
                # If all lands are available, proceed with the rental transaction
                if rented_lands:
                    try:
                        customer_name = input("Can you share us your good name: ")
                        duration = int(input("For how long would you like to rent thins land (in months): "))
                        invoice = generate_invoice(rented_lands, customer_name, "Rent", duration)
                        write_invoice_to_file(invoice, customer_name)
                        print("Congratulations!! You have successfully Rented this land")
                        write_land_data("C:\\Users\\himan\\OneDrive - London Metropolitan University\\Python\\Coursework\\land_data.txt", lands)
                        print(invoice)
                    except ValueError:
                        print("Oopsss!! You entered an Invalid input!")
            except ValueError:
                print("Oopsss!! Invalid input! Please enter valid kitta numbers separated by commas.")
        elif choice == '3':
            display_rented_lands(lands)
            print("=============================================================================================")
        elif choice == '4':
            try:
                kitta_number = int(input("Please input the kitta numbers of the lands you wish to return: "))
                duration = int(input("For how many months did you rent the land? : "))  # Get the rented duration
                # Check if the entered value is negative
                if kitta_number < 0:
                    print("Oopsss!! Invalid input! Please enter a positive value for the kitta number.")
                    continue
                exceed_month = int(input("Please input the number of months by which you have exceeded the rental period: "))
                # Check if the entered value is negative
                if exceed_month < 0:
                    print("Oopsss!! Invalid input! Please enter a positive value for the number of months exceeded.")
                    continue
                returned_land = return_land(lands, kitta_number, exceed_month, duration)
                if returned_land is not None:
                    if 'fine' in returned_land and returned_land['fine'] > 0:
                        fine_amount = returned_land['fine']
                    else:
                        fine_amount = 0
                    customer_name = input("Can you share us your good name: ")
                    invoice = generate_invoice([returned_land], customer_name, "Return", duration, exceed_month, fine_amount)
                    write_invoice_to_file(invoice,customer_name)
                    write_land_data("C:\\Users\\himan\\OneDrive - London Metropolitan University\\Python\\Coursework\\land_data.txt", lands)
                    print("Congratulations!! Land returned successfully.")
                    print("      Invoice generated and saved.\n")
                    print(invoice)
                else:
                    print(f"Oopsss!! Land with kitta number {kitta_number} is not rented or does not exist.")
            except ValueError:
                print("Oopsss!! Invalid input! Please enter a valid kitta number and number of months.")
        elif choice == '5':
            print("Thank you for utilizing the TechnoPropertyNepal Land Rental System. Farewell and have a great day!!")
            break
        else:
            print("Oopsss!! Invalid choice. Please enter a valid option.")
main()
