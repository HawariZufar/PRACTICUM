# dummy variable # 
client_data_list = []

# Status Declaration #
list_status = ["Eligible", "Standart", "Not Eligible"]

# List of Data #
list_data = {
    "name": ["Andi", "Budi", "Citra", "Dewi", "Eka"],
    "age": [37, 43, 24, 33, 50],
    "salary": [5_000_000, 6_750_000, 3_225_000, 5_825_000, 8_100_000],
    "saving_rate": [10, 8, 10, 15, 7.5],
    "gender": ["Male", "Male", "Female", "Female", "Female",],
    "pmt_spending": [3_000_000, 3_250_000, 2_850_000, 6_100_000, 2_250_000],
}

# Deklarasi Umur Pensiun Standar dan Bunga Investasi Per Tahun #
standart_retirement_age = 60
return_of_invesment = 0.06

# Login Process #
account_data = {"admin": "admin123", "user": "user123"}
max_attempts = 3 
attempts = 0 
is_logged_in = False 

while attempts < max_attempts and is_logged_in == False: 
    username = input("Enter username: ").strip() 
    password = input("Enter password: ").strip() 
    
    if username not in account_data or account_data[username] != password: 
        attempts += 1  
        print(f"Invalid username or password. {max_attempts - attempts} attempts remaining.")

    else :
        print("Login successful")
        is_logged_in = True
    
if attempts == max_attempts :
    print("Maximum login attempts reached. Exiting program")
    exit()
        
# Input Method

while True:
    input_choice = input("Choose input method (manual/list_data): ").strip().lower()
    if input_choice in ["manual", "list_data"]:
        break
    else:
        print("Invalid choice! Enter 'manual' or 'list_data'.")

# Manual Method #
if input_choice == "manual":

    while True:
        try:
            num_clients = int(input("Enter the number of client data to input: "))
            if num_clients > 0:
                break
            else:
                print("Error: Input must be greater than 0.")
        except ValueError:
            print("Invalid input. Enter a valid number.")
    
    for i in range(num_clients):

        # Input name
        print(f"Client-{i+1}" )
        while True:
            name = input("Enter client name: ").strip().title()
            if name:
                break
            else:
                print("Error: Input cannot be empty!")

        # Input age
        
        while True:
            try:
                age = int(input("Enter client age: "))
                if 0 < age < 60:
                    break
                else:
                    print("Error: Input must be greater than 0 and less than 60.")
            except ValueError:
                print("Invalid input. Enter a valid number.")


        # Input salary
        
        while True:
            try:
                salary = float(input("Enter Monthly Salary (Rp): "))
                if  salary > 0:
                    break
                else:
                    print("Error: Input must be greater than 0")
            except ValueError:
                print("Error: Input must be a valid number!")
                
        # Input saving rate
        
        while True:
            try:
                saving_rate = float(input("Enter Savings Rate (%): "))
                if saving_rate > 0:
                    break
                else:
                    print("Error: Input cannot be less than 0")
            except ValueError:
                print("Error: Input must be a valid number!")

        # Input gender
        
        while True:
            gender = input("Enter client gender (male/female): ").strip().capitalize()
            if gender in ["Male", "Female"]:
                break
            else:
                print("Error: Input must be one of (male/female) !")
                
        # Input pmt_spending
        
        while True:
            try:
                pmt_spending = float(input("Enter PMT Spending (Rp): "))
                if pmt_spending > 0:
                    break
                else:
                    print("Error: Input cannot be less than 0")
            except ValueError:
                print("Error: Input must be a valid number!")
        
        # Memasukkan data ke list data client
        client_data_list.append({
            "name": name,
            "age": age,
            "salary": salary,
            "saving_rate": saving_rate,
            "gender": gender,
            "pmt_spending": pmt_spending,
        })
        
    # list_data method 
else :
    for i in range(len(list_data["name"])):
        client_data_list.append({
                "name": list_data["name"][i],
                "age": list_data["age"][i],
                "salary": list_data["salary"][i],
                "saving_rate": list_data["saving_rate"][i],
                "gender": list_data["gender"][i],
                "pmt_spending": list_data["pmt_spending"][i],
        })

