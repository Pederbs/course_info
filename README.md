# Description

The scripts are meant to make course selection at the University of Bologna (UNIBO) easier. It works by using UNIBO's course search page to save all courses listed and then later scrape all course descriptions from each course page. All data are later dumped to a `.json` file for easy searching of learning goals, topics or keywords.

# Usage

`script.py` 

This script will scrape all info from a particular search defined in `params` (line 116) and return a `.json` file that can be searched


`cleaner.py`

This script will return a "cleaned" `.json` from an existing `.json`, the cleaning is to delete any course that does not have a timetable (I assume that the course is not taught in the current semester)

## example files
I included Engineering and Science as example files, they were created 14.08.2024 and gives a view of what the script creates