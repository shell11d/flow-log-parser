import os
import subprocess
def run_test(test_name, lookup_data, flow_log_data, expected_output):
    # Create temporary test files
    with open("test_lookup.csv", "w") as lookup_file:
        lookup_file.write(lookup_data)
    with open("test_flow_log.csv", "w") as flow_log_file:
        flow_log_file.write(flow_log_data)
    # Update config.json for testing
    config_data = {
        "lookup_file": "test_lookup.csv",
        "flow_log_file": "test_flow_log.csv",
        "output_file": "test_output.txt"
    }
    with open("config.json", "w") as config_file:
        json.dump(config_data, config_file)
    # Run the parser
    subprocess.run(["python", "flow_log_parser.py"])
    # Compare the result
    with open("test_output.txt", "r") as output_file:
        output_data = output_file.read()
    assert output_data == expected_output, f"Test {test_name} Failed"
    # Clean up
    os.remove("test_lookup.csv")
    os.remove("test_flow_log.csv")
    os.remove("test_output.txt")
    os.remove("config.json")
    print(f"Test {test_name} Passed")
if __name__ == "__main__":
    # Test 1: Basic Matching
    run_test(
        "Basic Matching",
        "dstport,protocol,tag\n25,tcp,sv_P1\n443,tcp,sv_P2\n",
        "dstport,protocol\n25,tcp\n443,tcp\n80,tcp\n",
        """Tag Counts:
Tag            Count
Untagged       1
sv_P1          1
sv_P2          1
Port/Protocol Combination Counts:
Port       Protocol  Count
25         tcp       1
80         tcp       1
443        tcp       1
"""
    )
    # Test 2: Case Insensitivity
    run_test(
        "Case Insensitivity",
        "dstport,protocol,tag\n25,TCP,sv_P1\n443,Tcp,sv_P2\n",
        "dstport,protocol\n25,tcp\n443,tcp\n80,tcp\n",
        """Tag Counts:
Tag            Count
Untagged       1
sv_P1          1
sv_P2          1
Port/Protocol Combination Counts:
Port       Protocol  Count
25         tcp       1
80         tcp       1
443        tcp       1
"""
    )
    # Test 3: No Matches
    run_test(
        "No Matches",
        "dstport,protocol,tag\n25,tcp,sv_P1\n443,tcp,sv_P2\n",
        "dstport,protocol\n80,tcp\n8080,udp\n",
        """Tag Counts:
Tag            Count
Untagged       2
Port/Protocol Combination Counts:
Port       Protocol  Count
80         tcp       1
8080       udp       1
"""
    )
    # Test 4: Empty Lookup Table
    run_test(
        "Empty Lookup Table",
        "dstport,protocol,tag\n",
        "dstport,protocol\n25,tcp\n443,tcp\n80,tcp\n",
        """Tag Counts:
Tag            Count
Untagged       3
Port/Protocol Combination Counts:
Port       Protocol  Count
25         tcp       1
80         tcp       1
443        tcp       1
"""
    )
    # Test 5: Empty Flow Log
    run_test(
        "Empty Flow Log",
        "dstport,protocol,tag\n25,tcp,sv_P1\n443,tcp,sv_P2\n",
        "dstport,protocol\n",
        """Tag Counts:
Tag            Count
Port/Protocol Combination Counts:
Port       Protocol  Count
"""
    )
