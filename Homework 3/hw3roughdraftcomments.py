import profile
import csv
# The import function is built into python that allows one to import other packages to use while coding in python
# Here, we are reusing the document distance code
from docdist_dict import (get_words_from_string, count_frequency, vector_angle)
# This is importing these three given functions from another python file that one can call while writing optimize this
# file
'''Change 1:
 1. changed imported file from docdist1 to docdist_dist
 2. Before: 131.829, After: 18.130
 3. Reduction Factor: 131.829/18.130 = 7.27'''
# As a convention, "constant" variable names are usually written in all-caps
OUTPUT_FILE = 'Sentence-Database-hw3.csv'
# MASTER_FILE = 'Sentences_Table_MasterList_sample.csv'
# SENTENCE_DB_FILE = 'Sentence_Database_Without_ID_sample.csv'
MASTER_FILE = 'Sentences_Table_MasterList.csv'
SENTENCE_DB_FILE = 'Sentence_Database_Without_ID.csv'



def get_csv_rows(filename):
    '''Read the CSV file using DictReader and then append all rows in a list'''
    with open(filename, 'r', newline='') as input_file:
        reader = csv.DictReader(input_file, delimiter=',', quotechar='"')

        data = []
        for row in reader:
            data.append(row)

        return data



def main():
    global MASTER_FILE, SENTENCE_DB_FILE
# setting the two files above as global variables so when called they refer to the files named that above

    # we will be collecting each row of the output file in this list
    output = []
    row_count = 0


    # looping through the SENTENCE_DB_FILE to process each row
    for row in get_csv_rows(SENTENCE_DB_FILE):
        set_sentence_id(row)
        replace_target_with_blank(row)
# this for loop is iterating through the file SENTENCE_DB_FILE to a list called data that is using DictReader and then
# appending all rows from that file to a list, we know this because when one calls get_csv_rows this creates
# the data list, then is iterating through calling set_sentence_id and replace_target_with_blank to then assign each of
# iterations a value for the replace_target_with_blank(row) to XXXXX by calling these functions
        if row['SentID_GM'] != 'NA':
            lookup_similar_id(row)
            find_alternate_sentence(row)
            find_unique_targets(row)
# This conditional statement is saying if the 'SentID_GM has a value that is not equal to 'NA', then call the three
# functions to then run through those individual definitions that I will explain later in the code
        output.append(row)
        row_count += 1
        print(row_count)

    write_output_file(output)
    # Once all of the other functions are called the they are appending to the output list, then printing 1,2,3... as each
    # list is iterated through and then calling the write_output_file(output) by telling it to pass the new output list
    # through the function

'''Change 3
1. outdented from the for loop so that it doesnt have to write the output every time
2.Before: 17.892 seconds, After: 17.392
3.Reduction Factor: 17.892/17.392 = 1.028'''



sentence_id_dic = {} #creating an empty dictionary
for record in get_csv_rows(MASTER_FILE): # using a for loop to iterate through the list of rows for the Master File
    sentence_id_dic[record['Sentence_with_Target'].strip()] = record #Setting the dictionary key equal to Sentence_with_Target and the values to dictionaries of the rows


    '''Change 2
    1. This creates an empty dictionary indexed with Sentence_with_Target to replace having to iterate through the for loop and using the set_sentence_id function
    2. Before: 18.130, After: 17.892
    3. Reduction Factor: 18.130/17.892 = 1.013
    '''
def set_sentence_id(row):

    lookup_key = row['Sentence'].strip() #I created a variable to be equal to the sentence we want to search for
    if lookup_key in sentence_id_dic: #looking to see if the key is in the dic
        row['SentID_GM'] = sentence_id_dic[lookup_key]['SentID_GM'] #Then changes the row with the new SentID_GM
    else:
        row['SentID_GM'] = 'NA' #if no match is found set SENTID_GM to 'NA'

'''Change 4
1. got rid of the for loop because of the dictionary we created and now searching for keys in the dictionary
2.Before: 17.392 seconds, After: 14.428
3.Reduction Factor: 17.392/14.428 = 1.205'''

'''
# Initial code that we were given before I made the changes above

    for record in get_csv_rows(MASTER_FILE):
        # record is a row in MASTER_FILE so this for loop is iterating through the rows in the master file
        if record['Sentence_with_Target'].strip() == row['Sentence'].strip():
            # found a matching sentence!
            # If the sentence in the master file is equal to the sentence that is being iterated through from the
            # sentence DB file then they will set the ID from the master file equal to the sentence being iterated
            # through, giving them the same ID. This is after they are both striped which means they are getting
            # rid of all white space characters.
            row['SentID_GM'] = record['SentID_GM']
            break
# break is a built in python function that stops iteration and then starts back up at the next statement
        else:
            # the default value
            row['SentID_GM'] = 'NA'
            # If the row 'sentence' that was iterated through did not find a match to a record 'sentence' in the
            # master file then the ID will be set equal to 'NA' for that given sentence

'''
def replace_target_with_blank(row):

    new_words = []
    # new words is being created into an empty list
    # Here, we split the sentence into words and loop through it till we find the target
    for word in row['Sentence'].split():
        if word[0]=='[' and (word[-1]==']' or word[-2:]=='].') and word[1:-1]==row['Targ']:
            new_words.append('XXXXX')
            #The sentences are being split into individual strings which are words and then the conditional statement
            # is checking to see if the first and the last characters are equal to '['']' or is equal to '[''].' and the
            # middle part of the word is equal to the target then append ('XXXXX') as a string to the new_words list
        else:
            new_words.append(word)
            # if the above conditional is not true then just apend the word as a string to the new words list

    row['Sentence_With_Blank'] = ' '.join(new_words)
