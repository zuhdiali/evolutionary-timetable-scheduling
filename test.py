import json
# import random
# sesi_mulai_3_blok = [1, 3, 4, 7, 10]
# period = random.randrange(0, 1)
# period = random.choice(sesi_mulai_3_blok)
# print(period)
input_file = 'classes/stis.json'
with open(input_file, 'r') as read_file:
    data = json.load(read_file)

dummy = data['Ruang Kelas']['25']

print(dummy)

dummy = dummy + data['Ruang Kelas']['26']

print(dummy)
