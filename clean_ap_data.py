import pandas as pd
import re

input_file = r"C:\Users\User\OneDrive - Convergint\Finance (SharePoint)\Accounts Payable\AP_Data.csv"
output_file = r"C:\Users\User\OneDrive - Convergint\Finance (SharePoint)\Accounts Payable\AP_Data_Cleaned.csv"

def clean_amount(row):
    value = str(row['Amount (Foreign Currency)'])
    currency = str(row['Currency']).strip()

    if pd.isna(value) or value == '':
        return value

    value = re.sub(r'S\$|RM|Rp|AU\$â€Ž|â‚¬|Â£|â‚©â€Ž|PHP|Ä‘|à¸¿', '', value).strip()

    if currency in ['IDR', 'VND']:
        if ',' in value and '.' in value:
            parts = value.rsplit(',', 1)
            integer_part = parts[0].replace('.', '')  #Remove thousand separators
            decimal_part = parts[1]
            value = f"{integer_part}.{decimal_part}"

    value = re.sub(r'[^0-9.]', '', value)

    # Step 4: Collapse multiple dots (e.g., "12..50" → "12.50")
    value = re.sub(r'\.{2,}', '.', value).strip('.')

    try:
        return float(value)
    except ValueError:
        return None

df = pd.read_csv(input_file)
df['Amount (Foreign Currency)'] = df.apply(clean_amount, axis=1)
df.to_csv(output_file, index=False)

print("Done")
