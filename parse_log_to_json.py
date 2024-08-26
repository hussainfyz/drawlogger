import json
import os,re


def initialize_json(log_file, json_file):
    log_data = []

    # Check if JSON file already exists
    if not os.path.exists(json_file):
        with open(log_file, 'r') as file:
            for line in file:
                if (line.find('call')!=-1 or line.find('exit')!=-1):
                    log_entry = parse_log_line(line)
                    log_data.append(log_entry)

        # Write initial JSON data to the file
        with open(json_file, 'w') as outfile:
            json.dump(log_data, outfile, indent=4)

def parse_log_line_for_creator_events(line):
    # Example parsing logic, should be adjusted based on actual log format
    log_entry=extract_value(line,'xyz')
    """
    log_entry = {
        "EventType": extract_value(line, "EventType"),
        "ProcessName": extract_value(line, "CreatorProcessName"),
        "ProcessID": extract_value(line, "ProcessID"),
        "ThreadID": extract_value(line, "ThreadID"),
        "Caller_name": extract_value(line, "CreatorThreadName"),
        "Caller_func": extract_value(line, "Creator_func"),
        "Caller_id": extract_value(line, "Creator_id"),
        "Caller_class": extract_value(line, "Created_tp_ID")
    }
    """
    return log_entry

def parse_log_line(line):
    log_entry = extract_value(line, 'xyz')
    """
    # Example parsing logic, should be adjusted based on actual log format
    log_entry = {
        "EventType": extract_value(line, "EventType"),
        "ProcessName": extract_value(line, "ProcessName"),
        "ProcessID": extract_value(line, "ProcessID"),
        "ThreadName": extract_value(line, "ThreadName"),
        "ThreadID": extract_value(line, "ThreadID"),
        "Caller_name": extract_value(line, "Caller_name"),
        "Caller_func": extract_value(line, "Caller_func"),
        "Caller_id": extract_value(line, "Caller_id"),
        "Caller_class": extract_value(line, "Caller_class"),
        "Callee_name": extract_value(line, "Callee_name"),
        "Callee_func": extract_value(line, "Callee_func"),
        "Callee_id": extract_value(line, "Callee_id"),
        "Callee_class": extract_value(line, "Callee_class")
    }
    """
    return log_entry


def extract_value(line,dummykey):
    # Split the line into timestamp and the rest of the data
    parts = line.split(' - ', 1)

    # Initialize a dictionary to hold the extracted values
    data = {}

    # Add the timestamp to the dictionary
    data['timestamp'] = parts[0].strip()

    # The remaining part contains key-value pairs separated by commas
    key_value_pairs = parts[1].split(',')

    # Iterate over the key-value pairs and add them to the dictionary
    for pair in key_value_pairs:
        key, value = pair.split(':', 1)
        data[key.strip()] = value.strip()

    return data


import json

import json
from collections import defaultdict


def detect_loops_and_add_counts(input_file, output_file):
    with open(input_file, 'r') as f:
        logs = json.load(f)

    # Dictionary to store the count of each (caller, callee) pair
    call_counts = defaultdict(int)
    unique_logs = []
    seen = set()

    # Process logs to detect duplicates and count calls
    for log in logs:
        call_key = (log['Caller_id'], log['Callee_id'])
        if log['EventType'] == 'call':
            call_counts[call_key] += 1
        log_id = (log['ProcessID'], log['ThreadID'], log['Caller_lineno'], log['Callee_lineno'])
        if log_id not in seen:
            seen.add(log_id)
            unique_logs.append(log)

    # Update logs with call counts
    updated_logs = []
    for log in unique_logs:
        if log['EventType'] == 'call':
            call_key = (log['Caller_id'], log['Callee_id'])
            log['Call_count'] = call_counts[call_key]
        else:
            log['Call_count'] = 1  # For 'exit' events, set Call_count to 1
        updated_logs.append(log)

    # Write updated logs to a new file
    with open(output_file, 'w') as f:
        json.dump(updated_logs, f, indent=4)


# Usage



def detect_loops_and_add_counts_old(input_file, output_file):
    # Load the JSON data
    with open(input_file, "r") as f:
        log_data = json.load(f)

    # To store the call relationships
    call_relations = {}

    # Analyze and collect call relations
    for log in log_data:
        process_id = log['ProcessID']
        thread_id = log['ThreadID']
        caller_id = log['Caller_id']
        callee_id = log['Callee_id']
        caller_lineno = log.get('Caller_lineno', 'unknown')
        callee_lineno = log.get('Callee_lineno', 'unknown')

        # Create a unique identifier for the call
        call_id = (process_id, thread_id,caller_lineno,callee_lineno)

        if call_id not in call_relations:
            call_relations[call_id] = 0

        call_relations[call_id] += 1

    # Add Call_count to each log record
    for log in log_data:
        process_id = log['ProcessID']
        thread_id = log['ThreadID']
        caller_id = log['Caller_id']
        callee_id = log['Callee_id']
        caller_lineno = log.get('Caller_lineno', 'unknown')
        callee_lineno = log.get('Callee_lineno', 'unknown')

        # Create a unique identifier for the call
        call_id = (process_id, thread_id,caller_lineno,callee_lineno)

        # Add Call_count to the log record
        log['Call_count'] = call_relations.get(call_id, 0)

    # Save the modified data to a new JSON file
    with open(output_file, "w") as f:
        json.dump(log_data, f, indent=4)


