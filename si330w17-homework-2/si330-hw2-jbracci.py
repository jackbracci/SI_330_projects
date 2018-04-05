import csv
from collections import defaultdict


def year_from_date(date):
    year = str.split(date, '/')[2]
    return(year)

def read_directed_graph_from_csv(filename, source_column, dest_column, weight_column):
    graph = defaultdict(list)
    with open(filename, 'r', newline = '') as input_file:
        graph_file_reader = csv.DictReader(input_file, delimiter=',', quotechar = '"')
        for row in graph_file_reader:
            try:
                source_column = row['Country Origin Name']
                dest_column = row['Country Dest Name']
                weight_column = float(row['2000 [2000]'])
                tup_1 = (source_column,weight_column)

                if dest_column not in graph.keys():
                    graph[dest_column] = []
                    graph[dest_column].append(tup_1)
                else:
                    graph[dest_column].append(tup_1)
            except:
                continue
        for key,value in graph.items():
            value.sort(key=lambda x:x[1], reverse=True)
    return (graph)

def read_directed_graph2_from_csv(filename, source_column, dest_column, weight_column):
    graph2 = defaultdict(list)
    with open(filename, 'r', newline = '') as input_file:
        graph_file_reader = csv.DictReader(input_file, delimiter=',', quotechar = '"')
        for row in graph_file_reader:
            try:
                source_column = row['Country Origin Name']
                dest_column = row['Country Dest Name']
                weight_column = float(row['2000 [2000]'])
                tup_2 = (dest_column,weight_column)
                if source_column not in graph2.keys():
                    graph2[source_column] = []
                    graph2[source_column].append(tup_2)
                else:
                    graph2[source_column].append(tup_2)
            except:
                continue
        for key,value in graph2.items():
            value.sort(key=lambda x:x[1], reverse=True)
    return (graph2)

def read_region_file(filename):
    region_mapping = dict()
    with open (filename, 'r', newline='') as input_file:
        region_reader = csv.DictReader (input_file, delimiter = '\t', quotechar ='"')
        for row in region_reader:
            region_mapping[row['Country']]= row['Region']
    return region_mapping

def export_files(file1, file2):
    nodedictionary = dict()
    edgesdictionary = []
    with open(file1, 'r', newline = '') as input1:
        # prepare to read the rows of the file using the csv packages' DictReader routines
        locations_data_reader = csv.DictReader(input1, delimiter=',', quotechar ='"')

        with open('si330-hw2-nodes-jbracci.csv', 'w', newline='') as output_file:
            nodes_data_writer = csv.DictWriter(output_file,
                                            fieldnames = ['country', 'latitude',
                                                        'longitude'],
                                            extrasaction= 'ignore',
                                            delimiter = ',', quotechar = '"')
            nodes_data_writer.writeheader()
            row_count = 0
            for row in locations_data_reader:

                row['country'] = row['Country Name']
                country = row['country']
                row['latitude'] = row['Latitude']
                latitude = row['latitude']
                row['longitude'] = row['Longitude']
                longitude = row['longitude']
                nodedictionary[country] = (row['latitude'], row['longitude'])
                nodes_data_writer.writerow(row)
                row_count = row_count + 1
        with open(file2, 'r', newline='') as input_file2:
        # prepare to read the rows of the file using the csv packages' DictReader routines
            locations_data_reader = csv.DictReader(input_file2, delimiter=',', quotechar='"')

            with open('si330-hw2-edges-jbracci.csv', 'w', newline='') as output_file:
                edges_data_writer = csv.DictWriter(output_file,
                                                   fieldnames=['start_country', 'end_country', 'start_lat', 'start_long',
                                                               'end_lat', 'end_long', 'count'],
                                                   extrasaction='ignore',
                                                   delimiter=',', quotechar='"')
                edges_data_writer.writeheader()
                row_count = 0
                for row in locations_data_reader:
                    if row['Country Origin Name'] not in nodedictionary or row['Country Dest Name'] not in nodedictionary:
                        continue
                    start_country = row['Country Origin Name']
                    row['start_country'] = start_country
                    end_country = row['Country Dest Name']
                    row['end_country'] = end_country

                    row['start_lat'] = nodedictionary[row['start_country']][0]
                    row['start_long'] = nodedictionary[row['start_country']][1]

                    row['end_lat'] = nodedictionary[row['end_country']][0]
                    row['end_long'] = nodedictionary[row['end_country']][1]

                    if row['2000 [2000]'] == ".." or row['2000 [2000]'] == "":
                        continue
                    row['count'] = float(row['2000 [2000]'])
                    edgesdictionary.append(row)
                    row_count = row_count + 1

                edgesdictionary = sorted(edgesdictionary, key=lambda x: x['count'], reverse=True)[0:1000]

                for row in edgesdictionary:
                    edges_data_writer.writerow(row)

def main():
    # open the tab-delimited input data file
    with open('world_bank_country_data.txt', 'r', newline = '') as input_file:
        # prepare to read the rows of the file using the csv packages' DictReader routines
        country_data_reader = csv.DictReader(input_file, delimiter='\t', quotechar ='"')
        region_data_reader = read_region_file('world_bank_regions.txt')
        migration_outflow_graph = read_directed_graph_from_csv("world_bank_migration.csv",
                                                               "Country Origin Name", "Country Dest Name",
                                                               "2000 [2000]")
        migration_outflow_graph2 = read_directed_graph2_from_csv("world_bank_migration.csv",
                                                               "Country Origin Name", "Country Dest Name",
                                                               "2000 [2000]")

        # open a new output file
        with open('world_bank-output-jbracci-hw2.csv', 'w', newline = '') as output_file:
            # Prepare to write out rows to the output file using csv package's DictWriter routines
            # We are going to write out a subset of the original input file's columns, namely, these three:
            country_data_writer = csv.DictWriter(output_file,
                                                 fieldnames = ['Region','Country Name','Mobile users per capita', 'Population: Total (count)','Year','Migration: Top 3 destinations','Migration: Top 3 sources' ],
                                                 extrasaction = 'ignore',
                                                 delimiter = ',', quotechar = '"')
            # write the column header to the output file
            country_data_writer.writeheader()

            row_count = 0
            for row in country_data_reader:

                if year_from_date(row['Date']) == ('2000'):
                    row['Year'] = year_from_date(row['Date'])

                    try:
                        row['Migration: Top 3 destinations'] = migration_outflow_graph2[row['Country Name']][0:3]
                    except:
                        continue
                    try:
                        row['Migration: Top 3 sources'] = migration_outflow_graph[row['Country Name']][0:3]
                    except:
                        continue

                    try:
                        data = row['Business: Mobile phone subscribers']
                        x = data.replace(',','')
                        x.strip("")
                        val_1 = float(x)
                    except:
                        x = 0

                    pop = row['Population: Total (count)']
                    xx = pop.replace(',', '')
                    xx.strip("")
                    val_2 = float(xx)
                    row['Population: Total (count)'] = val_2

                    if x == 0:
                        row["Mobile users per capita"] = 'NA'
                    else:
                        div = (val_1 / val_2)
                        div = "{0:0.2f}".format(div)
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
            export_files('locations.csv', 'world_bank_migration.csv')


# This is boilerplate python code: it tells the interpreter to execute main() only
# if this module is being run as the main script by the interpreter, and
# not being imported as a module.
if __name__ == '__main__':
    main()
