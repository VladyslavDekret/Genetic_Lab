import matplotlib.pyplot as plt
from constants import N
import os


def save_line_plot(encode_type, p_m, p_c, func_name, data, png_name, y_label, iteration, file_name, ylim=None):
    path = "data/Report" + "/" + str(
        N) + "/" + file_name + "/" + encode_type.value + "/" + f"p_m_{p_m}" + f"__p_c_{p_c}" + "/" + func_name + "/" + str(
        iteration)

    if not os.path.exists(path):
        os.makedirs(path)

    x = list(range(1, len(data) + 1))
    plt.plot(x, data, label=func_name)
    plt.ylabel(y_label)
    plt.xlabel("generation")

    if ylim:
        plt.ylim(ylim[0], ylim[1])

    plt.legend()
    plt.savefig(path + "/" + png_name + ".png")
    plt.close()


def save_lines_plot(
        encode_type, p_m, p_c, func_name, data_arr, label_arr, png_name, y_label, iteration, file_name, ylim=None
):
    path = "data/Report" + "/" + str(
        N) + "/" + file_name + "/" + encode_type.value + "/" + f"p_m_{p_m}" + f"__p_c_{p_c}" + "/" + func_name + "/" + str(
        iteration)

    if not os.path.exists(path):
        os.makedirs(path)

    for i in range(0, len(data_arr)):
        data = data_arr[i]
        label = label_arr[i]
        x = list(range(1, len(data) + 1))
        plt.plot(x, data, label=label)

    if ylim:
        plt.ylim(ylim[0], ylim[1])

    plt.ylabel(y_label)
    plt.xlabel("generation")
    plt.legend()
    plt.savefig(path + "/" + png_name + ".png")
    plt.close()
