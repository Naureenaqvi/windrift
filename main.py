#************************************
# Written by: Naureen Naqvi
# Notes: Code for Win Drift.
# Copyright: Naureen Naqvi.
#************************************

import csv
import datetime
import psutil
import array as arr
import decimal
import numpy as np
import numbers as nums
import string
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats as st

#region flags
debugflag = 0

printvaluesflag = 0

showgraphs = 0

shownochangemessage = 0

runnative = 1

runcorresponding = 1
#endregion

#region constants

win_lev_input = "[0-9].[0-9].[0-9]"

win_lev_size = arr.array('i', [12, 1, 6, 3])

base_stat_value = 1.961

alpha = 0.5

alpha_kswn = 0.001

classification_function_sea_gen = 2

random_state_sea_gen = 112

noise_percentage_sea_gen = 0.28

#endregion
# region variables

datacsvpath = '\\\\127.0.0.1\\windrift_data\\19052022\\data source\\E2D5.csv'

datacsv = None

datasetcount = None

win_lev_size_sorted = None

win_Count = None

win_Min = None

win_Max = None

user_continue = 1

data_block = 0

count_of_columns = -1

x = []

y = []

data_column_array = []

data_position_array = []

data_value_array = []

ecdf_position_array = []

ecdf_value_array = []

drift_flag_values_mode_1 = []

drift_flag_labels_mode_1 = []

drift_flag_values_mode_2 = []

drift_flag_labels_mode_2 = []

dfcols = []

dfrows = []

# endregion

# Process to load source dataset

def loaddata(csvpath):
    with open(csvpath) as csvfile:
        global datacsv
        global datasetcount

        datacsv = csv.reader(csvfile, delimiter=',')
        datasetcount = sum(1 for row in datacsv)

        csvfile.close()

    return

# Main process to execute the program.

def mainthread():
    global user_continue
    global data_block
    global data_position_array
    global data_value_array
    global win_Max
    global x
    global y
    global dfcols
    global dfrows
    global count_of_columns

    with open(datacsvpath) as csvfile:

        tempdatacounter = csv.reader(csvfile, delimiter=',')

        datasetcount = sum(1 for row in tempdatacounter)

        tempdatacounter = None

        csvfile.close()

        data_position_array = arr.array('d')
        # data_value_array = arr.array('d')

    pd.set_option("display.max_rows", None, "display.max_columns", None)

    dfcols = pd.read_csv(datacsvpath, nrows=0)

    colcount = dfcols.shape[1]

    count_of_columns = colcount

    colindex = 0

    while colindex < colcount:
        data_column_array.append(dfcols.columns[colindex])

        colindex = colindex + 1

    dfrows = pd.read_csv(datacsvpath, header=None, skiprows=[0])

    colindex = 0

    counter = 1

    count_of_columns = colcount

    while counter <= colcount:

        if counter > 0:

            if counter <= win_Max:
                                
                windriftconsecutive(counter, colcount)

            if counter >= win_Max:
                print('corresponding comparison')

                windriftcorresponding(counter, colcount)

            print('_____________________________________')

        colindex = colindex + 1

        counter = counter + 1

    indexer = 0

    print('results for mode 1')

    while indexer < len(drift_flag_values_mode_1):
        print('dflag for ', drift_flag_labels_mode_1[indexer], ' : ', drift_flag_values_mode_1[indexer])

        indexer = indexer + 1

    indexer = 0

    print('*****************************')
    print('results for mode 2')

    while indexer < len(drift_flag_values_mode_2):
        print('dflag for ', drift_flag_labels_mode_2[indexer], ' : ', drift_flag_values_mode_2[indexer])

        indexer = indexer + 1

    return

# Calculate critical value based on x & y

def d_crit_two_way(arr1, arr2):
    return 1.36 * np.sqrt(len(arr1) ** -1 + len(arr2) ** -1)

# Calculate drift in x & y values. Drift is detected and calculated using d_stat and d_crit.

