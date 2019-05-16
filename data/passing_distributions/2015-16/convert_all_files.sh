# 1. Converts .xlsx/xls files in tables/ to .csv
#    and outputs to csv/x.csv
# 2. Parses csv to node/edge format
#    and outputs to networks/

# for file in tables/*;
#     do
#         if [[ $file =~ \.xlsx?$ ]]
#         then
#             echo $file
#             python excel_to_csv.py -xls $file
#         fi
#     done

for file in csv/*;
    do
        if [[ $file =~ /(.+)\.+ ]]
        then
            prefix="networks/${BASH_REMATCH[1]}"
        echo "prefix is $prefix"
        python parse_passing.py -i $file -o $prefix
        fi
    done
