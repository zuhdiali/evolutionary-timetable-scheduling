import data as dt
import pandas as pd
import cost_functions
import mutation
from copy import deepcopy

max_generations = 6000
num_runs = 1
input_file = 'stis/stis_komplit.json'
output_file = 'stis/output_stis_komplit.json'
output_file_csv = 'stis/output_stis_komplit.csv'
output_prof_load = 'stis/load_prof_stis_komplit.csv'
output_classroom_load = 'stis/load_classroom_stis_komplit.csv'
output_group_load = 'stis/load_group_stis_komplit.csv'
cost_function = cost_functions.cost
cost_function2 = cost_functions.cost2


def evolutionary_algorithm():
    best_timetable = None
    chromosome = dt.load_data(input_file)
    neighbour = mutation.neighbour
    for i in range(num_runs):
        chromosome = dt.generate_chromosome(
            chromosome[0], chromosome[1], chromosome[2], chromosome[3])

        for j in range(max_generations):
            new_chromosome = neighbour(deepcopy(chromosome))
            ft = cost_function(chromosome)
            if ft == 0:
                break
            ftn = cost_function(new_chromosome)
            if ftn <= ft:
                chromosome = new_chromosome
            if j % 200 == 0:
                print('Iteration', j, 'cost', cost_function(chromosome))

        # print('Run', i + 1, 'cost', cost_function(chromosome),
        #       'chromosome', chromosome)

        if best_timetable is None or cost_function2(chromosome) <= cost_function2(best_timetable):
            best_timetable = deepcopy(chromosome)

    chromosome = best_timetable

    neighbour2 = mutation.neighbour2

    for j in range(3 * max_generations):
        new_chromosome = neighbour2(deepcopy(chromosome))
        ft = cost_function2(chromosome)
        ftn = cost_function2(new_chromosome)
        if ftn <= ft:
            chromosome = new_chromosome
        if j % 200 == 0:
            print('Iteration', j, 'cost', cost_function2(chromosome))
        if ft == 0:
            break

    # print('Run', 'cost', cost_function2(chromosome), 'chromosome', chromosome)

    dt.write_data(chromosome[0], output_file)

    professor_hard = True
    classroom_hard = True
    group_hard = True
    allowed_classrooms = True
    df_classroom = pd.DataFrame({"classroom": [], "keterangan": []})

    # Check hard constraints
    for single_class in chromosome[0]:
        if single_class['Assigned_classroom'] not in single_class['Classroom']:
            allowed_classrooms = False
            df_classroom = df_classroom._append(
                {"classroom": single_class['Assigned_classroom'],
                 "keterangan": 'kelas untuk kuliah ' + single_class['Professor'] + ' ' + single_class['Subject'] + ' tidak sesuai dengan ruang kelas yang diinginkan'}, ignore_index=True)
    for profesor in chromosome[1]:
        for i in range(len(chromosome[1][profesor])):
            if chromosome[1][profesor][i] > 1 and chromosome[1][profesor][i] < 99:
                professor_hard = False
    for ucionica in chromosome[2]:
        for i in range(len(chromosome[2][ucionica])):
            if chromosome[2][ucionica][i] > 1:
                classroom_hard = False
    for group in chromosome[3]:
        for i in range(len(chromosome[3][group])):
            if chromosome[3][group][i] > 1:
                group_hard = False

    print('Are hard restrictions for professors satisfied:', professor_hard)
    print('Are hard restrictions for classrooms satisfied:', classroom_hard)
    print('Are hard restrictions for groups satisfied:', group_hard)
    print('Are hard restrictions for allowed classrooms satisfied:',
          allowed_classrooms)

    # Check preferred order statistics
    subjects_cost = 0
    for single_class in chromosome[4]:
        subject_cost = 0
        for lab in chromosome[4][single_class]['L']:
            for practice in chromosome[4][single_class]['V']:
                for group in lab[1]:
                    if group in practice[1] and lab[0] < practice[0]:
                        subject_cost += 1
            for lecture in chromosome[4][single_class]['P']:
                for group in lab[1]:
                    if group in lecture[1] and lab[0] < lecture[0]:
                        subject_cost += 1
        for practice in chromosome[4][single_class]['V']:
            for lecture in chromosome[4][single_class]['P']:
                for group in practice[1]:
                    if group in lecture[1] and practice[0] < lecture[0]:
                        subject_cost += 1
        subjects_cost += subject_cost
        print('Subject cost for subject', single_class, 'is:', subject_cost)
    print('Total subject cost:', subjects_cost)

    # Check group statistics
    df_group = pd.DataFrame(
        {"group": [], "cost": [], "load": [], "keterangan": []})
    total_group_cost = 0
    total_group_load = 0
    max_group_cost = 0
    for group in chromosome[3]:
        group_cost = 0
        group_load = 0
        for day in range(5):
            last_seen = 0
            found = False
            current_load = 0
            for hour in range(9):
                time = day * 9 + hour
                if chromosome[3][group][time] >= 1 and chromosome[3][group][time] < 99:
                    current_load += 1
                    if not found:
                        found = True
                    else:
                        group_cost += (time - last_seen - 1)
                    last_seen = time
                    if chromosome[3][group][time] >= 2:
                        df_group = df_group._append(
                            {"group": group, "cost": group_cost, "load": group_load,
                             "keterangan": 'bentrok jadwal pada hari ' + str(day) + ' sesi ' + str(hour+1)}, ignore_index=True)
            if current_load > 6:
                group_load += 1
        print('Groups cost for group', group, 'is:',
              group_cost, ', number of hard days:', group_load)
        if max_group_cost < group_cost:
            max_group_cost = group_cost
        total_group_cost += group_cost
        total_group_load += group_load
    print('Maximum group cost is:', max_group_cost)
    print('Average group cost is:', total_group_cost / len(chromosome[3]))
    print('Total group load is:', total_group_load)

    # Check classroom statistics
    for classroom in chromosome[2]:
        for day in range(5):
            for hour in range(9):
                time = day * 9 + hour
                if chromosome[2][classroom][time] > 1 and chromosome[2][classroom][time] < 99:
                    print('Classroom violation for classroom', classroom, 'is:',)
                    df_classroom = df_classroom._append(
                        {"classroom": classroom,
                         "keterangan": 'bentrok jadwal pada hari ' + str(day) + ' sesi ' + str(hour+1)}, ignore_index=True)

    # Check professor statistics
    df_prof = pd.DataFrame(
        {"professor": [], "cost": [], "load": [], "keterangan": []})
    total_prof_cost = 0
    total_prof_load = 0
    # free_hour = True
    max_prof_cost = 0
    for prof in chromosome[1]:
        pref_time_violation = False
        prof_cost = 0
        prof_load = 0
        for day in range(5):
            last_seen = 0
            found = False
            current_load = 0
            for hour in range(9):
                time = day * 9 + hour
                if chromosome[1][prof][time] >= 1 and chromosome[1][prof][time] < 99:
                    # if time == 59:
                    #     free_hour = False
                    current_load += 1
                    if not found:
                        found = True
                    else:
                        prof_cost += (time - last_seen - 1)
                    last_seen = time
                    if chromosome[1][prof][time] >= 2:
                        df_prof = df_prof._append(
                            {"professor": prof, "cost": prof_cost, "load": prof_load,
                             "keterangan": 'bentrok jadwal pada hari ' + str(day) + ' sesi ' + str(hour+1)}, ignore_index=True)
                elif chromosome[1][prof][time] > 99:
                    pref_time_violation = True
            if current_load > 6:
                prof_load += 1
                df_prof = df_prof._append(
                    {"professor": prof, "cost": prof_cost, "load": prof_load, "keterangan": "mengajar terlalu banyak perkuliahan"}, ignore_index=True)
        print('Prof cost for prof', prof, 'is:', prof_cost,
              ', number of hard days:', prof_load)
        if pref_time_violation:
            df_prof = df_prof._append(
                {"professor": prof, "cost": prof_cost, "load": prof_load, "keterangan": "pelanggaran preferensi waktu"}, ignore_index=True)
        if max_prof_cost < prof_cost:
            max_prof_cost = prof_cost
        total_prof_cost += prof_cost
        total_prof_load += prof_load
    print('Max prof cost is:', max_prof_cost)
    print('Average prof cost is:', total_prof_cost / len(chromosome[1]))
    print('Total prof load is:', total_prof_load)
    # print('Free hour:', free_hour, ', 59')

    dt.write_csv(df_prof, output_prof_load)
    dt.write_csv(df_classroom, output_classroom_load)
    dt.write_csv(df_group, output_group_load)
    dt.write_csv(chromosome[0], output_file_csv)


evolutionary_algorithm()
