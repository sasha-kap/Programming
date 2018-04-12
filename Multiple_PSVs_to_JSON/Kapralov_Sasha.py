
# coding: utf-8

# Purpose of code:
# 1) Produce a series of JSONs, one per patient, representing that patient's complete health record
# (demographic information and a list of events)
# 2) Compute statistics on the data:
#     a) Total number of valid patients
#     b) Maximum/Minimun/Median length of patient timelines in days
#     c) Count of males and females
#     d) Maximum/Minimum/Median age of patient as calculated between birthdate andlast event in timeline
# 
# Input:
# 1) demo.psv (contains patient demographics)
# 2) events.psv (contains dates and medical events in an individual patient's timeline)
# 
# Output:
# 1) patients.json (contains a series of JSONs with patients' complete health records)
# 2) Print-out of statistics on the eligible patient population
# 
# Program logic:
# 1) To include only patients who have demographic information, the list of patient_id's in the demographics table is
# used as the master list of patients for whom events information is located and added.
# 2) If a patient's record is missing either gender or age, that patient is excluded.
# 3) To include only patients who have at least one event with complete information (date, code, system) and only events
# that meet the same completeness criteria, a dictionary of valid events is created and then patients are excluded if
# they are not found in that dictionary.  If they are found, their valid event information is added to the demographics
# information.

# In[1]:

import csv
import json
from collections import defaultdict
from datetime import datetime
import sys


# ### PART 1: CREATION OF JSON

# In[2]:

#first, check that there are no duplicate patient_id values in the demographics table
#also, generate master list of patient_ids from demographics table for later use
all_ids = [] #list to contain master list of patient_ids from demographics table
duplicate_ids = []
with open('demo.psv', 'rb') as demo:
    next(demo) #skip header row
    for line in demo:
        columns = line.strip().split('|')
        if columns[0] not in all_ids:
            all_ids.append(columns[0])
        else:
            duplicate_ids.append(columns[0])
if len(duplicate_ids) == 0:
    print "Check completed: No duplicate IDs in demographics table"
else:
    print "Review and reconcile duplicate patient_ids in demographics table before proceeding"
    sys.exit()


# In[3]:

#create separate dictionaries of birthdays and genders from demographics table
with open('demo.psv') as f:
    next(f) #skip header row
    r = csv.reader(f, delimiter='|')
    gender_dict = {row[0]: row[2] for row in r}

with open('demo.psv') as f:
    next(f) #skip header row
    r = csv.reader(f, delimiter='|')
    dob_dict = {row[0]: row[1] for row in r}


# In[4]:

#create a list of patient-event lists
with open('events.psv') as f:
    next(f) #skip header row
    events_list = list(csv.reader(f, delimiter='|'))
events_list[:5]


# In[5]:

#check for any events that are missing a code, date or ICD system and remove them
events_list = [event for event in events_list if (event[1] != '') & (event[2] != '') & (event[3] != '')]
events_list[:5]


# In[6]:

#convert above list of lists to a dictionary with unique patient_id keys
events_dict = defaultdict(list)
for event in events_list:
    events_dict[event[0]] += event[1:]


# In[7]:

#create dictionary to hold demographic and event information for all eligible patients and events
complete_dict = {}

#loop over patients in demographics table and generate their dictionary of demographic and event information
for patient_id in all_ids:
    #check that both birth date and gender are present and that patient has at least one event with code
    #exit loop if not, without creating patient dictionary, and continue to next patient
    if (dob_dict[patient_id] == '') | (gender_dict[patient_id] == '') | (patient_id not in events_dict):
        continue
    #create dictionary and populate it with demographic and event information for patient
    patient_dict = {}
    patient_dict['birth date'] = dob_dict[patient_id]
    patient_dict['gender'] = gender_dict[patient_id]
    #create empty list of events for single patient
    patient_dict['events'] = []
    #look up patient_id in events_dict and loop over 3-element groups of info for all events for this patient
    #to create separate event dictionaries
    for event_counter in range(len(events_dict[patient_id]) / 3):
        indiv_event_dict = {}
        indiv_event_dict['date'] = events_dict[patient_id][event_counter * 3]
        if events_dict[patient_id][event_counter * 3 + 1] == '9':
            indiv_event_dict['system'] = 'http://hl7.org/fhir/sid/icd-9-cm'
        elif events_dict[patient_id][event_counter * 3 + 1] == '10':
            indiv_event_dict['system'] = 'http://hl7.org/fhir/sid/icd-10'
        indiv_event_dict['code'] = events_dict[patient_id][event_counter * 3 + 2]
        #add this indiv_event_dict to events list
        patient_dict['events'].append(indiv_event_dict)
    #add this patient to the complete dictionary of all patients
    complete_dict[patient_id] = patient_dict