# After the iteration the row['Sentence_with_Blank'] is then setting a space and the new word equal with the .join
# so when it concatenates the strings they will return one string

lookup_similar_id_dic = {} #creating an empty dictionary
for record in get_csv_rows(MASTER_FILE): #for loop to iterate through a list of rows in master file
    lookup_similar_id_dic[record['SentID_GM']] = record # Setting the dictionary key equal to Sentence_with_Target, then setting the values into the dic


def lookup_similar_id(row):
    '''
        The MASTER_FILE also has a column 'SimilarTo_SentID_GM',
        which is the sentence ID of a similar sentence in the MASTER_FILE.

        In this function, we lookup the similar sentence for the given 'row',
        using the data in the MASTER_FILE

        # -------------------------------------------------------------------------
        # Implement a better way to find similar sentence,
        # without looping through the each row again and again
        #
        # Ask yourself:
        # -------------
        #   - Is "list" the best data structure for "lookup / search"?
        #   - What is the 'type' of running time for the current implementation?
        #     Is it linear or quadratic?
        #   - Can I reuse something from a previous step?
        #
        # -------------------------------------------------------------------------

    '''
    similar_to = None
    lookup_key = row['SentID_GM']
    if lookup_key in lookup_similar_id_dic:
        similar_to = lookup_similar_id_dic[lookup_key]['SimilarTo_SentID_GM']

    if similar_to is not None:
        if similar_to in lookup_similar_id_dic:
            row['SimilarTo_Sentence'] = lookup_similar_id_dic[similar_to]['Sentence_with_Target']
            row['SimilarTo_SentID_GM'] = similar_to

#Same as described below but using a dictionary

'''
CHANGE NUMBER: 5
1. looking through the keys in the dictionary we already created instead of going through an iteration for each one
2. Before:14.428 , After:8.271
3.Reduction Factor: 14.428/8.271 = 1.744
'''

'''
    similar_to = None
    # Here we get SimilarTo_SentID_GM for this row's SentID_GM using the MASTER_FILE
    for record in get_csv_rows(MASTER_FILE):
        # record is a row in MASTER_FILE
        if record['SentID_GM'] == row['SentID_GM']:
            # found a match
            # If the value from master file and the sentence DB file are equivalent then they will set the similar_to
            # value equal to the ID value from the master file
            similar_to = record['SimilarTo_SentID_GM']
            break
            # break is a built in python function that stops iteration and then starts back up at the next statement

    # then we find the similar sentence from the MASTER_FILE
    if similar_to is not None:
        # if the similar_to was given an ID value that is not none then enter the for loop
        for record in get_csv_rows(MASTER_FILE):
            # record is a row in MASTER_FILE
            if record['SentID_GM'] == similar_to:
                row['SimilarTo_Sentence'] = record['Sentence_with_Target']
                row['SimilarTo_SentID_GM'] = similar_to
                # if the SentID and the similar_to are equivalent then set the values on the left equal to the values
                # on the left
                break
# break is a built in python function that stops iteration and then starts back up at the next statement
'''

def find_alternate_sentence(row):
    '''
        Just like SimilarTo_Sentence and SimilarTo_SentID_GM, we will determine
        Alternate_SimilarTo_Sentence and Alternate_SimilarTo_SentID_GM
        by calculating the cosine distance between two sentences
        using the **document distance** code that we discussed in the previous class

        # -------------------------------------------------------------------------
        # Your aim in this function is to speed up the code using a simple trick
        # and a modification
        #
        # ----------
        # PRE-BONUS hints (to help get to 10x speedup):
        # Hint #1: Look at the other files in the folder.
        # Hint #2: You can speed up this function A LOT without changing a
        #          single line of it!
        #
        # Ask yourself:
        # -------------
        #   - Why are the functions called here so slow?
        #   - Is there something you learned in the class about "document distance" problem,
        #     that can be used here?
        #
        # -----
        # BONUS hints: (to get more than 10x speedup --- only try this after you
        #               have gotten a 10x speedup by completing the above changes and
        #               optimizing the other functions in this file)
        #
        # Hint #1: Is there a step which can be taken out of the 'for' loop?
        #
        # Hint #2: This code calculates the cosine distance between the given row's Sentence
        # and the Sentence_with_Target all the rows in MASTER_FILE.
        # This is repeated for each 'row' in SENTENCE_DB_FILE.
        # In first iteration, you already calculate the cosine distance of
        # "I go to school because I want to get a good [education]."
        # and all the rows in the MASTER_FILE
        # and that includes "I go to school because I want to get a good [education]."
        # This is repeated in 2nd iteration for "I go to school because I want to get a good [education].".
        #
        # Can you cache (store) these calculations for future iterations?
        # What would be the best data structure for caching?
        # Try to further optimize the code using a cache
        # -------------------------------------------------------------------------

    '''

    # find alternate similar sentence using document distance
    similar_sentence = None
    for record in get_csv_rows(MASTER_FILE):
        # record is a row in MASTER_FILE

        if record['SentID_GM'] == row['SentID_GM']:
            # ignore the same sentence
            continue