def calculate_drift(x_label, x_values, y_label, y_values, calcmode, dbcount, winlevel):
    driftflag = 0

    x_y = np.sort(np.concatenate((x_values, y_values)))

    x_y_label = x_label + ' VS ' + y_label

    print('Using TWEDD - Detecting change for ', x_y_label)

    x_cdf = [np.round(st.percentileofscore(x_values, samp) / 100, 1) for samp in x_y]
    y_cdf = [np.round(st.percentileofscore(y_values, samp) / 100, 1) for samp in x_y]

    if showgraphs == 1:

        strtitle = ''

        strlabelx = ''

        strlabely = '|F^(x)-G^(x)|'

        if dbcount == count_of_columns:

            strlabelx = 'x - All data points'

        else:

            strlabelx = 'x - ' + x_y_label

        strtitle = 'Mode:' + str(calcmode) + ', Win Level:' + str(winlevel) + ', Data block:' + str(dbcount)

        plt.rc('xtick', labelsize=10)

        plt.rc('ytick', labelsize=10)

        plt.plot(x_y, x_cdf, label='x', alpha=alpha, marker='^', color='black')

        plt.plot(x_y, y_cdf, label='y', alpha=alpha, marker='^', color='gray')

        plt.title(strtitle)

        plt.xlabel(strlabelx)

        plt.ylabel(strlabely)

        plt.show()

    abs_diff = np.abs(np.subtract(x_cdf, y_cdf))

    dcrittwoway = d_crit_two_way(x, y)

    # test 1
    if max(abs_diff) >= dcrittwoway:
        driftflag = 1

    x_y_label = 'dbcount : ' + str(dbcount) + ' win level ' + str(winlevel) + ' ' + x_y_label

    if calcmode == 1:

        drift_flag_labels_mode_1.append(x_y_label)

        drift_flag_values_mode_1.append(driftflag)

    elif calcmode == 2:

        drift_flag_labels_mode_2.append(x_y_label)

        drift_flag_values_mode_2.append(driftflag)

    if printvaluesflag == 1:

        print(x_y_label)

        print('d_stat: ', max(abs_diff))

        print('d_crit: ', dcrittwoway)

        print('drift flag: ', driftflag)

# mode 1
# process for evaluating two or more consecutive nodes within a dataset.
# example: Jan 2020 is evaluated against Feb 2020.

def windriftconsecutive(dbcount, maxcolcount):
    global x
    global y
    global dfrows

    #mark start of process
    print('dbcount : ', dbcount)

    # run for each window in the ordered array of windows
    for winlevel in win_lev_size_sorted:

        #initialise variables
        label_x = ''

        label_y = ''

        x = []

        y = []

        #print active window level being processed
        print('winlevel: ', winlevel)
        
        if runnative == 1:
            
            if winlevel == 1:
    
                if (dbcount < maxcolcount and dbcount < win_Max):
                    x = np.array(dfrows.iloc[:, dbcount - 1].values)
    
                    y = np.array(dfrows.iloc[:, dbcount].values)

                    label_x = data_column_array[dbcount - 1]
    
                    label_y = data_column_array[dbcount]
    
            elif dbcount % winlevel == 0 and dbcount > winlevel:
    
                datablockastart = dbcount - winlevel - winlevel + 1
    
                if datablockastart < 0:
                    datablockastart = 0
    
                datablockaend = (datablockastart) + (winlevel)
    
                datablockbstart = datablockaend
    
                datablockbend = datablockbstart + winlevel - 1
    
                index = datablockastart - 1
    
                while index < datablockaend - 1:
    
                    if (index == maxcolcount):
                        index = 1
    
                    x = np.concatenate((x, np.array(dfrows.iloc[:, index].values)))

                    if len(label_x) == 0:
    
                        if dbcount == maxcolcount:
    
                            labeldbcount = maxcolcount - 1
    
                        else:
    
                            labeldbcount = dbcount
    
                        label_x = data_column_array[index]
    
                    elif len(label_x) > 0:
    
                        label_x = label_x + ',' + data_column_array[index]
    
                    index = index + 1
    
                index = datablockbstart - 1
    
                while index <= (datablockbend - 1):
    
                    if (index == maxcolcount):
                        index = 1
    
                    y = np.concatenate((y, np.array(dfrows.iloc[:, index].values)))
    
                    if len(label_y) == 0:
    
                        label_y = data_column_array[index]
    
                    elif len(label_y) > 0:
    
                        label_y = label_y + ',' + data_column_array[index]
    
                    index = index + 1

        if len(x) > 0 and len(y) > 0 and len(label_x) > 0 and len(label_y) > 0:

            calculate_drift(label_x, x, label_y, y, 1, dbcount, winlevel)

