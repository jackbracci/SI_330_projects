import csv
import profile

# Here, we are reusing the document distance code
from docdist_dict import (get_words_from_string, count_frequency, vector_angle) #changed imported file from docdist1 to docdist_dict
'''Change number 5:
 1. changed imported file from docdist1 to docdist_dist
 2. Before: 134.380, After: 9.223
 3. Reduction Factor: 134.380/9.223 = 14.5700'''


# As a convention, "constant" variable names are usually written in all-caps
OUTPUT_FILE = 'Sentence_Database_With_ID.csv'

MASTER_FILE = 'Sentences_Table_MasterList.csv'
SENTENCE_DB_FILE = 'Sentence_Database_Without_ID.csv'
# MASTER_FILE = 'Sentences_Table_MasterList.csv'
# SENTENCE_DB_FILE = 'Sentence_Database_Without_ID.csv'

def get_csv_rows(filename):
    '''Read the CSV file using DictReader and then append all rows in a list'''
    with open(filename, 'r', newline='') as input_file:
        reader = csv.DictReader(input_file, delimiter=',', quotechar='"')

        data = []
        for row in reader:
            data.append(row)

        return data

def main(): #set up the main logic of the program
    global MASTER_FILE, SENTENCE_DB_FILE

    # we will be collecting each row of the output file in this list
    output = [] #list of dictionaries that represent rows
    row_count = 0

    # looping through the SENTENCE_DB_FILE to process each row
    for row in get_csv_rows(SENTENCE_DB_FILE):
        set_sentence_id(row) #adding missing id to row
        replace_target_with_blank(row) #replacing target word in sentence with XXXXX

        if row['SentID_GM'] != 'NA': #if the related id cannot be found find similar sentence
            lookup_similar_id(row) #trying to find the id of a similar sentence 
            find_alternate_sentence(row) #fidning an alternate similar sentence 
            find_unique_targets(row) #looks at the overlap of the 2 similar sentences 

        output.append(row)
        row_count += 1
        print(row_count)

    write_output_file(output)

'''Change Number: 1
1. outdented this line so the cvs file is only written once, not constantly
2.Before: 145.950 seconds, After: 142.025
3.Reduction Factor: 145.950/142.025 = 1.027'''

dic_4_set_sentence_id = {} #creating an empty dictionary
for record in get_csv_rows(MASTER_FILE): #iterating through the list of rows for the Master File
    dic_4_set_sentence_id[record['Sentence_with_Target'].strip()] = record #setting the key to Sentence_with_Target, and the values are dictionaries that represent the entire row

'''Change Number: 2
1. creating an emtpy dictionary that is indexed with Sentence_with_Target in order to save time looking for a sentence
2. Before: 142.025, After: 139.149
3. Reduction Factor: 142.025/139.149 = 1.0207
'''
def set_sentence_id(row): #the input format will be a dictionary, the output will be row modified with the correct ID
    '''
        If you look at the SENTENCE_DB_FILE, each row has a Sentence with a missing SentID_GM
        SentID_GM can be found in the MASTER_FILE
        So, we use the MASTER_FILE data to find SentID_GM for each Sentence

        # -------------------------------------------------------------------------
        # Implement a better way to "lookup" SentID_GM,
        # without looping through each row again and again
        #
        # Ask yourself:
        # -------------
        #   - Is "list" the best data structure for "lookup / search"?
        #   - What is the 'type' of running time for the current implementation?
        #     Is it linear or quadratic?
        #
        # -------------------------------------------------------------------------

    '''
    searchkey = row['Sentence'].strip() #creating a varaible with the sentence we want to search for
    if searchkey in dic_4_set_sentence_id: #checking to see if the key is within the dictionary
        row['SentID_GM'] = dic_4_set_sentence_id[searchkey]['SentID_GM'] #modifies the row with the correct SentID_GM
    else:
        row['SentID_GM'] = 'NA' #if a matching sentence isnt found, set SENTID_GM value to NA

'''Change Number: 2 cont.'''
"""for record in get_csv_rows(MASTER_FILE): #record is a dictionary that represents row in the masterfile
        # record is a row in MASTER_FILE
        print (type(get_csv_rows(MASTER_FILE)))
        if record['Sentence_with_Target'].strip() == row['Sentence'].strip(): #this line checks to see if the sentences are the same
            # found a matching sentence!
            row['SentID_GM'] = record['SentID_GM'] #modifies the row with the correct SentID_GM
            break

        else:
            # the default value
            row['SentID_GM'] = 'NA' #if a matching sentence isnt found, set SENTID_GM value to NA"""


