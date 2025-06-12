# MPIN Strength Checker Program
from datetime import datetime

# simple patterns
common_mpins = [
    '0000', '1111', '1234', '1212', '7777', '9999', '1004', '2000',
    '4444', '2222', '6969', '4321', '1010', '1122',
    '123456', '654321', '111111', '000000', '121212', '999999'
]

def extract_possible_pins_from_date(date_str):
    try:
        date_obj = datetime.strptime(date_str, "%d-%m-%Y")
        day = date_obj.strftime("%d")
        month = date_obj.strftime("%m")
        year_full = date_obj.strftime("%Y")
        year_short = date_obj.strftime("%y")

        combos = set()

        # Some basic combos 
        combos.add(day + month)
        combos.add(month + day)
        combos.add(day + year_short)
        combos.add(year_short + day)
        combos.add(month + year_short)
        combos.add(year_short + month)

        # 6-digit combos
        combos.add(day + month + year_short)
        combos.add(day + month + year_full)
        combos.add(month + day + year_short)
        combos.add(month + day + year_full)

        return combos
    except ValueError:
        return set()

#checks strength

def check_mpin_strength_full(mpin, dob_self=None, dob_spouse=None, anniversary=None):
    reasons = []

    if mpin in common_mpins:
        reasons.append("COMMONLY_USED")

    if dob_self:
        if mpin in extract_possible_pins_from_date(dob_self):
            reasons.append("DEMOGRAPHIC_DOB_SELF")

    if dob_spouse:
        if mpin in extract_possible_pins_from_date(dob_spouse):
            reasons.append("DEMOGRAPHIC_DOB_SPOUSE")

    if anniversary:
        if mpin in extract_possible_pins_from_date(anniversary):
            reasons.append("DEMOGRAPHIC_ANNIVERSARY")

    if len(reasons) == 0:
        strength = "STRONG"
    else:
        strength = "WEAK"

    return {
        "strength": strength,
        "reasons": reasons
    }

# test cases

def run_test_cases():
    print("\nRunning Test Cases...\n")
    tests = [
        {"mpin": "1234", "dob_self": None, "dob_spouse": None, "anniversary": None},
        {"mpin": "0705", "dob_self": "07-05-2000"},
        {"mpin": "0507", "dob_spouse": "05-07-2000"},
        {"mpin": "1402", "anniversary": "14-02-2010"},
        {"mpin": "14102001", "dob_self": "14-10-2001"},
        {"mpin": "123456"},
        {"mpin": "070500", "dob_self": "07-05-2000"},
        {"mpin": "07052000", "dob_self": "07-05-2000"},
        {"mpin": "140299", "anniversary": "14-02-1999"},
        {"mpin": "0000"},
        {"mpin": "7890", "dob_self": "05-09-1998"},
        {"mpin": "0510", "dob_self": "10-05-2000"},
        {"mpin": "1010", "dob_spouse": "10-10-1998"},
        {"mpin": "1515"},
        {"mpin": "2601", "dob_self": "26-01-2001"},
        {"mpin": "070598", "dob_self": "07-05-1998"},
        {"mpin": "07052001", "dob_spouse": "07-05-2001"},
        {"mpin": "15082000", "anniversary": "15-08-2000"},
        {"mpin": "9999"},
        {"mpin": "05111998", "dob_self": "05-11-1998"}
    ]

    for i, test in enumerate(tests, start=1):
        result = check_mpin_strength_full(
            test.get("mpin"),
            dob_self=test.get("dob_self"),
            dob_spouse=test.get("dob_spouse"),
            anniversary=test.get("anniversary")
        )
        print(f"Test {i}: MPIN = {test['mpin']} => Strength: {result['strength']}, Reasons: {result['reasons']}")

if __name__ == "__main__":
    print("MPIN Strength Checker")
    print("----------------------")
    mpin_input = input("Enter your MPIN (4 or 6 digits): ")
    dob = input("Enter your DOB (DD-MM-YYYY): ")
    spouse_dob = input("Spouse DOB (DD-MM-YYYY) [optional]: ") or None
    anniv = input("Anniversary (DD-MM-YYYY) [optional]: ") or None

    result = check_mpin_strength_full(mpin_input, dob, spouse_dob, anniv)

    print("\nResult:")
    print("Strength:", result["strength"])
    if result["reasons"]:
        print("Reasons:", ", ".join(result["reasons"]))


    run_test_cases()
