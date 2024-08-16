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