# Perhitungan #
for client in client_data_list:
    
    # hitung lama menabung berdasarkan umur pensiun standar #
    client["years_to_retirement"] = 60 - client["age"]
    # konversi ke bulan
    months_to_retirement = client["years_to_retirement"] * 12

    # decision making nilai life_expectancy
    if client["gender"] == "Male":
        life_expectancy = 70
    else:
        life_expectancy = 75

    # Konversi lama pasca pensiun ke dalam bulan
    post_retirement_time = (life_expectancy - standart_retirement_age) * 12
    
    # konversi ke bulan (asumsi bunga tetap dan ga ada inflasi)
    r = return_of_invesment/12

    client["pmt_saving"] = client["salary"] * (client["saving_rate"] / 100)

    # # Present Value Annuity # (dana yang dibutuhkan untuk mencapai target pensiun dengan dana per bulan yang diinginkan user)
    client["pva"] = client["pmt_spending"] * ( ( 1 -( 1 / ( (1+r) **post_retirement_time) ) )/ r )

    # # Future Value Annuity # (jumlah dana hasil tabungan dengan iuran berdasarkan usia standar pensiun)
    client["fva_standard"] = client["pmt_saving"] * ((((1 + r)**months_to_retirement) - 1)/r)

    # Hitung Persentase Kecukupan Dana #
    coverage_ratio = client["fva_standard"] / client["pva"] 

    # decision making status (klasifikasi status berdasarkan coverage ratio) 
    if coverage_ratio > 1:
        client["status"] = list_status[0]
    elif coverage_ratio == 1:
        client["status"] = list_status[1]
    else:
        client["status"] = list_status[2]  

    # Hitung Umur Untuk Pensiun #
    # melakukan iterasi tabungan sebanyak bulan n hingga lebih dari atau sama dengan PV (dana yang dibutuhkan ketika pensiun)
    fva_target = 0
    month_target = 1
    while fva_target < client["pva"]:
        fva_target = client["pmt_saving"] * ((((1 + r)**month_target) - 1)/r)
        month_target +=1

    # convert bulan target tercapai #
    client["year_target"] = int(month_target/12) + 1

    # usia pensiun berdasarkan target dari iuran user #
    client["retirement_age"] = (client["age"] + client["year_target"])
    
    # monthly contribution recommendation with age of retirement = 60 #
    client["pmt_saving_standard"] = ((client["pva"] * r)) / (((1 + r)**months_to_retirement) - 1)
    
    client["saving_rate_standard"] = client["pmt_saving_standard"] * 100 / client["salary"]

print("\n")
print("=" * 126)
print(f"| {"SUMMARY":^122} |")
print("-" * 126)
print(f"| {"No":<3} | {"Name":<10} | {"Age":<3} | {"Gender":<7} | {"Salary":<15} | {"PMT Spending":<15} | {"PVA":<16} | {"FVA Standard":<16} | {"Status":<13} |")
print("=" * 126)

for idx, client in enumerate(client_data_list, start=1):   
    print(f"| {idx:<3} | {client["name"]:<10} | {client["age"]:<3} | {client["gender"]:<7} | Rp{client["salary"]:<13,.2f} | Rp{client["pmt_spending"]:<13,.2f} | Rp{client["pva"]:<14,.2f} | Rp{client["fva_standard"]:<14,.2f} | {client["status"]:<13} |")

print("=" * 126)

print("\n")
print("=" * 123)
print(f"| {"RECOMMENDATION":^119} |")
print("-" * 123)

print(f"| {"No":<3} | {"Name":<10} | {"Existing PMT":<16} | {"Existing Rate":<7} | {"Minimum PMT":<16} | {"Minimum Rate":<8} | {"Remaining Time":<12} | {"Estimated Time":<12} |")
print("=" * 123)

for idx, client in enumerate(client_data_list, start=1):
    print(f"| {idx:<3} | {client["name"]:<10} | Rp{client["pmt_saving"]:<14,.2f} | {client["saving_rate"]:<12,.2f}% | Rp{client["pmt_saving_standard"]:<14,.2f} | {client["saving_rate_standard"]:<11,.2f}% | {client["years_to_retirement"]:<8} years | {client["year_target"]:<8} years |")

print("=" * 123)