# In[8]:

#print an example of one patient record in the complete dictionary
complete_dict['id-743']


# In[9]:

#convert complete dictionary to JSON file
with open('patients.json', 'a') as outfile:
    outfile.write(json.dumps(complete_dict, sort_keys=True, indent=4))


# ### PART 2: STATISTICS 

# In[10]:

#calculate total number of valid patients
print "Total number of valid patients is {}.".format(len(complete_dict))


# In[11]:

#calculate counts of males and females
male_ct = 0
female_ct = 0
other_gender_ct = 0
for patient_dict in complete_dict.values():
    if patient_dict['gender'] == 'M':
        male_ct += 1
    elif patient_dict['gender'] == 'F':
        female_ct += 1
    else:
        other_gender_ct += 1
print "Number of males is {} and number of females is {}.".format(male_ct, female_ct)
print "There is/are {} patients with another recorded gender.".format(other_gender_ct)


# In[12]:

#create a list of all lengths of patient timelines
#also create a list of all ages as of the last event in timeline
timelines_in_days = []
ages = []
for patient_dict in complete_dict.values():
    for ctr, event in enumerate(patient_dict['events']):
        event_dt = datetime.strptime(event['date'], '%Y-%m-%d')
        if ctr == 0:
            earliest_dt = event_dt
            latest_dt = event_dt
        else:
            if event_dt < earliest_dt:
                earliest_dt = event_dt
            elif event_dt > latest_dt:
                latest_dt = event_dt
        #at last event, calculate days contained between earliest and latest days and patient's age
        if ctr == len(patient_dict['events']) - 1:
            days = (latest_dt - earliest_dt).days + 1
            timelines_in_days.append(days)
            birth_dt = datetime.strptime(patient_dict['birth date'], '%Y-%m-%d')
            age = latest_dt.year - birth_dt.year - ((latest_dt.month, latest_dt.day) < (birth_dt.month, birth_dt.day))
            ages.append(age)
timelines_in_days[:10]


# In[13]:

ages[:10]


# In[14]:

#compute minimum and maximum length of patient timelines in days
timelines_sorted = sorted(timelines_in_days)
min_length = timelines_sorted[0]
max_length = timelines_sorted[-1]
print "Minumum length of patient timelines is {} day(s) and maximum length is {} day(s).".format(min_length, max_length)


# In[15]:

#compute median length of patient timelines in days
if len(timelines_sorted) % 2 == 1:
    median_length = timelines_sorted[len(timelines_sorted)//2]
else:
    median_length = sum(timelines_sorted[len(timelines_sorted)//2-1:len(timelines_sorted)//2+1])/2
print "Median length of patient timelines is {} day(s).".format(median_length)


# In[16]:

#Maximum/Minimum/Median age of patient (in years) as calculated between birthdate and last event in timeline
ages_sorted = sorted(ages)
min_age = ages_sorted[0]
max_age = ages_sorted[-1]

if len(ages_sorted) % 2 == 1:
    median_age = ages_sorted[len(ages_sorted)//2]
else:
    median_age = sum(ages_sorted[len(ages_sorted)//2-1:len(ages_sorted)//2+1])/2

print "Minimum age is {} years, maximum age is {} years, and median age is {} years.".format(min_age, max_age, median_age)

