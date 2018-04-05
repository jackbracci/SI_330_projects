#!/usr/bin/env python
# SI 330 Lab 1 sample file

# We use the csv package to read and write delimited text files
# This program reads a tab-delimited file, parses a date field, adds a new column and writes a comma-delimited file
import csv

def year_from_date(date):
    year = str.split(date, '/')[2]
    return(year)

def read_region_file(filename):
    region_mapping = dict()
    with open (filename, 'r', newline='') as input_file:
        region_reader = csv.DictReader (input_file, delimiter = '\t', quotechar ='"')
        for row in region_reader:
            region_mapping[row['Country']]= row['Region']


    return region_mapping



def main():
    # open the tab-delimited input data file
    with open('world_bank_country_data.txt', 'r', newline = '') as input_file:
        # prepare to read the rows of the file using the csv packages' DictReader routines
        country_data_reader = csv.DictReader(input_file, delimiter='\t', quotechar ='"')
        region_data_reader = read_region_file('world_bank_regions.txt')
        # open a new output file
        with open('world_bank_output_result.csv', 'w', newline = '') as output_file:
            # Prepare to write out rows to the output file using csv package's DictWriter routines
            # We are going to write out a subset of the original input file's columns, namely, these three:
            country_data_writer = csv.DictWriter(output_file,
                                                 fieldnames = ['Region','Country Name','Mobile users per capita', 'Population: Total (count)','Year' ],
                                                 extrasaction = 'ignore',
                                                 delimiter = ',', quotechar = '"')
            # write the column header to the output file
            country_data_writer.writeheader()

            row_count = 0
            for row in country_data_reader:

                if year_from_date(row['Date']) == ('2000') or year_from_date(row['Date']) == ('2010'):
                    row['Year'] = year_from_date(row['Date'])


                    try:
                        data = row['Business: Mobile phone subscribers']
                        x = data.replace(',','')
                        x.strip("")
                        convert = float(x)
                    except:
                        x = 0


                    pop = row['Population: Total (count)']
                    xx = pop.replace(',', '')
                    xx.strip("")
                    conv = float(xx)
                    row['Population: Total (count)'] = conv


                    if x == 0:
                        row["Mobile users per capita"] = 'NA'
                    else:
                        div = (convert / conv)
                        div = str(div)[0:4]
                        row["Mobile users per capita"] = div


                    try:
                        row['Region']= region_data_reader[row['Country Name']]

                    except:
                        row['Region']= 'NA'


                    country_data_writer.writerow(row)
                    row_count = row_count + 1


                    if row_count % 500 == 0:
                        print("Wrote %d rows" % row_count)
            print("Done! Wrote a total of %d rows" % row_count)


# This is boilerplate python code: it tells the interpreter to execute main() only
# if this module is being run as the main script by the interpreter, and
# not being imported as a module.
if __name__ == '__main__':
    main()

