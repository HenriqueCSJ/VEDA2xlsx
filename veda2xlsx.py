import re
import pandas as pd
import xlsxwriter
from itertools import chain

# Put here the path to the output files
vdf_file_path = "/home/henrique/Coding/Python/VEDA2XLSX/test/nq1a.vdf"
dd2_file_path = "/home/henrique/Coding/Python/VEDA2XLSX/test/nq1a.dd2"

# ----------------HERE STARTS THE TREATMENT OF THE VDF FILE -----------

vdf_big_list = []
vdf_s_lines_string = """ """

with open(vdf_file_path, "r") as vdf_all_input_lines:
    for vdf_line in vdf_all_input_lines.readlines()[4:]:
        if "Frequencies" in vdf_line:
            break
        else:
            vdf_s_line_fixed = vdf_line.strip()
            vdf_s_lines_list = list(filter(None, vdf_s_line_fixed.split(" ")))
            vdf_big_list.append(vdf_s_lines_list)
            vdf_big_list2 = list(filter(None, vdf_big_list))

# ----------------HERE ENDS THE TREATMENT OF THE VDF FILE -----------

# ----------------HERE STARTS THE TREATMENT OF THE DD2 FILE -----------

dd2_big_list2 = []
dd2_s_lines_string = """ """

with open(dd2_file_path, "r") as dd2_all_input_lines:
    for dd2_line in dd2_all_input_lines:
        if "alternative" in dd2_line:
            break
        else:
            dd2_valid_lines = dd2_line
            dd2_s_lines = re.match(r"s\s\d(.*)", dd2_valid_lines)
            if dd2_s_lines:
                dd2_s_lines_string += dd2_s_lines.group(0) + "\n"


def while_not_alpha(iterator):
    iterator = iter(iterator)
    for s in iterator:
        if not str(s).isalpha():
            yield s
        else:
            yield chain([s], iterator)
            break


def parse(line):
    *chunk1, rest = line.split(maxsplit=4)
    *chunk2, rest = while_not_alpha(rest.split())
    rest = list(rest)
    chunk3 = rest[:2]
    chunk4 = rest[2:]
    chunk1[0:2] = [''.join(chunk1[0:2])]
    chunk1 = [chunk1[0], chunk1[-1]]
    return chunk1, chunk2, chunk3  # , chunk4


#chunk1, chunk2, chunk3, chunk4 = map(list, zip(*map(parse, dd2_s_lines_string.splitlines())))
chunk1, chunk2, chunk3 = map(
    list, zip(*map(parse, dd2_s_lines_string.splitlines())))


df = pd.concat(
    map(pd.DataFrame, map(list, zip(*map(parse, dd2_s_lines_string.splitlines())))),
    axis=1, keys=[f'chunk{i}' for i in range(1, 5)]
)

dd2_big_list = df.values.tolist()
dd2_sublist = []

for i in range(len(dd2_big_list)):
    dd2_sublist = dd2_big_list[i]
    dd2_big_list2.append(dd2_sublist)
#    print(dd2_sublist)

# ----------------HERE ENDS THE TREATMENT OF THE DD2 FILE -----------

# ----------------HERE STARTS THE GENERATION OF THE OUTPUT -----------

for i in vdf_big_list2:
    for j in range(len(i)):
        for k in dd2_big_list2:
            if(i[j] == k[0]):
                i[j] = k
print(vdf_big_list2)

# Let's generate the Excel file here

big_df = pd.DataFrame(vdf_big_list2)
writer = pd.ExcelWriter('veda2xlsx_output.xlsx', engine='xlsxwriter')
big_df.to_excel(writer, sheet_name='VEDA2XLSX')
writer.save()