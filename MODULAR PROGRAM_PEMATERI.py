# # Global Variabel Declaration
STANDARD_RETIREMENT_AGE = 60
RETURN_OF_INVESTMENT = 0.06
LIST_STATUS = ['Eligible', 'Standard', 'Not Eligible']

LIST_DATA = {
    'name': ['Andi', 'Budi', 'Citra', 'Dewi', 'Eka'],
    'age': [37, 43, 24, 33, 50],
    'salary': [5_000_000, 6_750_000, 3_225_000, 5_825_000, 8_100_000],
    'saving_rate': [10, 8, 10, 15, 7.5],
    'gender': ['Male', 'Male', 'Female', 'Female', 'Female',],
    'pmt_spending': [3_000_000, 3_250_000, 2_850_000, 6_100_000, 2_250_000],
}

ACCOUNT_DATA = {
    'admin': 'admin123',
    'user': 'user123'
}

CLIENT_DATA_LIST = []

# Login
def login():
    max_attempts = 3
    attempts = 0

    while attempts < max_attempts:
        username = input("Enter username: ").strip()
        password = input("Enter password: ").strip()

        if username not in ACCOUNT_DATA or ACCOUNT_DATA[username] != password:
            attempts += 1  
            print(f"Invalid username or password. {max_attempts - attempts} attempts remaining.")
        else:
            print('Login successful')
            return True

    return False

# # Validate Input
def validate_input(prompt, input_type, valid_values=None, min_value=None, max_value=None):
    while True:
        try:
            if input_type == 'str':
                value = input(prompt).strip().capitalize()
                if not value:
                    raise ValueError("Input cannot be empty")
                if valid_values and value not in valid_values:
                    raise ValueError(f"Input must be one of {valid_values}")
                return value

            elif input_type == 'int':
                value = int(input(prompt))
                if min_value is not None and value < min_value:
                    raise ValueError("Value too small")
                if max_value is not None and value > max_value:
                    raise ValueError("Value too large")
                return value

            elif input_type == 'float':
                value = float(input(prompt))
                if min_value is not None and value < min_value:
                    raise ValueError("Value too small")
                return value

        except ValueError as e:
            print(f"Error: {e}")


# #Manual Input
def manual_input():
    CLIENT_DATA_LIST.append({
        'name': validate_input("Enter client name: ", 'str'),
        'age': validate_input("Enter client age: ", 'int', min_value=1, max_value=59),
        'salary': validate_input("Enter Monthly Salary (Rp): ", 'float', min_value=1),
        'saving_rate': validate_input("Enter savings rate: ", 'float', min_value=0.1),
        'gender': validate_input("Enter client gender (male/female): ", 'str', valid_values=['Male', 'Female']),
        'pmt_spending': validate_input("Enter PMT Spending (Rp): ", 'float', min_value=1)
    })

# #List Data Input
def list_data_input():
    for i in range(len(LIST_DATA['name'])):
        CLIENT_DATA_LIST.append({
                'name': LIST_DATA["name"][i],
                'age': LIST_DATA["age"][i],
                'salary': LIST_DATA["salary"][i],
                'saving_rate': LIST_DATA["saving_rate"][i],
                'gender': LIST_DATA["gender"][i],
                'pmt_spending': LIST_DATA["pmt_spending"][i],
        })
        
