import csv
import logging
from collections import defaultdict
import json
import os
class ConfigLoader:
    @staticmethod
    def load(config_file):
        try:
            with open(config_file, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            logging.error(f"Configuration file {config_file} not found.")
            raise
        except json.JSONDecodeError:
            logging.error(f"Error decoding the configuration file {config_file}.")
            raise
class BaseParser:
    def __init__(self, lookup_file, flow_log_file):
        self.lookup_file = lookup_file
        self.flow_log_file = flow_log_file
        self.lookup_dict = {}
        self.tag_count = defaultdict(int)
        self.port_protocol_count = defaultdict(int)
    def load_lookup_table(self):
        raise NotImplementedError
    def parse_log(self):
        raise NotImplementedError
    def write_output(self, output_file):
        raise NotImplementedError
class FlowLogParser(BaseParser):
    def load_lookup_table(self):
        """Load the lookup table from a CSV file."""
        try:
            with open(self.lookup_file, 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    key = (row['dstport'].strip().lower(), row['protocol'].strip().lower())
                    self.lookup_dict[key] = row['tag'].strip()
        except FileNotFoundError:
            logging.error(f"Lookup file {self.lookup_file} not found.")
            raise
        except KeyError as e:
            logging.error(f"Missing expected column in the lookup file: {e}")
            raise
        except Exception as e:
            logging.error(f"An error occurred while loading the lookup table: {e}")
            raise
    def parse_log(self):
        """Parse the flow log file and apply tags based on the lookup table."""
        try:
            with open(self.flow_log_file, 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    dstport = row['dstport'].strip().lower()
                    protocol = row['protocol'].strip().lower()
                    key = (dstport, protocol)
                    # Increment port/protocol combination count
                    self.port_protocol_count[key] += 1
                    # Tag matching
                    tag = self.lookup_dict.get(key, "Untagged")
                    self.tag_count[tag] += 1
        except FileNotFoundError:
            logging.error(f"Flow log file {self.flow_log_file} not found.")
            raise
        except KeyError as e:
            logging.error(f"Missing expected column in the flow log file: {e}")
            raise
        except Exception as e:
            logging.error(f"An error occurred while parsing the flow log: {e}")
            raise
    def write_output(self, output_file):
        """Write the output to a file."""
        try:
            with open(output_file, 'w') as file:
                file.write("Tag Counts:\n")
                file.write("Tag            Count\n")
                for tag, count in sorted(self.tag_count.items()):
                    file.write(f"{tag:<15} {count}\n")
                file.write("\nPort/Protocol Combination Counts:\n")
                file.write("Port       Protocol  Count\n")
                for (port, protocol), count in sorted(self.port_protocol_count.items()):
                    file.write(f"{port:<10} {protocol:<10} {count}\n")
        except IOError as e:
            logging.error(f"Error writing output file {output_file}: {e}")
            raise
def main():
    # Load configuration
    config = ConfigLoader.load('config.json')
    # Initialize parser
    parser = FlowLogParser(config['lookup_file'], config['flow_log_file'])
    # Process files
    parser.load_lookup_table()
    parser.parse_log()
    parser.write_output(config['output_file'])
    print(f"Output written to {config['output_file']}")
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        main()
    except Exception as e:
        logging.error(f"An error occurred: {e}")
