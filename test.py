import json
# import random
# sesi_mulai_3_blok = [1, 3, 4, 7, 10]
# period = random.randrange(0, 1)
# period = random.choice(sesi_mulai_3_blok)
# print(period)

input_file = 'classes/stis.json'
with open(input_file, 'r') as read_file:
    data = json.load(read_file)

# dummy = data['Ruang Kelas']['25']
# # print(dummy)

# dummy = dummy + data['Ruang Kelas']['26']
# # print(dummy)

# professors = {}
# prefRoomProf = {}


# # mengambil preferensi waktu dosen
# for professor in data['Dosen']:
#     professors[professor['Name']] = professor['PrefTime']
#     prefRoomProf[professor['Name']] = []
#     for gedung in professor['PrefRoom']:
#         prefRoomProf[professor['Name']] += data['Ruang Kelas'][gedung]
# print(professors['yunarso anang'][0])

constraints = data['Constraints']
# for i, professor in enumerate(constraints['Data']):
# for professor in constraints['Data']:
# for i in constraints['Session']:
#     print(professor, i)
