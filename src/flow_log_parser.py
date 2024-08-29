import csv
import argparse
import logging
from collections import defaultdict
from datetime import datetime

def load_lookup_table(lookup_file):
    """
    Load the lookup table from the specified file.
    The lookup table maps (dstport, protocol) combinations to tags.
    
    Args:
        lookup_file (str): Path to the lookup table file.
        
    Returns:
        defaultdict: A dict mapping (dstport, protocol) tuples to a list of tags.
    """
    lookup_dict = defaultdict(list)
    with open(lookup_file, mode='r') as file:
        for line in file:
            line = line.strip()  # Remove any leading/trailing whitespace or newlines
            if not line or ',' not in line:
                continue  # Skip empty lines or lines without commas
            # Split the line into dstport, protocol, and tag, and normalize the protocol to lowercase
            dstport, protocol, tag = [item.strip().lower() for item in line.split(',')]
            lookup_dict[(dstport, protocol)].append(tag)  # Map (dstport, protocol) to the tag
    return lookup_dict

def parse_flow_logs(log_file, lookup_dict, verbosity):
    """
    Parse the flow logs and count occurrences of tags and port/protocol combinations.
    
    Args:
        log_file (str): Path to the flow log file.
        lookup_dict (defaultdict): Thee lookup dict mapping (dstport, protocol) to tags.
        verbosity (int): The verbosity level for logging.
        
    Returns:
        tuple: Two dict, one for tag counts and one for port/protocol combination counts.
    """
    tag_counts = defaultdict(int)  # Dict to count occurrences of each tag
    port_protocol_counts = defaultdict(int)  # Dict to count occurrences of each port/protocol combination
    
    with open(log_file, mode='r') as file:
        for line in file:
            line = line.strip()  # Remove any leading/tailing whitespace or newlines
            if not line:
                continue  # Skip empty lines
            
            fields = line.split()  # Split the line into fields based on whitespace
            if len(fields) < 14:
                continue  # Skip lines that don't have enough fields
            
            dstport = fields[4]  # Extract the destination port
            protocol_num = fields[6]  # Extract the protocol number
            # Map protocol number to its corresponding protocol name
            protocol = "tcp" if protocol_num == "6" else "udp" if protocol_num == "17" else "icmp"
            
            tags = lookup_dict.get((dstport, protocol), ["Untagged"])  # Get tags or use "Untagged" if no match
            for tag in tags:
                tag_counts[tag] += 1  # Increment the count for each associated tag
            
            port_protocol_counts[(dstport, protocol)] += 1  # Increment the count for the port/protocol combination
            
            if verbosity >= 2:
                logging.info(f"Processed line with port: {dstport}, protocol: {protocol}, tags: {tags}")

    return tag_counts, port_protocol_counts

def save_results(tag_counts, port_protocol_counts, output_file):
    """
    Save the results to the specified output file.
    
    Args:
        tag_counts (defaultdict): dictt containing tag counts.
        port_protocol_counts (defaultdict): dict containing port/protoccol combination counts.
        output_file (str): Path to the output file.
    """
    with open(output_file, mode='w') as file:
        file.write("Tag Counts:\n")
        file.write("Tag,Count\n")
        for tag, count in sorted(tag_counts.items()):
            file.write(f"{tag},{count}\n")  # Write each tag and its count
        
        file.write("\nPort/Protocol Combination Counts:\n")
        file.write("Port,Protocol,Count\n")
        for (port, protocol), count in sorted(port_protocol_counts.items()):
            file.write(f"{port},{protocol},{count}\n")  # Write each port/protocol combination and its count

def main():
    """
    Main function to parse command-line arguments, process the flow logs, and save results.
    """
    parser = argparse.ArgumentParser(description="Parse flow logs and map them to tags using a lookup table.")
    parser.add_argument("lookup_file", help="Path to the lookup table file (txt).")
    parser.add_argument("log_file", help="Path to the flow log file (txt).")
    parser.add_argument("-o", "--output", default=None, help="Output file name (default: output_results_<UTC_TIMESTAMP>.txt).")
    parser.add_argument("-v", "--verbosity", type=int, choices=[0, 1, 2], default=1, help="Set verbosity level: 0 (errors), 1 (info), 2 (debug).")
    parser.add_argument("-l", "--logfile", help="Log to a file instead of the console.")
    
    args = parser.parse_args()
    
    # Generate default output file name with UTC timestamp if not provided
    if args.output is None:
        utc_timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        args.output = f"output_results_{utc_timestamp}.txt"
    
    # Configure logging based on verbosity and optional logfile
    if args.logfile:
        logging.basicConfig(filename=args.logfile, level=logging.DEBUG if args.verbosity == 2 else logging.INFO)
    else:
        logging.basicConfig(level=logging.DEBUG if args.verbosity == 2 else logging.INFO)

    logging.info("Loading lookup table...")
    lookup_dict = load_lookup_table(args.lookup_file)  # Load the lookup table
    
    logging.info("Parsing flow logs...")
    tag_counts, port_protocol_counts = parse_flow_logs(args.log_file, lookup_dict, args.verbosity)  # Parse the flow logs

    logging.info(f"Saving results to {args.output}...")
    save_results(tag_counts, port_protocol_counts, args.output)  # Save the results to the output file
    
    logging.info("Processing complete.")

if __name__ == "__main__":
    main()
