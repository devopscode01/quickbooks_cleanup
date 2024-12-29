import pandas as pd
from fuzzywuzzy import process

def process_statement(input_file, quickbooks_file, output_file):
    # Read the CSV file into a DataFrame with a specific header row
    df = pd.read_csv(input_file, header=6)

    # Remove 'Running Bal.' column if it exists
    if 'Running Bal.' in df.columns:
        df = df.drop('Running Bal.', axis=1)

    # Filter rows based on 'Amount' column
    if 'Amount' in df.columns:
        df['Amount'] = df['Amount'].astype(str)
        df = df[~df['Amount'].str.startswith('-')]

    # Filter rows based on 'Description' column
    if 'Description' in df.columns:
        df = df[df['Description'].str.contains('Zelle|Offering|Conference|Easter')]
        df = df[df['Description'].str.contains('Zelle')]

    # Extract names from 'Description'
    name_pattern = r'(?:Zelle Transfer Conf# \w+;|Zelle payment from) (?P<FirstName>\w+),? (?P<LastName>\w+)'
    df[['FirstName', 'LastName']] = df['Description'].str.extract(name_pattern)

    # Combine first and last names
    df['F'] = df['FirstName'] + ' ' + df['LastName']

    # Read QuickBooks names
    quickbooks_df = pd.read_csv(quickbooks_file)

    # Fuzzy matching function
    def fuzzy_lookup(name, choices):
        match, score = process.extractOne(name, choices)
        return match if score >= 80 else None

    # Apply fuzzy matching
    df['Matched_names'] = df['F'].apply(lambda x: fuzzy_lookup(x, quickbooks_df['Customer']))

    # Export the transformed DataFrame
    df.to_csv(output_file, index=False)
    print(f"Transformed data saved to {output_file}")

if __name__ == "__main__":
    process_statement(
        input_file="input/stmt_2024.csv",  # Updated to match the new file name
        quickbooks_file="input/quickbooks_names.csv",
        output_file="output/transformed_stmt_2024.csv"
    )
