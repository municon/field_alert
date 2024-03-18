INVESTIGATE TODO:

# Add configuration file support:

# Instead of hardcoding sensitive information like email credentials and PDU IP addresses directly in the code, store them in a separate configuration file (e.g., config.ini or config.json).
# Use a library like configparser or json to read the configuration file and load the necessary values.
# This makes the program more secure and easier to maintain.
# Implement logging:

# Replace print statements with proper logging using the logging module.
# Configure different log levels (e.g., DEBUG, INFO, WARNING, ERROR) to control the verbosity of the logs.
# Write logs to a file for easier troubleshooting and monitoring.
# Add email filtering and parsing:

# Implement more robust email filtering based on specific criteria like sender, subject, or content.
# Use regular expressions or other parsing techniques to extract relevant information from the email body.
# Handle different email formats (plain text, HTML) and attachments more effectively.
# Implement error handling and retries:

# Wrap critical sections of code with try-except blocks to catch and handle specific exceptions gracefully.
# Implement retry mechanisms with exponential backoff for network-related operations (e.g., email retrieval, PDU control) to handle temporary failures.
# Provide informative error messages and log them appropriately.
# Enhance PDU control functionality:

# Add support for controlling multiple outlets simultaneously.
# Implement a mechanism to check the current status of outlets before sending control commands.
# Add a feature to schedule outlet control based on specific times or events.
# Improve email processing performance:

# Implement parallel processing or multithreading to handle multiple emails simultaneously.
# Use techniques like connection pooling or caching to optimize email retrieval and avoid unnecessary reconnections.
# Add monitoring and alerting:

# Implement a monitoring system to check the health and status of the program periodically.
# Send alerts (e.g., email, SMS) to administrators or relevant parties if critical errors occur or if the program becomes unresponsive.
# Implement a user-friendly interface:

# Create a command-line interface (CLI) or a graphical user interface (GUI) to allow users to configure settings, monitor the program's status, and control outlets manually.
# Use libraries like argparse for CLI or tkinter for GUI development.
# Add unit tests and documentation:

# Write unit tests to verify the correctness of critical functions and modules.
# Use a testing framework like unittest or pytest to organize and run the tests.
# Provide comprehensive documentation, including comments in the code, README files, and user guides, to facilitate understanding and maintenance of the program.
# Implement security measures:

# Use secure communication protocols (e.g., HTTPS) when interacting with the PDU or other external services.
# Implement authentication and authorization mechanisms to ensure only authorized users can control the PDU and access sensitive information.
# Follow security best practices, such as input validation, parameterized queries, and avoiding hardcoded credentials.
