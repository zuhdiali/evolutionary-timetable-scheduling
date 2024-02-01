import json
import random


def load_data(path):
    with open(path, 'r') as read_file:
        data = json.load(read_file)

    for university_class in data['Casovi']:
        classroom = university_class['Classroom']
        university_class['Classroom'] = data['Ucionice'][classroom]

    data = data['Casovi']

    return data


def generate_chromosome(data):
    professors = {}
    classrooms = {}
    groups = {}
    subjects = {}

    new_data = []
    sesi_mulai_3_blok = [1, 3, 4, 7]
    sesi_mulai_2_blok = [1, 3, 5, 7]
    for single_class in data:
        professors[single_class['Professor']] = [0] * 60
        for classroom in single_class['Classroom']:
            classrooms[classroom] = [0] * 60
        for group in single_class['Groups']:
            groups[group] = [0] * 60
        subjects[single_class['Subject']] = {'P': [], 'V': [], 'L': []}

    for single_class in data:
        new_single_class = single_class.copy()

        classroom = random.choice(single_class['Classroom'])
        day = random.randrange(0, 5)
        if (int(single_class['Duration']) == 3):
            period = random.choice(sesi_mulai_3_blok)
            period = period - 1
        else:
            period = random.choice(sesi_mulai_2_blok)
            period = period - 1
        # if day == 4:
        #     period = random.randrange(0, 9 - int(single_class['Duration']))
        # else:
        #     period = random.randrange(0, 13 - int(single_class['Duration']))
        new_single_class['Assigned_classroom'] = classroom
        time = 9 * day + period
        new_single_class['Assigned_time'] = time

        for i in range(time, time + int(single_class['Duration'])):
            professors[new_single_class['Professor']][i] += 1
            classrooms[classroom][i] += 1
            for group in new_single_class['Groups']:
                groups[group][i] += 1
        subjects[new_single_class['Subject']][new_single_class['Type']].append(
            (time, new_single_class['Groups']))

        new_data.append(new_single_class)

    return (new_data, professors, classrooms, groups, subjects)


def write_data(data, path):
    for single_class in data:
        single_class['Day'] = single_class['Assigned_time'] // 9
        single_class['Classroom'] = single_class['Assigned_classroom']
        for i in range(int(single_class['Duration'])):
            single_class['Sesi {}'.format(i+1)] = str(single_class['Assigned_time'] %
                                                      9 + i + 1) + " "
    with open(path, 'w') as write_file:
        json.dump(data, write_file, indent=4)
