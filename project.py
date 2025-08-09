# Feel free to add additional python files to this project and import
# them in this file. However, do not change the name of this file
# Avoid the names ms1check.py and ms2check.py as those file names
# are reserved for the autograder

# To run your project use:
#     python runproject.py

# This will ensure that your project runs the way it will run in the
# the test environment


# supports the use of csv library
import csv



# This function reads a csv file and return a list of lists
# each element of the returned list is a row in the csv file
# The first row is the header row
def read_csv_file(file_name):
    data_set = []
    with open(file_name, mode='r', encoding="utf-8-sig") as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            data_set.append(row)
    return data_set

# This function writes out a list of lists to a csv file
# each element of the list is a row in the csv file
# The first row is the header row
def write_csv_file(file_name, data_set):
    with open(file_name, mode='w', newline='', encoding="utf-8-sig") as file:
        csv_writer = csv.writer(file)
        for row in data_set:
            csv_writer.writerow(row)


# This main function is the function that the runner will call
# The function prototype cannot be changed
def main():

    # example to read the csv file
    athlete_bio_file = read_csv_file("olympic_athlete_bio.csv")

    # example to write the data back from csv file
    write_csv_file("new_olympic_athlete_bio.csv",athlete_bio_file)