# Example usage
#input_file = "log_data.json"
#output_file = "log_data_with_counts.json"



def extract_value1(line, key):
    # Example extraction logic based on key; customize based on log format
    start = line.find(key + ": ") + len(key) + 2
    end = line.find(",", start)
    return line[start:end].strip()

def get_creator_events_data(log_file):
        #if not os.path.exists(json_file):
        log_data=[]
        with open(log_file, 'r') as file:
            for line in file:
                if (line.find('Thread_creation')!=-1 or line.find('Process_creation')!=-1):
                    log_entry = parse_log_line_for_creator_events(line)
                    log_data.append(log_entry)
        #print(log_data)
        return log_data
def enrich_json_with_creation_details(log_file,json_file):
    with open(json_file, 'r') as infile:
        log_data = json.load(infile)
    creator_data=get_creator_events_data(log_file)
    temp_creator_list_threads = {}
    temp_creator_list_processes = {}
    print("Creator data")
    print(creator_data)
    for entry1 in creator_data:
        #print(entry)
        #exit()
        if entry1['EventType'] == 'Thread_creation':
            #print(entry)
            creator_id1 = entry1.get('Creator_id')
            if(creator_id1 not in temp_creator_list_threads.keys()):
                t1=[]
                tmp1={}
                tmp1['ID']=entry1['Created_tp_ID']
                tmp1['timestamp']=entry1['timestamp']
                #tmp['Created_Threads'] =tmp1
                t1.append(tmp1)
                temp_creator_list_threads[creator_id1] =t1
            else:
                tmplist=temp_creator_list_threads[creator_id1]
                tmp1={}
                tmp1['ID']=entry1['Created_tp_ID']
                tmp1['timestamp'] = entry1['timestamp']
                tmplist.append(tmp1)
                temp_creator_list_threads[creator_id1]=tmplist

        elif entry1['EventType'] == 'Process_creation':
            creator_id1 = entry1.get('Creator_id')
            if (creator_id1 not in temp_creator_list_processes.keys()):
                tmp1 = []
                t1={}
                t1['ID']=entry1['Created_tp_ID']
                t1['timestamp']=entry1['timestamp']
                tmp1.append(t1)
                # tmp['Created_Threads'] =tmp1
                temp_creator_list_processes[creator_id1] = tmp1
            else:
                tmplist = temp_creator_list_processes[creator_id1]
                t1={}
                t1['ID'] = entry1['Created_tp_ID']
                t1['timestamp'] = entry1['timestamp']
                tmplist.append(t1)
                temp_creator_list_processes[creator_id1] = tmplist

        else:
            continue
        # Iterate over log data to find matching Callee_id
    for one_entry in creator_data:
        print("-------------------")
        print('Parsing entry ')
        print(one_entry)

        creator_id2 = one_entry.get('Creator_id')
        for log_entry in log_data:
            #print(log_entry['Callee_id'],creator_id2,':',log_entry['Callee_func'],one_entry['Creator_func'])
            #if log_entry['Callee_id'] == creator_id2 and log_entry['Callee_func']== one_entry['Creator_func']:
            #print(log_entry['ThreadID'],one_entry['ThreadID'],':',one_entry['Creator_func'],log_entry['Callee_func'])
            print(log_entry)
            if(log_entry['EventType']=='call'):
                if log_entry['Callee_id'] == creator_id2: #or (log_entry['ThreadID']==one_entry['ThreadID'] and one_entry['Creator_func']==log_entry['Callee_func']):
                    print("Found matching ")
                    print(log_entry)
                    print(one_entry)
                    print(temp_creator_list_processes)
                    #exit()
                    if one_entry['EventType'] == 'Thread_creation':
                        log_entry['Created_Thread_IDs'] =temp_creator_list_threads[creator_id2]
                    elif one_entry['EventType'] == 'Process_creation':
                        log_entry['Created_Process_IDs'] =temp_creator_list_processes[creator_id2]
                    #print(log_entry)
                    #exit()
        #exit()

        #exit()
    # Write the enriched data back to the JSON file
    with open(json_file, 'w') as outfile:
        json.dump(log_data, outfile, indent=4)


# Example usage
log_file = 'function_calls.log'
json_file = 'log_data.json'

initialize_json(log_file, json_file)
enrich_json_with_creation_details(log_file,json_file)
#detect_loops_and_add_counts(json_file, 'final.json')