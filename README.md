# Illumio Technical Assessment for Mimi Pieper
# Author: Mimi Pieper

## Running the Program

### Command-Line Tool
This program has a simple command line tool that allows for manual selection of files to parse, the output file name and location, verobosity, and a help function.

1. **Command-Line Arguments:**
   - I used the `argparse` module to handle command-line arguments.
   - The arguments include:
     - `lookup_file`: Path to the lookup table file.
     - `log_file`: Path to the flow log file.
     - `-o` or `--output`: Optional argument to specify the output file name and location.
     - `-v` or `--verbosity`: Optional argument to set the verbosity level (0 for errors, 1 for info, 2 for debug).
     - `-l` or `--logfile`: Optional argument to log to a file instead of the console.

2. **Logging:**
   - Logging is integrated into the program with adjustable verbosity levels. 
   - Verbosity level 0 logs only errors, level 1 logs informational messages, and level 2 logs debug messages including detailed processing of each line. This is obviously not a very efficient use of resources for large files, so it is on the lowest logging option by default, but can be enabled to help with debugging and issues.

3. **Default Values:**
   - The output file defaults to `output_results.txt` if not specified.
   - Verbosity defaults to level 1 (info), which logs key steps in the process, but does not give line by line information.

### Instructions for Running the Program

1. **Prerequisites:**
   - Ensure Python 3 is installed on your machine.

2. **File Setup:**
   - All required files are included.

3. **Running the Program:**
   - Here is the command structure to run the program:
     ```bash
     python3 src/flow_log_parser.py lookup_tables/lookup_table.txt sample_logs/flow_logs.txt
     ```
   - Optional arguments:
     - To specify a different output file name/location:
       ```bash
       python3 src/flow_log_parser.py lookup_tables/lookup_table.txt sample_logs/flow_logs.txt -o custom_output.txt
       ```
     - To set the verbosity level (0,1,2):
       ```bash
       python3 src/flow_log_parser.py lookup_tables/lookup_table.txt sample_logs/flow_logs.txt -v 2
       ```
     - To log output to a file:
       ```bash
       python3 src/flow_log_parser.py lookup_tables/lookup_table.txt sample_logs/flow_logs.txt -l log.txt
       ```

NOTE: There are two provided sample logs, one formatted without extra whitespace, and the other with additional trailing whitespace. This program gracefully handles them both.

I have included outputs for the program including sample logs in the `output` folder for your convinence.

The `output_results` files are saved as `output_results_UTC_TIME` to ensure each run fives an individual file, not overwritting another file.

## Testing and Assumptions
### Assumptions:
- The protocol numbers 6, 17, and 1 correspond to tcp, udp, and icmp respectively.
- Untagged entries in the flow logs are counted under the tag "Untagged".
- The flow logs follow the format provided in the sample data. 
    - NOTE: some robustness was added here by stripping off whitespace and newlines from the log files.
- The flow logs are given as TXT files.

### Testing:
- The program was tested with the provided sample flow logs and the provided sample lookup table.
- Furthermore the program was tested with various flow log samples to ensure proper parsing and tagging. IE: I took the base sample logs and edited some of the data slightly.
- The output was verified to match the expected format, and the counts were checked for accuracy.
E- dge cases, such as missing or incorrectly formatted lines in the flow log, are handled gracefully, with the program continuing to process valid lines.

## Analysis
### Efficiency:
The program is designed to handle large files (up to 10 MB for logs and 10,000 mappings in the lookup table) quickly and with minimal computational resorces by processing the data line by line. 

It uses dictionaries for quick lookups and avoids loading the entire file into memory at once, which means large files can be processed quickly.

### Tag Counts and Port/Protocol Combination Counts:
The program outputs a formatted output file that lists the counts of tags and the counts of port/protocol combinations as specified. Both sections are sorted alphabetically or numerically for easier readability.

The lookup table allows multiple tags to be associated with the same port/protocol combination. The program correctly increments counts for each tag associated with a given flow log entry.

### Handling Case Sensitivity:
The protocol field is normalized to lowercase when checking against the lookup table to ensure case-insensitive matching, fulfilling the requirement that matches should be case insensitive.

The program has case-insensitive protocol matching, making it flexible to handle variations in log data.

### Flexible Lookup Table:
The lookup table can have up to 10,000 mappings, and the program supports mapping a tag to multiple port/protocol combinations.

### Stripping Whitespace:
The program strips leading and trailing whitespace from each line of both the lookup table and flow logs, ensuring that extra spaces or newlines do not interfere with parsing.
