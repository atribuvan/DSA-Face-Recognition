import csv


input_csv_file = 'app/reference.csv'
output_csv_file = 'output.csv'

def extract_and_save_column(input_file, output_file):
    try:
        with open(input_file, mode='r', newline='') as infile, open(output_file, mode='w', newline='') as outfile:
            reader = csv.reader(infile)
            writer = csv.writer(outfile)

            extracted_column = []

            for row in reader:
                if len(row) >= 3:
                    extracted_column.append([row[2]])  

            writer.writerows(extracted_column)

        return True 

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return False 

result = extract_and_save_column(input_csv_file, output_csv_file)

if result:
    print(f"The 3rd column has been successfully extracted and saved to '{output_csv_file}'.")
else:
    print("Extraction and save process failed.")