# conditional statement saying if the masterfile and the sentenceDB file are equivalent then continue in the function
        # get frequency mapping for row['Sentence']
        row_word_list = get_words_from_string(row['Sentence'])
        row_freq_mapping = count_frequency(row_word_list)
        # setting variables equal to functions that are defined in the docdist1.py file that will then be able to be
        # called

        # get frequency mapping for record['Sentence_with_Target']
        record_word_list = get_words_from_string(record['Sentence_with_Target'])
        record_freq_mapping = count_frequency(record_word_list)
        # setting variables equal to functions that are defined in the docdist1.py file that will then be able to be
        # called

        distance = vector_angle(row_freq_mapping, record_freq_mapping)
        # calculating the distance of each vector angle by calling the variables that refer to functions in the
        # docdist1.py file
        if 0 < distance < 0.75:
            # conditional: if the distance value is between 0 and .75 then it's true and one will continue
            if (not similar_sentence) or (distance < similar_sentence['distance']):
                # if the value is not none or the value of the distance is less than the value of
                # similar_sentence['distance']
                similar_sentence = {
                    'distance': distance,
                    'Sentence_with_Target': record['Sentence_with_Target'],
                    'SentID_GM': record['SentID_GM']
                }
# Then continue and set this dictionary keys of 'distance', 'sentence_with_target', and 'SentID_GM' equal to the
                #  values of distance, record['Sentence_with_Target'],and record['SentID_GM']
    if similar_sentence and similar_sentence['SentID_GM'] != row.get('SimilarTo_SentID_GM'):
        row['Alternate_SimilarTo_SentID_GM']  = similar_sentence['SentID_GM']
        row['Alternate_SimilarTo_Sentence']  = similar_sentence['Sentence_with_Target']
# if similar_sentence and similar_sentence['SentID_GM] are not equal to row.get('SimilarTo_SentID_GM')
#Then set the values on the left equal to the values on the right so that they are the same values now

def find_unique_targets(row):
    '''
        This steps finds [target] word in "SimilarTo_Sentence" and "Alternate_SimilarTo_Sentence",
        selects only unique target word(s), and saves it in `row['SimilarTo_Targets']`

        # -------------------------------------------------------------------------
        # Implement a better way to find unique target words,
        # without looping through the words
        #
        # Ask yourself:
        # -------------
        #   - Can you use regular expressions to do this?
        #   - What is the data structure that stores only unique values?
        #     Can it be used here instead of checking "if target not in targets:"?
        #     Try searching the web for "python get unique values from a list".
        #
        # -------------------------------------------------------------------------

    '''

    # find unique targets from similar sentences
    targets = []
    # setting an empty list named target
    for key in ('SimilarTo_Sentence', 'Alternate_SimilarTo_Sentence'):
        for word in row.get(key, '').split():
            if word.startswith('[') and word.endswith(']'):
                # using a conditional to see if the word starts with '[' and ends with ']'
                target = word[1:-1]
                #if the above is true then setting the target = to the key word by getting rid of the brackets
                if target not in targets:
                    targets += [target]
                    #if the word set equal to target is not in the list targets then adding target to the list targets

            elif word.startswith('[') and word.endswith('].'):
                target = word[1:-2]
                if target not in targets:
                    targets += [target]
                    # target is now set equal to the word getting rid of the front '[' and the '].'
                    # Then if target is not in targets the  list it is then adding the string target to targets

    row['SimilarTo_Targets'] = ','.join(targets)
# setting the row['SimilarTo_Targets'] and making them one string while also adding a ',' in between each word


def write_output_file(output):
    '''Write output into a new CSV file. Uses the OUTPUT_FILE variable to determine the filename.'''
    global OUTPUT_FILE
    with open(OUTPUT_FILE, 'w', newline='') as output_file_obj:
        sentence_db_writer = csv.DictWriter(output_file_obj,
                                fieldnames=["SentID_GM", "Sentence", "Targ", "Sentence_With_Blank",
                                        "SimilarTo_Sentence", "SimilarTo_SentID_GM",
                                        "Alternate_SimilarTo_Sentence", "Alternate_SimilarTo_SentID_GM",
                                        "SimilarTo_Targets"],
                                extrasaction="ignore", delimiter=",", quotechar='"')

        sentence_db_writer.writeheader()

        for row in output:
            sentence_db_writer.writerow(row)


if __name__ == '__main__':
    profile.run('main()')
    # main()