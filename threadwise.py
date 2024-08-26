import json
import os
from graphviz import Digraph

# Load the JSON log data from a file
with open("log_data.json", "r") as f:
    log_data = json.load(f)
extra_nodes={}
process_subgraph_color='#89E0CB'
thread_subgraph_color='white'
process_node_color='#6EADE0'
thread_node_color='#6EE0B6'
node_color='#C2E096'

# Create a new directed graph
dot = Digraph()

# Set global attributes for spacing and layout
dot.attr(rankdir='LR', nodesep='1.0', ranksep='1.5')

node_to_thread_map = {}
start = False

# Group logs by ProcessID and ThreadID
process_thread_groups = {}
for log in log_data:
    process_id = log['ProcessID']
    thread_id = log['ThreadID']
    if process_id not in process_thread_groups:
        process_thread_groups[process_id] = {}
    if thread_id not in process_thread_groups[process_id]:
        process_thread_groups[process_id][thread_id] = []
    process_thread_groups[process_id][thread_id].append(log)

# Iterate through each process and thread group to create subgraphs
process_graphs_list = []
created_node_ids = []
for process_id, threads in process_thread_groups.items():
    with dot.subgraph(name=f'cluster_process_{process_id}') as process_subgraph:
        process_subgraph.attr(
            label=f'Process {process_id}',
            color='blue',
            style='filled',
            fillcolor=process_subgraph_color,
            rankdir='LR',
            pad='25',
            margin='25'  # Add margin around the process cluster

        )
        process_graphs_list.append(process_subgraph)

        for thread_id, logs in threads.items():
            if logs[0]['Callee_func'] == '<module>':
                displayname = f'MainThread {thread_id}'
            else:
                displayname = f'Thread {thread_id}'
            with process_subgraph.subgraph(name=f'cluster_thread_{thread_id}') as thread_subgraph:
                thread_subgraph.attr(
                    label=displayname,
                    color='green',
                    style='filled',
                    fillcolor=thread_subgraph_color,
                    rankdir='TB',
                    margin='25'
                      # Add margin around the thread cluster
                )

                # For each log, create a node and add edges
                for log in logs:
                    node_counter = log['timestamp'].split(' ')[1]
                    event_type = log['EventType']
                    timestamp = log['timestamp']
                    func_name = log['Callee_func'].replace('<', '').replace('>', '')
                    caller_func_name = log['Caller_func'].replace('<', '').replace('>', '')
                    callee_id = f"{func_name}-{log['Callee_id']}"
                    caller_id = f"{caller_func_name}-{log['Caller_id']}"
                    callee_class = log['Callee_class']
                    print('log',log)
                    filename = log['Callee_name'].split(os.path.sep)[-1]

                    # Node ID for internal use
                    node_id = f"{callee_id}"
                    label = f"""<<FONT POINT-SIZE="16"><B>{func_name}(  )</B></FONT><BR/><FONT POINT-SIZE="14">Class:{callee_class}</FONT><BR/><FONT POINT-SIZE="10">stack-id:{callee_id}</FONT><BR/><FONT POINT-SIZE="10">File:{filename}</FONT>>"""

                    # Add the function call node
                    if True:
                        created_node_ids.append(node_id)
                        thread_subgraph.node(node_id, label=label, style='filled',shape='rectangle',fillcolor=node_color)
                        if not start:
                            thread_subgraph.node('1', label='START', shape='doublecircle',style='filled',fillcolor='#00E04A')
                            start = True
                            dot.edge('1', node_id, weight='1', constraint='false')

                    created_threads_count = 0

                    if event_type == 'call':
                        # Add edge from Caller_id to Callee_id
                        previous_node_id_call = f'{caller_id}'
                        if caller_id != callee_id:
                            thread_subgraph.edge(
                                previous_node_id_call,
                                node_id,
                                label=f"IN-{node_counter}",
                                color='green'
                            )
                    elif event_type == 'exit':
                        # Add edge from Callee_id to Caller_id
                        previous_node_id_exit = f'{caller_id}'
                        if caller_id != callee_id and previous_node_id_exit in created_node_ids:
                            thread_subgraph.edge(
                                node_id,
                                previous_node_id_exit,
                                label=f"Out-{node_counter}",
                                style='dotted',
                                color='red'
                            )

                    # Handle thread and process creation
                    created_thread_ids = log.get("Created_Thread_IDs", [])
                    created_process_ids = log.get("Created_Process_IDs", [])

                    # Add edges from the current node to the created threads and processes
                    for created_thread_id in created_thread_ids:
                        timestamp_inner = created_thread_id['timestamp'].split(' ')[-1]
                        label_text = f'Cluster_Thread {created_thread_id["ID"]}'
                        tmpid = f'Cluster_Thread {created_thread_id["ID"]}'
                        thread_subgraph.node(tmpid, label=label_text, shape='parallelogram', style='filled', fillcolor=thread_node_color, color='green')
                        node_to_thread_map[created_thread_id["ID"]] = f'Thread {created_thread_id["ID"]}'
                        thread_subgraph.edge(
                            node_id,
                            tmpid,
                            label=f"Creates Thread {created_thread_id['ID']}-{timestamp_inner}",
                            color='blue',
                            style='dashed',
                            shape='circle'
                        )

                    for created_process_id in created_process_ids:
                        timestamp_inner1 = created_process_id['timestamp'].split(' ')[-1]
                        label_text = f'Cluster_Process {created_process_id["ID"]}'
                        tmpid = f'Cluster_Process {created_process_id["ID"]}'
                        thread_subgraph.node(tmpid, label=label_text, shape='parallelogram', style='filled', fillcolor=process_node_color, color='blue')
                        node_to_thread_map[tmpid] = f'Process {created_process_id["ID"]}'
                        thread_subgraph.edge(
                            node_id,
                            tmpid,
                            label=f"Creates Process {created_process_id['ID']}-{timestamp_inner1}",
                            color='orange',
                            style='dashed'
                        )

# Render the graph
dot.render('threaded_process_workflow_with_creation_vertical_horizontal', format='pdf', view=True)
