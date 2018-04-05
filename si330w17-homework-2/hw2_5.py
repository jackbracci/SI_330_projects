import csv
from collections import defaultdict

def read_region_file(filename):
    region_mapping = dict()
    with open (filename, 'r', newline='') as input_file:
        region_reader = csv.DictReader (input_file, delimiter = '\t', quotechar ='"')
        for row in region_reader:
            region_mapping[row['Country']]= row['Region']
    return region_mapping
def main():
    # open the tab-delimited input data file
    with open('locations.csv', 'r', newline = '') as input_file:
        region_data_reader = csv.DictReader(input_file, delimiter='\t', quotechar='"')
        with open('nodes.csv', 'w', newline='') as output_file:
        # Prepare to write out rows to the output file using csv package's DictWriter routines
                # We are going to write out a subset of the original input file's columns, namely, these three:
            region_data_writer = csv.DictWriter(output_file,
                                                     fieldnames=['Country Name', 'Longitude', 'Latitude'],
                                                     extrasaction='ignore',
                                                     delimiter=',', quotechar='"')
        region_data_writer.writeheader()

        row_count = 0
        for row in region_data_reader:
            region_data_writer.writerow(row)

            row_count = row_count + 1

            if row_count % 500 == 0:
                print("Wrote %d rows" % row_count)
        print("Done! Wrote a total of %d rows" % row_count)


        # This is boilerplate python code: it tells the interpreter to execute main() only
        # if this module is being run as the main script by the interpreter, and
        # not being imported as a module.
if __name__ == '__main__':
    main()
