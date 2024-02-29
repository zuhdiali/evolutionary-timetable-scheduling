import json
import random
import pandas as pd


def load_data(path):
    rooms = {}
    professors = {}
    prefRoomProf = {}
    profAvailable = {}
    profAvailable2Blok = {}
    profAvailable3Blok = {}

    sesi_mulai_3_blok = [1, 3, 4, 7]
    sesi_mulai_2_blok = [1, 3, 5, 7]

    with open(path, 'r') as read_file:
        data = json.load(read_file)

    for room in data['ruangKelas']:
        rooms[room['gedung']] = []
        for nomorRuang in room['ruangan']:
            rooms[room['gedung']].append(nomorRuang)

    # mengambil preferensi waktu dosen
    for professor in data['dosen']:
        professors[professor['name']] = professor['prefTime']

        profAvailable2Blok[professor['name']] = []
        for i in range(len(professor['prefTime'])-1):
            if professor['prefTime'][i] == 0 and professor['prefTime'][i+1] != 1 and (i % 9 + 1) in sesi_mulai_2_blok:
                profAvailable2Blok[professor['name']] += [i]

        profAvailable3Blok[professor['name']] = []
        for i in range(len(professor['prefTime'])-2):
            if professor['prefTime'][i] == 0 and professor['prefTime'][i+1] != 1 and professor['prefTime'][i+2] != 1 and (i % 9 + 1) in sesi_mulai_3_blok:
                profAvailable3Blok[professor['name']] += [i]

        prefRoomProf[professor['name']] = []
        for gedung in professor['prefRoom']:
            prefRoomProf[professor['name']] += rooms[gedung]
    profAvailable["2 Blok"] = profAvailable2Blok
    profAvailable["3 Blok"] = profAvailable3Blok

    for university_class in data['perkuliahan']:
        # classroom = university_class['Classroom']
        university_class['Classroom'] = prefRoomProf[university_class['professor']]

    constraints = data['constraints']
    data = data['perkuliahan']

    return (data, professors, constraints, profAvailable)


def generate_chromosome(data, professors, constraints, profAvailable):
    classrooms = {}
    groups = {}
    subjects = {}

    new_data = []
    sesi_mulai_3_blok = [1, 3, 4, 7]
    sesi_mulai_2_blok = [1, 3, 5, 7]

    for single_class in data:
        # preferensi waktu dosen sudah diambil dari file json
        # preferensi waktu dosen bisa dilihat di sini
        # professors[single_class['professor']] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0,
        #                                          0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for classroom in single_class['Classroom']:
            classrooms[classroom] = [0] * 45
        for group in single_class['groups']:
            groups[group] = [0] * 45
        subjects[single_class['subject']] = {'P': [], 'V': [], 'L': []}

    for constraint in constraints:
        match constraint['key']:
            case 'professor':
                if constraint['isAll'] == True:
                    for professor in professors:
                        for i in constraint['session']:
                            professors[professor][i] = 999
                else:
                    for professor in constraint['data']:
                        for i in constraint['session']:
                            professors[professor][i] = 999
            case 'Group':
                if constraint['isAll'] == True:
                    for group in groups:
                        for i in constraint['session']:
                            groups[group][i] = 999
                else:
                    for group in constraint['data']:
                        for i in constraint['session']:
                            groups[group][i] = 999

    for single_class in data:
        new_single_class = single_class.copy()

        classroom = random.choice(single_class['Classroom'])
        new_single_class['Assigned_classroom'] = classroom

        # # ------------------------------ INI KODINGAN SEBELUMNYA ------------------------------
        # day = random.randrange(0, 5)
        # if (int(single_class['duration']) == 3):
        #     period = random.choice(sesi_mulai_3_blok)
        #     period = period - 1
        # else:
        #     period = random.choice(sesi_mulai_2_blok)
        #     period = period - 1
        # # if day == 4:
        # #     period = random.randrange(0, 9 - int(single_class['duration']))
        # # else:
        # #     period = random.randrange(0, 13 - int(single_class['duration']))
        # time = 9 * day + period
        # # ------------------------------ INI KODINGAN SEBELUMNYA ------------------------------

        # ------------------------------ INI KODINGAN BARU ------------------------------
        if int(single_class['duration']) == 3:
            time = random.choice(
                profAvailable['3 Blok'][single_class['professor']])
            # while time + int(single_class['duration']) > 45:
            #     time = random.choice(profAvailable['3 Blok'][single_class['professor']])
        else:
            time = random.choice(
                profAvailable['2 Blok'][single_class['professor']])
        #     while time + int(single_class['duration']) > 45:
        #         time = random.choice(profAvailable['2 Blok'][single_class['professor']])
        # time = random.choice(profAvailable[single_class['professor']])
        # while time + int(single_class['duration']) > 44:
        #     time = random.choice(profAvailable[single_class['professor']])
        # ------------------------------ INI KODINGAN BARU ------------------------------

        new_single_class['Assigned_time'] = time

        for i in range(time, time + int(single_class['duration'])):
            professors[new_single_class['professor']][i] += 1
            classrooms[classroom][i] += 1
            for group in new_single_class['groups']:
                groups[group][i] += 1
        subjects[new_single_class['subject']][new_single_class['type']].append(
            (time, new_single_class['groups']))

        new_data.append(new_single_class)

    return (new_data, professors, classrooms, groups, subjects, profAvailable)


def write_data(data, path):
    for single_class in data:
        single_class['Day'] = single_class['Assigned_time'] // 9
        single_class['Classroom'] = single_class['Assigned_classroom']
        for i in range(int(single_class['duration'])):
            single_class['Sesi {}'.format(i+1)] = str(single_class['Assigned_time'] %
                                                      9 + i + 1)
    with open(path, 'w') as write_file:
        json.dump(data, write_file, indent=4)


def write_csv(df, path):
    # cek apakah tipe data masih list, belum dataframe. Jika iya, maka ubah menjadi dataframe
    if isinstance(df, list):
        for single_class in df:
            single_class['groups'] = single_class['groups'][0]
        df = pd.DataFrame(df)
    df.to_csv(path, sep=',', index=False)


def write_excel(df, path):
    if isinstance(df, list):
        for single_class in df:
            single_class['groups'] = single_class['groups'][0]
        df = pd.DataFrame(df)
    df.to_excel(path, index=False)
