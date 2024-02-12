import json
import random
import pandas as pd


def load_data(path):
    professors = {}
    prefRoomProf = {}
    profAvailable = {}
    profAvailable2Blok = {}
    profAvailable3Blok = {}

    sesi_mulai_3_blok = [1, 3, 4, 7]
    sesi_mulai_2_blok = [1, 3, 5, 7]

    with open(path, 'r') as read_file:
        data = json.load(read_file)

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
    profAvailable["2 Blok"] = profAvailable2Blok
    profAvailable["3 Blok"] = profAvailable3Blok

    for university_class in data['Perkuliahan']:
        # classroom = university_class['Classroom']
        university_class['Classroom'] = prefRoomProf[university_class['Professor']]

    constraints = data['Constraints']
    data = data['Perkuliahan']

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
        # professors[single_class['Professor']] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0,
        #                                          0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for classroom in single_class['Classroom']:
            classrooms[classroom] = [0] * 45
        for group in single_class['Groups']:
            groups[group] = [0] * 45
        subjects[single_class['Subject']] = {'P': [], 'V': [], 'L': []}

    for constraint in constraints:
        match constraint['Key']:
            case 'Professor':
                if constraint['is All'] == True:
                    for professor in professors:
                        for i in constraint['Session']:
                            professors[professor][i] = 99
                else:
                    for professor in constraint['Data']:
                        for i in constraint['Session']:
                            professors[professor][i] = 99
            case 'Group':
                if constraint['is All'] == True:
                    for group in groups:
                        for i in constraint['Session']:
                            groups[group][i] = 99
                else:
                    for group in constraint['Data']:
                        for i in constraint['Session']:
                            groups[group][i] = 99

    for single_class in data:
        new_single_class = single_class.copy()

        classroom = random.choice(single_class['Classroom'])
        new_single_class['Assigned_classroom'] = classroom

        # # ------------------------------ INI KODINGAN SEBELUMNYA ------------------------------
        # day = random.randrange(0, 5)
        # if (int(single_class['Duration']) == 3):
        #     period = random.choice(sesi_mulai_3_blok)
        #     period = period - 1
        # else:
        #     period = random.choice(sesi_mulai_2_blok)
        #     period = period - 1
        # # if day == 4:
        # #     period = random.randrange(0, 9 - int(single_class['Duration']))
        # # else:
        # #     period = random.randrange(0, 13 - int(single_class['Duration']))
        # time = 9 * day + period
        # # ------------------------------ INI KODINGAN SEBELUMNYA ------------------------------

        # ------------------------------ INI KODINGAN BARU ------------------------------
        if int(single_class['Duration']) == 3:
            time = random.choice(
                profAvailable['3 Blok'][single_class['Professor']])
            # while time + int(single_class['Duration']) > 45:
            #     time = random.choice(profAvailable['3 Blok'][single_class['Professor']])
        else:
            time = random.choice(
                profAvailable['2 Blok'][single_class['Professor']])
        #     while time + int(single_class['Duration']) > 45:
        #         time = random.choice(profAvailable['2 Blok'][single_class['Professor']])
        # time = random.choice(profAvailable[single_class['Professor']])
        # while time + int(single_class['Duration']) > 44:
        #     time = random.choice(profAvailable[single_class['Professor']])
        # ------------------------------ INI KODINGAN BARU ------------------------------

        new_single_class['Assigned_time'] = time

        for i in range(time, time + int(single_class['Duration'])):
            professors[new_single_class['Professor']][i] += 1
            classrooms[classroom][i] += 1
            for group in new_single_class['Groups']:
                groups[group][i] += 1
        subjects[new_single_class['Subject']][new_single_class['Type']].append(
            (time, new_single_class['Groups']))

        new_data.append(new_single_class)

    return (new_data, professors, classrooms, groups, subjects, profAvailable)


def write_data(data, path):
    for single_class in data:
        single_class['Day'] = single_class['Assigned_time'] // 9
        single_class['Classroom'] = single_class['Assigned_classroom']
        for i in range(int(single_class['Duration'])):
            single_class['Sesi {}'.format(i+1)] = str(single_class['Assigned_time'] %
                                                      9 + i + 1)
    with open(path, 'w') as write_file:
        json.dump(data, write_file, indent=4)


def write_csv(df, path):
    if isinstance(df, list):
        for single_class in df:
            single_class['Groups'] = single_class['Groups'][0]
        df = pd.DataFrame(df)
    # new_data.to_csv('stis/output_dummy.csv', sep=',', index=False)
    # if isinstance(df, list) and df['Groups']:
    #     df['Groups'] = df['Groups'][0]
    #     df = pd.DataFrame(df)
    df.to_csv(path, sep=',', index=False)
