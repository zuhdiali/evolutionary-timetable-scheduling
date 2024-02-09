import json
# import random
sesi_mulai_3_blok = [1, 3, 4, 7]
sesi_mulai_2_blok = [1, 3, 5, 7]
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

professors = {}
prefRoomProf = {}
profAvailable = {}
profAvailable2Blok = {}
profAvailable3Blok = {}

# mengambil preferensi waktu dosen
for professor in data['Dosen']:
    professors[professor['Name']] = professor['PrefTime']

    profAvailable2Blok[professor['Name']] = []
    for i in range(len(professor['PrefTime'])-1):
        if professor['PrefTime'][i] == 0 and professor['PrefTime'][i+1] != 1 and (i % 9 + 1) in sesi_mulai_2_blok:
            profAvailable2Blok[professor['Name']] += [i]

    profAvailable3Blok[professor['Name']] = []
    for i in range(len(professor['PrefTime'])-2):
        if professor['PrefTime'][i] == 0 and professor['PrefTime'][i+1] != 1 and professor['PrefTime'][i+2] != 1 and (i % 9 + 1) in sesi_mulai_3_blok:
            profAvailable3Blok[professor['Name']] += [i]

    prefRoomProf[professor['Name']] = []
    for gedung in professor['PrefRoom']:
        prefRoomProf[professor['Name']] += data['Ruang Kelas'][gedung]
# print(profAvailable2Blok['ratih ngestrini'])
# print(profAvailable3Blok['ratih ngestrini'])
profAvailable["2 Blok"] = profAvailable2Blok
profAvailable["3 Blok"] = profAvailable3Blok
print(profAvailable['2 Blok']['ratih ngestrini'])
# constraints = data['Constraints']
# for i, professor in enumerate(constraints['Data']):
# for professor in constraints['Data']:
# for i in constraints['Session']:
#     print(professor, i)

# print(int(5/3))