# # Calculation
def calculation(client):

    years_to_retirement = STANDARD_RETIREMENT_AGE - client['age']

    months_to_retirement = years_to_retirement * 12

    life_expectancy = life_expectancy_calculation(client["gender"])
        
    post_retirement_time = (life_expectancy - STANDARD_RETIREMENT_AGE) * 12

    r = RETURN_OF_INVESTMENT / 12

    pmt_saving = client["salary"] * (client["saving_rate"] / 100)
    
    pva = client['pmt_spending'] * ( (1 - (1 / (1 + r) ** post_retirement_time)) / r )

    fva_standard = pmt_saving * (((1 + r) ** months_to_retirement - 1) / r)

    coverage_ratio = fva_standard / pva

    status = classification(coverage_ratio)

    fva_target = 0
    month_target = 1
    while fva_target < pva:
        fva_target = pmt_saving * ( ((1 + r) ** month_target - 1) / r )
        month_target += 1

    year_target = round(month_target / 12) + 1

    retirement_age = (client['age']) + year_target

    pmt_saving_standard = pva * r / ((1 + r) ** months_to_retirement - 1)
    
    saving_rate_standard = (pmt_saving_standard / client['salary']) * 100
    
    client.update({
        'years_to_retirement': years_to_retirement,
        'life_expectancy': life_expectancy,
        'pmt_saving': pmt_saving,
        'pva': pva,
        'fva_standard': fva_standard,
        'coverage_ratio': coverage_ratio,
        'year_target': year_target,
        'retirement_age': retirement_age,
        'pmt_saving_standard': pmt_saving_standard,
        'saving_rate_standard': saving_rate_standard,
        'status': status
    })

    return client

# # Classification
def classification(coverage_ratio):
    if coverage_ratio > 1:
        status = LIST_STATUS[0]
    elif coverage_ratio == 1:
        status = LIST_STATUS[1]
    else:
        status = LIST_STATUS[2]
    return status

def life_expectancy_calculation(gender):
    if gender == 'Male':
        life_expectancy = 70
    else:
        life_expectancy = 75
    return life_expectancy

def show_data():  
    print("\n")
    print("=" * 126)
    print(f"| {'SUMMARY':^122} |")
    print("-" * 126)
    print(f"| {'No':<3} | {'Name':<10} | {'Age':<3} | {'Gender':<7} | {'Salary':<15} | {'PMT Spending':<15} | {'PVA':<16} | {'FVA Standard':<16} | {'Status':<13} |")
    print("=" * 126)

    for idx, client in enumerate(CLIENT_DATA_LIST, start=1):   
        print(f"| {idx:<3} | {client['name']:<10} | {client['age']:<3} | {client['gender']:<7} | Rp{client['salary']:<13,.2f} | Rp{client['pmt_spending']:<13,.2f} | Rp{client['pva']:<14,.2f} | Rp{client['fva_standard']:<14,.2f} | {client["status"]:<13} |")

    print("=" * 126)

    print("\n")
    print("=" * 123)
    print(f"| {'RECOMMENDATION':^119} |")
    print("-" * 123)

    print(f"| {'No':<3} | {'Name':<10} | {'Existing PMT':<16} | {'Existing Rate':<7} | {'Minimum PMT':<16} | {'Minimum Rate':<8} | {'Remaining Time':<12} | {'Estimated Time':<12} |")
    print("=" * 123)

    for idx, client in enumerate(CLIENT_DATA_LIST, start=1):
        print(f"| {idx:<3} | {client['name']:<10} | Rp{client['pmt_saving']:<14,.2f} | {client['saving_rate']:<12,.2f}% | Rp{client['pmt_saving_standard']:<14,.2f} | {client['saving_rate_standard']:<11,.2f}% | {client['years_to_retirement']:<8} years | {client['year_target']:<8} years |")

    print("=" * 123)

## Main
def main():
    method = validate_input(
        "Choose input method (manual or list_data): ",
        'str',
        valid_values=['Manual', 'List_data']
    )

    if method == 'Manual':
        n = validate_input("Enter the number of client data to input: ", 'int', min_value=1)
        for i in range(n):
            print(f"Client-{i+1}")
            manual_input()
    else:
        list_data_input()

    for i, client in enumerate(CLIENT_DATA_LIST):
        CLIENT_DATA_LIST[i] = calculation(client)

    show_data()

# #Program Overview
if login():
    main()
else:
    print("Maximum login attempts reached. Program terminated.")

    exit()
