# Parsing Passing Distributions

## Objectives
1. convert tables/*.xls(x) to .csv
2. get nodes/edges from csv/*.csv

## Instructions

1. copy convert_all_files.sh, parse_passing.py, and excel_to_csv.py
to your working directory (be it matchdayx, r-16, etc. with csv, tables dir's)
2. $ mkdir networks
3. $ bash convert_all_files.sh

## Results
In the networks directory,
- [date]_tpd-[teamName]-edges
    * player_num1 player_num2 weight
- [date]_tpd-[teamName]-nodes
    * player_num player_name
- [date]_tpd-[teamName]-players
    * player_num, passes_completed, passes_attempted, passes_completed%
- [date]_tpd-[teamName]-team
    * player_num, passes_completed, passes_attempted, passes_completed%