def replace_target_with_blank(row): #the input format will be a dictionary, the output will be row modified with the replace target word in the Sentence_With_Blank
    '''
        Each row in SENTENCE_DB_FILE has a "Target" word like "[education]".
        In this function, we replace the target word with "XXXXX", and
        store its value in "Sentence_With_Blank" column

        # -------------------------------------------------------------------------
        # Implement a better way to replace the Target word with XXXXX,
        # without looping through the words
        #
        # Ask yourself:
        # -------------
        #   - Is there an inbuilt python function,
        #     that can be used to substitute a word with another word?
        #
        # -------------------------------------------------------------------------

    '''
    row['Sentence_With_Blank'] = row['Sentence'].replace('[' + row['Targ'] + ']','XXXXX')  # replacing the target with XXXXX
    """new_words = [] #list of strings

    # Here, we split the sentence into words and loop through it till we find the target
    for word in row['Sentence'].split():
        if word[0]=='[' and (word[-1]==']' or word[-2:]=='].') and word[1:-1]==row['Targ']: #looking for target word by indentyfying brackets in the word regardless of where the word is within the sentence  
            new_words.append('XXXXX') #changing the target word to XXXXX
        else:
            new_words.append(word) #if the target word cannot be identified add that word to the list

    row['Sentence_With_Blank'] = ' '.join(new_words)""" #recreating the sentence with the replaced target word as XXXXX

'''Change Number: 3
1.Utilizing the built in .replace method from python
2. Before: 139.149, After: 140.139
3. Reduction Factor: 139.149/140.149 = .9929 '''

dic_4_lookup_similar_id = {} #creating an empty dictionary
for record in get_csv_rows(MASTER_FILE): #iterating through the list of rows for the Master File
    dic_4_lookup_similar_id[record['SentID_GM']] = record #setting the key to Sentence_with_Target, and the values are dictionar


def lookup_similar_id(row): #the input format will be a dictionary, the output will be row modified with the similar sentence and the corresponding ID
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
    searchkey = row['SentID_GM']
    if searchkey in dic_4_lookup_similar_id:
        similar_to = dic_4_lookup_similar_id[searchkey]['SimilarTo_SentID_GM']

    if similar_to is not None:
        if similar_to in dic_4_lookup_similar_id:
            row['SimilarTo_Sentence'] = dic_4_lookup_similar_id[similar_to]['Sentence_with_Target']
            row['SimilarTo_SentID_GM'] = similar_to

'''CHANGE NUMBER: 4
1. Creating an empty dictionary for indexing rather than looking through everything
2. Before: 140.139, After:134.380
3.Reduction Factor: 140.139/134.380 = 1.0429'''


"""
    similar_to = None 
    # Here we get SimilarTo_SentID_GM for this row's SentID_GM using the MASTER_FILE
    for record in get_csv_rows(MASTER_FILE): #record is a dictionary that represents row in the masterfile
        # record is a row in MASTER_FILE
        if record['SentID_GM'] == row['SentID_GM']: 
            # found a match
            similar_to = record['SimilarTo_SentID_GM']
            break

    # then we find the similar sentence from the MASTER_FILE
    if similar_to is not None:
        for record in get_csv_rows(MASTER_FILE):
            # record is a row in MASTER_FILE
            if record['SentID_GM'] == similar_to:
                row['SimilarTo_Sentence'] = record['Sentence_with_Target']
                row['SimilarTo_SentID_GM'] = similar_to
                break"""

def find_alternate_sentence(row): #the input format will be a dictionary, the output will be row modified with the alternate sentence and the corresponding ID
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

        # get frequency mapping for row['Sentence']
        row_word_list = get_words_from_string(row['Sentence']) #list of strings 
        row_freq_mapping = count_frequency(row_word_list) #list of lists where the inner list contains a word and then its count

        # get frequency mapping for record['Sentence_with_Target']
        record_word_list = get_words_from_string(record['Sentence_with_Target']) #list of strings
        record_freq_mapping = count_frequency(record_word_list) #list of lists where the inner list contains a word and then its count

        distance = vector_angle(row_freq_mapping, record_freq_mapping) #float 
        if 0 < distance < 0.75: #checking to see if your distance variable can be considered similar
            if (not similar_sentence) or (distance < similar_sentence['distance']): #checking to see what identified sentence is more similar 
                similar_sentence = { #Creating a new dictionary with the more newly identified more similar sentence 
                    'distance': distance,
                    'Sentence_with_Target': record['Sentence_with_Target'],
                    'SentID_GM': record['SentID_GM']
                }

    if similar_sentence and similar_sentence['SentID_GM'] != row.get('SimilarTo_SentID_GM'): #if the newly found sentence is NOT identical to the origincal sentence 
        row['Alternate_SimilarTo_SentID_GM']  = similar_sentence['SentID_GM']
        row['Alternate_SimilarTo_Sentence']  = similar_sentence['Sentence_with_Target']


def find_unique_targets(row): #the input format will be a dictionary, the output will be row modified with both similar sentence target words
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
    targets = [] #list of target words
    for key in ('SimilarTo_Sentence', 'Alternate_SimilarTo_Sentence'): #running the same logic for each similar sentence 
        for word in row.get(key, '').split(): #pull each word string from the sentence stored at that key
            if word.startswith('[') and word.endswith(']'): #finding the target word withing the list of strings 
                target = word[1:-1] #finding the target word withing the list of strings 
                if target not in targets: #if the target word is unique append the new word to the target list
                    targets += [target]

            elif word.startswith('[') and word.endswith('].'): #finding when the target word is at the end of the sentence 
                target = word[1:-2] #finding when the target word is at the end of the sentence
                if target not in targets: #if the target word is unique append the new word to the target list
                    targets += [target]

    row['SimilarTo_Targets'] = ','.join(targets) #recreating the target word list with commas seperating the words




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
    profile.run("main()")
