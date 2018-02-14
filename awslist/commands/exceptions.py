from colorama import Fore

UNKNOWN_VAR = """{0}[!]{1} Non-existent variable in configuration file.""".format(Fore.RED, Fore.RESET)

AWS_CONFIG_FILE = """{0}[!]{1} Error to parser AWS credentials.
Check: https://docs.aws.amazon.com/cli/latest/userguide/cli-config-files.html.""".format(Fore.RED, Fore.RESET)
