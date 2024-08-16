# Flow Log Parser
This program parses a flow log file and maps each row to a tag based on a lookup table. The tags are defined by the combination of `dstport` and `protocol`.
## Assumptions
The lookup table and flow log files are well-formed CSV files.
Protocol matching is case-insensitive.
If a port/protocol combination isn't found in the lookup table, it is tagged as `Untagged`.
## Requirements
Python 3.x (no additional libraries required)
## How to Run the Program
Clone this repository
Place your lookup_table.csv and flow_log.csv in same directory as script 
Run the script : python flow_log_parser.py
Output will be saved to output.txt
#Testing 
Sample lookup_table.csv and flow_log.csv is provided for testing. And  various use cases and edge 
cases have been tested along with tests mentioned in the file 
#Notes
This program avoids using non default Python libraraies to ensure compatibilitywith most local machines 
## Time and Space Complexity
### Time Complexity
**Loading Lookup Table:** `O(n)` where `n` is the number of rows in the lookup table.
**Parsing Flow Log:** `O(m)` where `m` is the number of rows in the flow log.
**Writing Output:** `O(p + q)` where `p` is the number of unique tags, and `q` is the number of unique port/protocol combinations.
The overall time complexity is `O(n + m + p + q)`, dominated by the size of the flow log file (`m`).
### Space Complexity
**Lookup Dictionary:** `O(n)` for storing `n` entries from the lookup table.
**Counting Dictionaries:** `O(m)` for storing counts based on `m` rows in the flow log.
The overall space complexity is `O(n + m)`.
7:32
## Running Tests
To run the provided test cases, use the following commands:

Place the `test_flow_log_parser.py` script in the same directory as `flow_log_parser.py`.
Run the test script:
    ```bash
    python test_flow_log_parser.py
    ```
The script will execute multiple test cases and output the result of each.
