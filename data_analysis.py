import json
import numpy as np
import matplotlib.pyplot as plt

my_json_data = open("mars_rems_data.json", "r")
data = json.loads(my_json_data.read())

sols = []

min_air_temp_data = []
max_air_temp_data = []

min_ground_temp_data = []
max_ground_temp_data = []

radiation_leves_data = []
radiation_levels = {
    None: None,
    'UV Radiation level low': 1,
    'UV Radiation level moderated': 2,
    'UV Radiation level high': 3,
    'UV Radiation level very high': 4,
}


for i in range(len(data)+1):
    try:
        min_air_temp_data.append(int(data[str(i)]['air_temp_min']))
        max_air_temp_data.append(int(data[str(i)]['air_temp_max']))

        min_ground_temp_data.append(int(data[str(i)]['ground_temp_min']))
        max_ground_temp_data.append(int(data[str(i)]['ground_temp_max']))

        radiation_leves_data.append(data[str(i)]['radiation_level'])
        sols.append(i)
    except KeyError:
        sols.append(i)
        min_air_temp_data.append(None)
        max_air_temp_data.append(None)

        min_ground_temp_data.append(None)
        max_ground_temp_data.append(None)

        radiation_leves_data.append(None)


# Air temperature plot
def create_air_temp_plot():
    plt.title("Air temperature on Mars (REMS)")
    plt.ylabel('Air temperature (C)')
    plt.xlabel('Sol')
    plt.grid(True)
    plt.plot(sols, min_air_temp_data, 'b', max_air_temp_data, 'r')
    plt.axis([0, len(sols), -100, 30])
    plt.show()

# Ground temperature plot
def create_ground_temp_plot():
    plt.title("Ground temperature on Mars (REMS)")
    plt.ylabel('Ground temperature (C)')
    plt.xlabel('Sol')
    plt.grid(True)
    plt.plot(sols, min_ground_temp_data, 'b', max_ground_temp_data, 'r')
    plt.axis([0, len(sols), -140, 30])
    plt.show()


def filter_data(data):
    air_temp_min_filetered_data = []
    for i in range(len(data)):
        if data[i] != None:
            air_temp_min_filetered_data.append(data[i])
    return air_temp_min_filetered_data


min_air_temp_filtered = filter_data(min_air_temp_data)
max_air_temp_filtered = filter_data(max_air_temp_data)
def print_percentiles(data):
    print("25% population below: " + str(np.percentile(data, 25)))
    print("50% population below: " + str(np.percentile(data, 50)))
    print("75% population below: " + str(np.percentile(data, 75)))
    print("100% population below: " + str(np.percentile(data, 100)))


print("Min air temp:")
print_percentiles(min_air_temp_filtered)
print("Max air temp:")
print_percentiles(max_air_temp_filtered)
create_air_temp_plot()

plt.hist(min_air_temp_filtered, 50, density=1, facecolor='b', alpha=0.75)
plt.show()
