# import json
# # import random
# sesi_mulai_3_blok = [1, 3, 4, 7]
# sesi_mulai_2_blok = [1, 3, 5, 7]
# # period = random.randrange(0, 1)
# # period = random.choice(sesi_mulai_3_blok)
# # print(period)

# input_file = 'classes/stis.json'
# with open(input_file, 'r') as read_file:
#     data = json.load(read_file)

# # dummy = data['ruangKelas']['25']
# # # print(dummy)

# # dummy = dummy + data['ruangKelas']['26']
# # # print(dummy)

# professors = {}
# prefRoomProf = {}
# profAvailable = {}
# profAvailable2Blok = {}
# profAvailable3Blok = {}

# # mengambil preferensi waktu dosen
# for professor in data['dosen']:
#     professors[professor['name']] = professor['prefTime']

#     profAvailable2Blok[professor['name']] = []
#     for i in range(len(professor['prefTime'])-1):
#         if professor['prefTime'][i] == 0 and professor['prefTime'][i+1] != 1 and (i % 9 + 1) in sesi_mulai_2_blok:
#             profAvailable2Blok[professor['name']] += [i]

#     profAvailable3Blok[professor['name']] = []
#     for i in range(len(professor['prefTime'])-2):
#         if professor['prefTime'][i] == 0 and professor['prefTime'][i+1] != 1 and professor['prefTime'][i+2] != 1 and (i % 9 + 1) in sesi_mulai_3_blok:
#             profAvailable3Blok[professor['name']] += [i]

#     prefRoomProf[professor['name']] = []
#     for gedung in professor['prefRoom']:
#         prefRoomProf[professor['name']] += data['ruangKelas'][gedung]
# # print(profAvailable2Blok['ratih ngestrini'])
# # print(profAvailable3Blok['ratih ngestrini'])
# profAvailable["2 Blok"] = profAvailable2Blok
# profAvailable["3 Blok"] = profAvailable3Blok
# print(profAvailable['2 Blok']['ratih ngestrini'])
# # constraints = data['constraints']
# # for i, professor in enumerate(constraints['data']):
# # for professor in constraints['data']:
# # for i in constraints['session']:
# #     print(professor, i)

# # print(int(5/3))

#  ===============================================================================================

# # Importing pandas as pd
# import pandas as pd

# # Creating the first Dataframe using dictionary
# df1 = df = pd.DataFrame({"a": [1, 2, 3, 4],
#                          "b": ["5", "6", " 7", "8"]})

# # Creating the Second Dataframe using dictionary
# df2 = pd.DataFrame({"a": [1, 2, 3],
#                     "b": ["5", " 6", "7"]})

# # Print df1
# print("Printing df1")
# print(df1, "\n")

# # # Print df2
# # print("Printing df2")
# # print(df2, "\n")
# # Append Dict as row to DataFrame
# new_row = {"a": 10, "b": 'aku ditambah ' + str(10) + ' sama dengan berapa'}
# df2 = df._append(new_row, ignore_index=True)
# print(new_row)

# print(df2)

# path = 'classes/prof_load_stis_komplit.csv'
# df.to_csv(path, sep=',', index=False)

#  ===============================================================================================
import json
import pandas as pd
import data as dt

input_file = 'stis/stis_komplit.json'
with open(input_file, 'r') as read_file:
    data = json.load(read_file)

chromosome = dt.load_data(input_file)
chromosome = dt.generate_chromosome(
    chromosome[0], chromosome[1], chromosome[2], chromosome[3])
# data.to_csv('stis/output_dummy.csv', sep=',', index=False)
# print(isinstance(data, list))
# if isinstance(data, list):
#     for single_class in data:
#         single_class['groups'] = single_class['groups'][0]
#         single_class['Classroom'] = single_class['Assigned_classroom']
#     new_data = pd.DataFrame(data)
#     new_data.to_csv('stis/output_dummy.csv', sep=',', index=False)
#     print(isinstance(new_data, list))


print(chromosome[5])
