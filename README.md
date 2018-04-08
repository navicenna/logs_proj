# logs project
Source code for a report generator written in Python and connecting to
PostgresSQL article log database. Three reports are output: the most popular articles,
the most popular authors, and an error report. Each report is output to a separate
text file.
By: Navid Bahmanyar


MODULES

1. report_gen.py: outputs reports


HOW TO USE:

1. Navigate to the vagrant directory
2. Run "vagrant up" to start the VM
3. Run "vagrant ssh" to log in
4. Clone my repository: https://github.com/nbahmanyar/logs_proj.git
5. Navigate to the repository in bash
6. Run "python report_gen.py"
7. The three reports will be output as text files in the same directory