#process for evaluating corressponding nodes within a dataset.
#example: Jan 2020 is evaluated against Jan 2021

def windriftcorresponding(dbcount, maxcolcount):
    global x
    global y
    global win_Max
    global dfrows

    #mark start of process

    if debugflag == 1:
        print('corresponding calculation')
        print('dbcount : ', dbcount)

    # run for each window in the ordered array of windows
    for winlevel in win_lev_size_sorted:

        #initialise variables
        label_x = ''

        label_y = ''

        x = []

        y = []

        index = 0

        localdbcount = dbcount - win_Max

        #print active window level being processed
        if debugflag == 1:
            print('winlevel: ', winlevel)

        if runcorresponding == 1:

            if winlevel == 1:

                if dbcount < maxcolcount:
                    x = np.array(dfrows.iloc[:, dbcount - win_Max].values)

                    y = np.array(dfrows.iloc[:, dbcount].values)

                    label_x = data_column_array[dbcount - win_Max]

                    label_y = data_column_array[dbcount]

            elif (localdbcount) % winlevel == 0 and (localdbcount) >= winlevel:

                datablockastart = dbcount - win_Max - winlevel + 1  # localdbcount - winlevel - winlevel + 1

                if datablockastart < 0:
                    datablockastart = 0

                datablockaend = (datablockastart) + (winlevel)

                datablockbstart = datablockastart + win_Max

                datablockbend = datablockbstart + winlevel - 1

                index = datablockastart - 1

                if index < 0:
                    index = 0

                while index < datablockaend - 1:

                    if (index == maxcolcount):
                        index = 1

                    x = np.concatenate((x, np.array(dfrows.iloc[:, index].values)))

                    if len(label_x) == 0:

                        if dbcount == maxcolcount:

                            labeldbcount = maxcolcount - 1

                        else:

                            labeldbcount = dbcount

                        label_x = data_column_array[index]

                    elif len(label_x) > 0:

                        label_x = label_x + ':' + data_column_array[index]

                    index = index + 1

                index = datablockbstart - 1

                while index <= (datablockbend - 1):

                    if (index == maxcolcount):
                        index = 1

                    y = np.concatenate((y, np.array(dfrows.iloc[:, index].values)))

                    if len(label_y) == 0:

                        label_y = data_column_array[index]

                    elif len(label_y) > 0:

                        label_y = label_y + ':' + data_column_array[index]

                    index = index + 1

        # process mode 2 if x, y values and their respective labels are not empty
        if len(x) > 0 and len(y) > 0 and len(label_x) > 0 and len(label_y) > 0:

            calculate_drift(label_x, x, label_y, y, 2, dbcount, winlevel)

if __name__ == '__main__':

    # read source data
    loaddata(datacsvpath)

    # sort window size
    win_lev_size_sorted = np.sort(win_lev_size)

    # set ordered window counts
    win_Count = win_lev_size_sorted.size

    # set min & max window sizes
    win_Min = np.amin(win_lev_size_sorted)

    win_Max = np.amax(win_lev_size_sorted)

    # print variables if debug flag is set to true

    if debugflag == 1:
        print('dataset: ', datacsvpath)
        print('win_lev_size:', win_lev_size)
        print('win_lev_size_sorted:', win_lev_size_sorted)
        print('win_Min:', win_Min)
        print('win_Max:', win_Max)
        print('win_Count:', win_Count)
        print('datasetcount:', datasetcount)

    mainthread()
