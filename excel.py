from population import Population
from constants import N
import xlsxwriter
import math
import os


def save_to_excel_internal(sheet, dictionary, col_num=1, row_num=2, print_keys=True):
    for key, value in dictionary.items():
        if print_keys:
            sheet.write(row_num - 1, col_num, key)
        if value[0] is None:
            sheet.write(row_num, col_num, "None")
        elif math.isnan(value[0]):
            sheet.write(row_num, col_num, "NaN")
        elif math.isinf(value[0]):
            sheet.write(row_num, col_num, "Inf")
        else:
            sheet.write_column(row_num, col_num, value)
        col_num += 1

    return col_num


def save_to_excel(runs_dictionary, selection_func_name, encode_type, p_m, p_c, p: Population):
    path = "data/Report" + "/" + str(
        N) + "/" + selection_func_name + "/" + encode_type.value + "/" + f"p_m_{p_m}" + f"__p_c_{p_c}"

    if not os.path.exists(path):
        os.makedirs(path)

    workbook = xlsxwriter.Workbook(
        path + "/" + selection_func_name + "_" + str(N) + f"_data_{encode_type.value}__p_m_{p_m}__p_c_{p_c}.xlsx"
    )
    worksheet = workbook.add_worksheet()
    worksheet.name = str(N)
    func_num = 1
    items_len = len(runs_dictionary)
    merge_format = workbook.add_format(
        {"bold": 1, "border": 1, "align": "center", "fg_color": "yellow"}
    )

    for func_name, runs_stats in runs_dictionary.items():
        worksheet.write(func_num + 1, 0, func_name)
        worksheet.write(func_num + items_len + 3, 0, func_name)
        last_col_num = 1
        i = 0

        for run in runs_stats.runs:
            start_range = last_col_num
            last_col_num = save_to_excel_internal(
                worksheet,
                run.pressure_stats.as_dict(),
                last_col_num,
                func_num + 1,
                func_num == 1,
            )
            last_col_num = save_to_excel_internal(
                worksheet,
                run.reproduction_stats.as_dict(),
                last_col_num,
                func_num + 1,
                func_num == 1,
            )
            last_col_num = save_to_excel_internal(
                worksheet,
                run.selection_diff_stats.as_dict(),
                last_col_num,
                func_num + 1,
                func_num == 1,
            )
            i = i + 1
            if func_num == 1:
                worksheet.merge_range(
                    0, start_range, 0, last_col_num - 1, "Run " + str(i), merge_format
                )

        start_range = last_col_num
        last_col_num = save_to_excel_internal(
            worksheet, runs_stats.as_dict(), last_col_num, func_num + 1, func_num == 1
        )
        if func_num == 1:
            worksheet.merge_range(
                0, start_range, 0, last_col_num - 1, "Avg values", merge_format
            )
        last_col_num = save_to_excel_internal(
            worksheet, runs_stats.as_dict(), 1, func_num + items_len + 3, func_num == 1
        )
        if func_num == 1:
            worksheet.merge_range(
                func_num + items_len + 1,
                1,
                func_num + items_len + 1,
                last_col_num - 1,
                "Avg values",
                merge_format,
            )

        func_num = func_num + 1

    worksheet.write(func_num + items_len + 5, 0, "Chromosomes codes")
    worksheet.write(func_num + items_len + 5, 1, ", ".join([str(list(c.code)) for c in p.chromosomes]))

    worksheet.write(func_num + items_len + 6, 0, "Fitness list")
    worksheet.write(func_num + items_len + 6, 1, ", ".join([str(fitness) for fitness in p.fitness_list]))

    worksheet.write(func_num + items_len + 7, 0, "Genotypes list")
    worksheet.write(func_num + items_len + 7, 1, ", ".join([str(gen) for gen in p.genotypes_list]))

    workbook.close()


def save_noise_to_excel(runs_dictionary, selection_func_name):
    path = "data/Report" + "/" + str(N) + "/" + selection_func_name

    if not os.path.exists(path):
        os.makedirs(path)

    workbook = xlsxwriter.Workbook(
        path + "/" + selection_func_name + "_" + str(N) + ".xlsx"
    )
    worksheet = workbook.add_worksheet()
    worksheet.name = str(N)
    func_num = 1
    items_len = len(runs_dictionary)
    merge_format = workbook.add_format(
        {"bold": 1, "border": 1, "align": "center", "fg_color": "yellow"}
    )

    for func_name, runs_stats in runs_dictionary.items():
        worksheet.write(func_num + 1, 0, func_name)
        worksheet.write(func_num + items_len + 3, 0, func_name)
        last_col_num = 1
        i = 0

        for run in runs_stats.runs:
            start_range = last_col_num
            last_col_num = save_to_excel_internal(
                worksheet,
                run.as_dict(),
                last_col_num,
                func_num + 1,
                func_num == 1,
            )
            i = i + 1
            if func_num == 1:
                worksheet.merge_range(
                    0, start_range, 0, last_col_num - 1, "Run " + str(i), merge_format
                )

        start_range = last_col_num
        last_col_num = save_to_excel_internal(
            worksheet,
            runs_stats.as_noise_dict(),
            last_col_num,
            func_num + 1,
            func_num == 1,
        )
        if func_num == 1:
            worksheet.merge_range(
                0, start_range, 0, last_col_num - 1, "Avg values", merge_format
            )
        last_col_num = save_to_excel_internal(
            worksheet,
            runs_stats.as_noise_dict(),
            1,
            func_num + items_len + 3,
            func_num == 1,
        )
        if func_num == 1:
            worksheet.merge_range(
                func_num + items_len + 1,
                1,
                func_num + items_len + 1,
                last_col_num - 1,
                "Avg values",
                merge_format,
            )

        func_num = func_num + 1

    workbook.close()


def save_avg_to_excel(func_runs_dictionary, noise_runs_dictionary):
    path = "data/Report" + "/" + str(N) + "/" + "AVG"
    if not os.path.exists(path):
        os.makedirs(path)
    workbook = xlsxwriter.Workbook(path + "/average.xlsx")
    worksheet = workbook.add_worksheet()
    worksheet.name = str(N)
    merge_format = workbook.add_format(
        {"bold": 1, "border": 1, "align": "center", "fg_color": "yellow"}
    )
    row = 1
    for fitness_func, runs_dictionary in func_runs_dictionary.items():
        func_num = 1
        for func_name, runs_stats in runs_dictionary.items():
            worksheet.write(row + 1, 0, func_name)
            last_col_num = save_to_excel_internal(
                worksheet, runs_stats.as_dict(), 1, row + 1, func_num == 1
            )
            if func_num == 1:
                worksheet.merge_range(
                    row - 1, 1, row - 1, last_col_num - 1, fitness_func, merge_format
                )
            func_num = func_num + 1
            row = row + 1
        row = row + 3
    for fitness_func, runs_dictionary in noise_runs_dictionary.items():
        func_num = 1
        for func_name, runs_stats in runs_dictionary.items():
            worksheet.write(row + 1, 0, func_name)
            last_col_num = save_to_excel_internal(
                worksheet, runs_stats.as_noise_dict(), 1, row + 1, func_num == 1
            )
            if func_num == 1:
                worksheet.merge_range(
                    row - 1, 1, row - 1, last_col_num - 1, fitness_func, merge_format
                )
            func_num = func_num + 1
            row = row + 1
        row = row + 3
    workbook.close()
