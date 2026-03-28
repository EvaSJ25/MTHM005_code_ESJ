#Code for emission rate plots and total emission plots for comparing the different source resolutions
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm, LinearSegmentedColormap
import pandas as pd
from matplotlib.dates import DateFormatter, AutoDateLocator
import matplotlib.cm as cm
from matplotlib.colors import TwoSlopeNorm
from itertools import combinations
import math

#The definition structure below was provided by AI 
def parse_file(filename):
    names_values = {}
    matrix = []
    row_labels = []
    col_labels = []

    with open(filename, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    # Separate key-value lines and matrix lines
    kv_lines = []
    matrix_lines = []
    matrix_started = False

    for line in lines:
        if ":" in line and not matrix_started:
            kv_lines.append(line)
        else:
            matrix_started = True
            matrix_lines.append(line)

    # Process key-value pairs
    for line in kv_lines:
        parts = line.split(":", 1)
        if len(parts) == 2:
            key = parts[0].strip()
            val = parts[1].strip()
            # Try to convert val to number if possible
            try:
                val = float(val)
            except ValueError:
                pass
            names_values[key] = val

    # Process matrix (comma-separated, first row and column are labels)
    if matrix_lines:
        split_lines = [row.split(",") for row in matrix_lines]
        col_labels = [c.strip() for c in split_lines[0][1:]]  # skip first empty cell
        for row in split_lines[1:]:
            row_labels.append(row[0].strip())
            matrix.append([float(x.strip()) for x in row[1:]])
            
            ###Below is code Eva Siney Jones (ESJ) has written for this function
            matrix1=np.array(matrix)
            num_h1=int(names_values['Number of heights']) #gives number of height intervals 
            num_t1=int(names_values['Number of times per day']) #gives number of time intervals
            t_int1=24/num_t1 #calculates the time intervals
            h_int1=24/num_h1 #calculates the height intervals
            matrix_vals=matrix1[:,:num_h1] #outputs the emission rate matrix from InTEM
            matrix_tot_1=np.multiply(60*60*t_int1,matrix_vals) #creates matrix to find total emission by multiplying all emission rates by 60*60*time_interval to give total emission (g) in the in time interval
            matrix_tot=matrix_tot_1.sum(axis=1) #finds total amount (g) emitted over all height columns for each time period (e.g. total amount emitted over all heights for each time period)
            matrix_rate_emissions1=matrix_tot/(t_int1) #finds emission rate (g/hr) over all height columns for each time interval
            matrix_rate_emissions2=matrix_rate_emissions1[0:int(num_t1)] #focuses on the first day 03/11/2021 00:00 UTC to second day 04/11/2021 00:00 UTC (nothing happens past this for this case study so later times ignored)
            matrix_rate_emissions=np.asarray(matrix_rate_emissions2).flatten()
            y_step=np.r_[matrix_rate_emissions2[0], matrix_rate_emissions] #enables plotting steps in emission rate plots
    return names_values, matrix_vals, matrix_tot, matrix_rate_emissions, y_step

#Below labels the InTEM files for the 4 km 3 hour resolution (adapted code from AI output)
obs2_202111031200_4km3hr="InTEM_files/202111031200_obs2_emission_4km3hr.txt"
obs2_202111031800_4km3hr="InTEM_files/202111031800_obs2_emission_4km3hr.txt"
obs2_202111040000_4km3hr="InTEM_files/202111040000_obs2_emission_4km3hr.txt"
obs2_202111040600_4km3hr="InTEM_files/202111040600_obs2_emission_4km3hr.txt"
obs2_202111041200_4km3hr="InTEM_files/202111041200_obs2_emission_4km3hr.txt"
obs2_202111041800_4km3hr="InTEM_files/202111041800_obs2_emission_4km3hr.txt"
obs2_202111050000_4km3hr="InTEM_files/202111050000_obs2_emission_4km3hr.txt"
obs2_202111050600_4km3hr="InTEM_files/202111050600_obs2_emission_4km3hr.txt"
obs2_202111051200_4km3hr="InTEM_files/202111051200_obs2_emission_4km3hr.txt"
obs2_202111051800_4km3hr="InTEM_files/202111051800_obs2_emission_4km3hr.txt"
apriori_031200_4km3hr="InTEM_files/apriori_intem_CrossCorr_4km3hr_obs2.txt" 

#Finds the emission rates and total emissions for each InTEM run. Note names_values also returns the names of the categories found in the InTEM files (adapted code from AI output)
names_values_031200_obs2_4km3hr, matrix_031200_obs2_4km3hr, total_matrix_031200_obs2_4km3hr, rate_matrix_031200_obs2_4km3hr, y_steps_031200_4km3hr = parse_file(obs2_202111031200_4km3hr)
names_values_031800_obs2_4km3hr, matrix_031800_obs2_4km3hr, total_matrix_031800_obs2_4km3hr, rate_matrix_031800_obs2_4km3hr, y_steps_031800_4km3hr = parse_file(obs2_202111031800_4km3hr)
names_values_040000_obs2_4km3hr, matrix_040000_obs2_4km3hr, total_matrix_040000_obs2_4km3hr, rate_matrix_040000_obs2_4km3hr, y_steps_040000_4km3hr = parse_file(obs2_202111040000_4km3hr)
names_values_040600_obs2_4km3hr, matrix_040600_obs2_4km3hr, total_matrix_040600_obs2_4km3hr, rate_matrix_040600_obs2_4km3hr, y_steps_040600_4km3hr = parse_file(obs2_202111040600_4km3hr)
names_values_041200_obs2_4km3hr, matrix_041200_obs2_4km3hr, total_matrix_041200_obs2_4km3hr, rate_matrix_041200_obs2_4km3hr, y_steps_041200_4km3hr = parse_file(obs2_202111041200_4km3hr)
names_values_041800_obs2_4km3hr, matrix_041800_obs2_4km3hr, total_matrix_041800_obs2_4km3hr, rate_matrix_041800_obs2_4km3hr, y_steps_041800_4km3hr = parse_file(obs2_202111041800_4km3hr)
names_values_050000_obs2_4km3hr, matrix_050000_obs2_4km3hr, total_matrix_050000_obs2_4km3hr, rate_matrix_050000_obs2_4km3hr, y_steps_050000_4km3hr = parse_file(obs2_202111050000_4km3hr)
names_values_050600_obs2_4km3hr, matrix_050600_obs2_4km3hr, total_matrix_050600_obs2_4km3hr, rate_matrix_050600_obs2_4km3hr, y_steps_050600_4km3hr = parse_file(obs2_202111050600_4km3hr)
names_values_051200_obs2_4km3hr, matrix_051200_obs2_4km3hr, total_matrix_051200_obs2_4km3hr, rate_matrix_051200_obs2_4km3hr, y_steps_051200_4km3hr = parse_file(obs2_202111051200_4km3hr)
names_values_051800_obs2_4km3hr, matrix_051800_obs2_4km3hr, total_matrix_051800_obs2_4km3hr, rate_matrix_051800_obs2_4km3hr, y_steps_051800_4km3hr = parse_file(obs2_202111051800_4km3hr)
names_values_prior_obs2_4km3hr, matrix_prior_obs2_4km3hr, total_matrix_prior_obs2_4km3hr, rate_matrix_prior_obs2_4km3hr, y_steps_prior_4km3hr = parse_file(apriori_031200_4km3hr)

#Below labels the InTEM files for the 4 km 2 hour resolution (adapted code from AI output)
obs2_202111031200_4km2hr="InTEM_files/202111031200_obs2_emission_4km2hr.txt"
obs2_202111031800_4km2hr="InTEM_files/202111031800_obs2_emission_4km2hr.txt"
obs2_202111040000_4km2hr="InTEM_files/202111040000_obs2_emission_4km2hr.txt"
obs2_202111040600_4km2hr="InTEM_files/202111040600_obs2_emission_4km2hr.txt"
obs2_202111041200_4km2hr="InTEM_files/202111041200_obs2_emission_4km2hr.txt"
obs2_202111041800_4km2hr="InTEM_files/202111041800_obs2_emission_4km2hr.txt"
obs2_202111050000_4km2hr="InTEM_files/202111050000_obs2_emission_4km2hr.txt"
obs2_202111050600_4km2hr="InTEM_files/202111050600_obs2_emission_4km2hr.txt"
obs2_202111051200_4km2hr="InTEM_files/202111051200_obs2_emission_4km2hr.txt"
obs2_202111051800_4km2hr="InTEM_files/202111051800_obs2_emission_4km2hr.txt"
apriori_031200_4km2hr="InTEM_files/apriori_intem_CrossCorr_4km2hr_obs2.txt" 

#Finds the emission rates and total emissions for each InTEM run. Note names_values also returns the names of the categories found in the InTEM files (adapted code from AI output)
names_values_031200_obs2_4km2hr, matrix_031200_obs2_4km2hr, total_matrix_031200_obs2_4km2hr, rate_matrix_031200_obs2_4km2hr, y_steps_031200_4km2hr = parse_file(obs2_202111031200_4km2hr)
names_values_031800_obs2_4km2hr, matrix_031800_obs2_4km2hr, total_matrix_031800_obs2_4km2hr, rate_matrix_031800_obs2_4km2hr, y_steps_031800_4km2hr = parse_file(obs2_202111031800_4km2hr)
names_values_040000_obs2_4km2hr, matrix_040000_obs2_4km2hr, total_matrix_040000_obs2_4km2hr, rate_matrix_040000_obs2_4km2hr, y_steps_040000_4km2hr = parse_file(obs2_202111040000_4km2hr)
names_values_040600_obs2_4km2hr, matrix_040600_obs2_4km2hr, total_matrix_040600_obs2_4km2hr, rate_matrix_040600_obs2_4km2hr, y_steps_040600_4km2hr = parse_file(obs2_202111040600_4km2hr)
names_values_041200_obs2_4km2hr, matrix_041200_obs2_4km2hr, total_matrix_041200_obs2_4km2hr, rate_matrix_041200_obs2_4km2hr, y_steps_041200_4km2hr = parse_file(obs2_202111041200_4km2hr)
names_values_041800_obs2_4km2hr, matrix_041800_obs2_4km2hr, total_matrix_041800_obs2_4km2hr, rate_matrix_041800_obs2_4km2hr, y_steps_041800_4km2hr = parse_file(obs2_202111041800_4km2hr)
names_values_050000_obs2_4km2hr, matrix_050000_obs2_4km2hr, total_matrix_050000_obs2_4km2hr, rate_matrix_050000_obs2_4km2hr, y_steps_050000_4km2hr = parse_file(obs2_202111050000_4km2hr)
names_values_050600_obs2_4km2hr, matrix_050600_obs2_4km2hr, total_matrix_050600_obs2_4km2hr, rate_matrix_050600_obs2_4km2hr, y_steps_050600_4km2hr = parse_file(obs2_202111050600_4km2hr)
names_values_051200_obs2_4km2hr, matrix_051200_obs2_4km2hr, total_matrix_051200_obs2_4km2hr, rate_matrix_051200_obs2_4km2hr, y_steps_051200_4km2hr = parse_file(obs2_202111051200_4km2hr)
names_values_051800_obs2_4km3hr, matrix_051800_obs2_4km2hr, total_matrix_051800_obs2_4km2hr, rate_matrix_051800_obs2_4km2hr, y_steps_051800_4km2hr = parse_file(obs2_202111051800_4km2hr)
names_values_prior_obs2_4km2hr, matrix_prior_obs2_4km2hr, total_matrix_prior_obs2_4km2hr, rate_matrix_prior_obs2_4km2hr, y_steps_prior_4km2hr = parse_file(apriori_031200_4km2hr)

#Below labels the InTEM files for the 2 km 1 hour resolution (that utilises the last hour of observations) (adapted code from AI output)
obs2_202111031200_2km1hr="InTEM_files/2km1hr_with_202111031200_obs2.txt"
obs2_202111031800_2km1hr="InTEM_files/2km1hr_with_202111031800_obs2.txt"
obs2_202111040000_2km1hr="InTEM_files/2km1hr_with_202111040000_obs2.txt"
obs2_202111040600_2km1hr="InTEM_files/2km1hr_with_202111040600_obs2.txt"
obs2_202111041200_2km1hr="InTEM_files/2km1hr_with_202111041200_obs2.txt"
obs2_202111041800_2km1hr="InTEM_files/2km1hr_with_202111041800_obs2.txt"
obs2_202111050000_2km1hr="InTEM_files/2km1hr_with_202111050000_obs2.txt"
obs2_202111050600_2km1hr="InTEM_files/2km1hr_with_202111050600_obs2.txt"
obs2_202111051200_2km1hr="InTEM_files/2km1hr_with_202111051200_obs2.txt"
obs2_202111051800_2km1hr="InTEM_files/2km1hr_with_202111051800_obs2.txt"
obs2_prior_2km1hr="InTEM_files/apriori_intem_CrossCorr_2km1hr_obs2.txt"

#Finds the emission rates and total emissions for each InTEM run. Note names_values also returns the names of the categories found in the InTEM files (adapted code from AI output)
names_values_031200_obs2_2km1hr, matrix_031200_obs2_2km1hr, total_matrix_031200_obs2_2km1hr, rate_matrix_031200_obs2_2km1hr, y_steps_031200_2km1hr = parse_file(obs2_202111031200_2km1hr)
names_values_031800_obs2_2km1hr, matrix_031800_obs2_2km1hr, total_matrix_031800_obs2_2km1hr, rate_matrix_031800_obs2_2km1hr, y_steps_031800_2km1hr  = parse_file(obs2_202111031800_2km1hr)
names_values_040000_obs2_2km1hr, matrix_040000_obs2_2km1hr, total_matrix_040000_obs2_2km1hr, rate_matrix_040000_obs2_2km1hr, y_steps_040000_2km1hr  = parse_file(obs2_202111040000_2km1hr)
names_values_040600_obs2_2km1hr, matrix_040600_obs2_2km1hr, total_matrix_040600_obs2_2km1hr, rate_matrix_040600_obs2_2km1hr, y_steps_040600_2km1hr  = parse_file(obs2_202111040600_2km1hr)
names_values_041200_obs2_2km1hr, matrix_041200_obs2_2km1hr, total_matrix_041200_obs2_2km1hr, rate_matrix_041200_obs2_2km1hr, y_steps_041200_2km1hr  = parse_file(obs2_202111041200_2km1hr)
names_values_041800_obs2_2km1hr, matrix_041800_obs2_2km1hr, total_matrix_041800_obs2_2km1hr, rate_matrix_041800_obs2_2km1hr, y_steps_041800_2km1hr  = parse_file(obs2_202111041800_2km1hr)
names_values_050000_obs2_2km1hr, matrix_050000_obs2_2km1hr, total_matrix_050000_obs2_2km1hr, rate_matrix_050000_obs2_2km1hr, y_steps_050000_2km1hr  = parse_file(obs2_202111050000_2km1hr)
names_values_050600_obs2_2km1hr, matrix_050600_obs2_2km1hr, total_matrix_050600_obs2_2km1hr, rate_matrix_050600_obs2_2km1hr, y_steps_050600_2km1hr  = parse_file(obs2_202111050600_2km1hr)
names_values_051200_obs2_2km1hr, matrix_051200_obs2_2km1hr, total_matrix_051200_obs2_2km1hr, rate_matrix_051200_obs2_2km1hr, y_steps_051200_2km1hr  = parse_file(obs2_202111051200_2km1hr)
names_values_051800_obs2_2km1hr, matrix_051800_obs2_2km1hr, total_matrix_051800_obs2_2km1hr, rate_matrix_051800_obs2_2km1hr, y_steps_051800_2km1hr  = parse_file(obs2_202111051800_2km1hr)
names_values_prior_obs2_2km1hr, matrix_prior_obs2_2km1hr, total_matrix_prior_obs2_2km1hr, rate_matrix_prior_obs2_2km1hr, y_steps_prior_2km1hr  = parse_file(obs2_prior_2km1hr)

###Below is code ESJ has written
num_h_4km3hr=int(names_values_031200_obs2_4km3hr['Number of heights']) #gives number of heights (e.g. 6 at 4km each)
num_t_4km3hr=int(names_values_031200_obs2_4km3hr['Number of times per day']) #gives number of time intervals (e.g. 8 at 3hrs each)

t_int_4km3hr=24/num_t_4km3hr #calculates the time intervals for 4km3hr case
h_int_4km3hr=24/num_h_4km3hr #calculates the height intervals for 4km3hr case

num_h_4km2hr=int(names_values_031200_obs2_4km2hr['Number of heights']) #gives number of heights (e.g. 6 at 4km each)
num_t_4km2hr=int(names_values_031200_obs2_4km2hr['Number of times per day']) #gives number of time intervals (e.g. 24 at 2hrs each)

t_int_4km2hr=24/num_t_4km2hr #calculates the time intervals for 4km2hr case
h_int_4km2hr=24/num_h_4km2hr #calculates the height intervals for 4km2hr case


num_h_2km1hr=int(names_values_031200_obs2_2km1hr['Number of heights']) #gives number of heights (e.g. 12 at 2km each)
num_t_2km1hr=int(names_values_031200_obs2_2km1hr['Number of times per day']) #gives number of time intervals (e.g. 24 at 1hrs each)

t_int_2km1hr=24/num_t_2km1hr #calculates the time intervals for 2km1hr case
h_int_2km1hr=24/num_h_2km1hr #calculates the height intervals for 2km1hr case

#Creates time and date labels
start = pd.Timestamp('2021-11-03 00:00')
end = pd.Timestamp('2021-11-04 00:00')
time_labels_4km3hr = pd.date_range(start, end, freq='3h')  # every 3 hours it adds a time label
time_labels_4km2hr = pd.date_range(start, end, freq='2h')  # every 2 hours it adds a time label
time_labels_2km1hr = pd.date_range(start, end, freq='1h')  # every 1 hour it adds a time label

#Finds ends of each time interval for the different resolutions
delta_t_4km3hr=pd.Timedelta(hours=round(t_int_4km3hr))
t_edges_4km3hr = pd.date_range(start=start, periods=num_t_4km3hr+1, freq=delta_t_4km3hr)

delta_t_4km2hr=pd.Timedelta(hours=round(t_int_4km2hr))
t_edges_4km2hr = pd.date_range(start=start, periods=num_t_4km2hr+1, freq=delta_t_4km2hr)

delta_t_2km1hr=pd.Timedelta(hours=round(t_int_2km1hr))
t_edges_2km1hr = pd.date_range(start=start, periods=num_t_2km1hr+1, freq=delta_t_2km1hr)


#Produces labels for each 3 hourly interval 
labels = [
    t.strftime('%d/%m \n%H:%M') if i % 3 == 0 else ''
    for i, t in enumerate(time_labels_2km1hr)
]

###Plot emission rates
fig1, ax1=plt.subplots(figsize=(7,7),constrained_layout=True)
ax1.step(time_labels_2km1hr,y_steps_031200_2km1hr, lw=2.5,label='2km1hr run')
ax1.step(time_labels_4km2hr,y_steps_031200_4km2hr, lw=2.5,label='4km2hr run')
ax1.step(time_labels_4km3hr,y_steps_031200_4km3hr, lw=2.5,label='4km3hr run')
ax1.grid(True, alpha=0.3)
ax1.yaxis.get_offset_text().set_fontsize(15)
ax1.tick_params(axis='y', labelsize=15)
ax1.set_xticks(time_labels_4km3hr)
ax1.set_xticklabels(time_labels_4km3hr.strftime('%d/%m \n%H:%M'), fontsize=15)
plt.legend(fontsize=12)  # Show labels
plt.title("Run 1", fontsize=25)
plt.xlabel("Date", fontsize=20)
plt.ylabel("Emission rate (g/hr)", fontsize=20)


fig2, ax2=plt.subplots(figsize=(7,7),constrained_layout=True)
ax2.step(time_labels_2km1hr,y_steps_031800_2km1hr, lw=2.5,label='2km1hr run')
ax2.step(time_labels_4km2hr,y_steps_031800_4km2hr, lw=2.5,label='4km2hr run')
ax2.step(time_labels_4km3hr,y_steps_031800_4km3hr, lw=2.5,label='4km3hr run')
ax2.grid(True, alpha=0.3)
ax2.yaxis.get_offset_text().set_fontsize(15)
ax2.tick_params(axis='y', labelsize=15)
ax2.set_xticks(time_labels_4km3hr)
ax2.set_xticklabels(time_labels_4km3hr.strftime('%d/%m \n%H:%M'), fontsize=15)
plt.legend(fontsize=12)  # Show labels
plt.title("Run 2", fontsize=25)
plt.xlabel("Date", fontsize=20)
plt.ylabel("Emission rate (g/hr)", fontsize=20)

fig3, ax3=plt.subplots(figsize=(7,7),constrained_layout=True)
ax3.step(time_labels_2km1hr,y_steps_040000_2km1hr, lw=2.5,label='2km1hr run')
ax3.step(time_labels_4km2hr,y_steps_040000_4km2hr, lw=2.5,label='4km2hr run')
ax3.step(time_labels_4km3hr,y_steps_040000_4km3hr, lw=2.5,label='4km3hr run')
ax3.grid(True, alpha=0.3)
ax3.yaxis.get_offset_text().set_fontsize(15)
ax3.tick_params(axis='y', labelsize=15)
ax3.set_xticks(time_labels_4km3hr)
ax3.set_xticklabels(time_labels_4km3hr.strftime('%d/%m \n%H:%M'), fontsize=15)
plt.legend(fontsize=12)  # Show labels
plt.title("Run 3", fontsize=25)
plt.xlabel("Date", fontsize=20)
plt.ylabel("Emission rate (g/hr)", fontsize=20)

fig4, ax4=plt.subplots(figsize=(7,7),constrained_layout=True)
ax4.step(time_labels_2km1hr,y_steps_040600_2km1hr, lw=2.5,label='2km1hr run')
ax4.step(time_labels_4km2hr,y_steps_040600_4km2hr, lw=2.5,label='4km2hr run')
ax4.step(time_labels_4km3hr,y_steps_040600_4km3hr, lw=2.5,label='4km3hr run')
ax4.grid(True, alpha=0.3)
ax4.yaxis.get_offset_text().set_fontsize(15)
ax4.tick_params(axis='y', labelsize=15)
ax4.set_xticks(time_labels_4km3hr)
ax4.set_xticklabels(time_labels_4km3hr.strftime('%d/%m \n%H:%M'), fontsize=15)
plt.legend(fontsize=12)  # Show labels
plt.title("Run 4", fontsize=25)
plt.xlabel("Date", fontsize=20)
plt.ylabel("Emission rate (g/hr)", fontsize=20)



#Below finds the total emissions after each time interval - in vector form
#### 031200 run (Run 1)
cumulative_e_4km3hr_031200=np.zeros((int(num_t_4km3hr+1), 1))
cumulative_e_4km3hr_031200[0]=0.0 #No emission at start 
cumulative_e_4km3hr_031200[1]=total_matrix_031200_obs2_4km3hr[0] #second component equals the total amount found after first time interval (3 hours)
for i in range(1,int(num_t_4km3hr)+1):
    cumulative_e_4km3hr_031200[i]=cumulative_e_4km3hr_031200[i-1]+total_matrix_031200_obs2_4km3hr[i-1]

cumulative_e_4km2hr_031200=np.zeros((int(num_t_4km2hr+1), 1))
cumulative_e_4km2hr_031200[0]=0.0 #No emission at start 
cumulative_e_4km2hr_031200[1]=total_matrix_031200_obs2_4km2hr[0] #second component equals the total amount found after first time interval (2 hours)
for i in range(1,int(num_t_4km2hr)+1):
    cumulative_e_4km2hr_031200[i]=cumulative_e_4km2hr_031200[i-1]+total_matrix_031200_obs2_4km2hr[i-1]

cumulative_e_2km1hr_031200=np.zeros((int(num_t_2km1hr+1), 1))
cumulative_e_2km1hr_031200[0]=0.0 #No emission at start 
cumulative_e_2km1hr_031200[1]=total_matrix_031200_obs2_2km1hr[0] #second component equals the total amount found after first time interval (1 hour)
for i in range(1,int(num_t_2km1hr)+1):
    cumulative_e_2km1hr_031200[i]=cumulative_e_2km1hr_031200[i-1]+total_matrix_031200_obs2_2km1hr[i-1]


#### 031800 run (Run 2)
cumulative_e_4km3hr_031800=np.zeros((int(num_t_4km3hr+1), 1))
cumulative_e_4km3hr_031800[0]=0.0 #No emission at start 
cumulative_e_4km3hr_031800[1]=total_matrix_031800_obs2_4km3hr[0] #second component equals the total amount found after first time interval 
for i in range(1,int(num_t_4km3hr)+1):
    cumulative_e_4km3hr_031800[i]=cumulative_e_4km3hr_031800[i-1]+total_matrix_031800_obs2_4km3hr[i-1]

cumulative_e_4km2hr_031800=np.zeros((int(num_t_4km2hr+1), 1))
cumulative_e_4km2hr_031800[0]=0.0
cumulative_e_4km2hr_031800[1]=total_matrix_031800_obs2_4km2hr[0]
for i in range(1,int(num_t_4km2hr)+1):
    cumulative_e_4km2hr_031800[i]=cumulative_e_4km2hr_031800[i-1]+total_matrix_031800_obs2_4km2hr[i-1]

cumulative_e_2km1hr_031800=np.zeros((int(num_t_2km1hr+1), 1))
cumulative_e_2km1hr_031800[0]=0.0
cumulative_e_2km1hr_031800[1]=total_matrix_031800_obs2_2km1hr[0]
for i in range(1,int(num_t_2km1hr)+1):
    cumulative_e_2km1hr_031800[i]=cumulative_e_2km1hr_031800[i-1]+total_matrix_031800_obs2_2km1hr[i-1]


##### 040000 run (Run 3)
cumulative_e_4km3hr_040000=np.zeros((int(num_t_4km3hr+1), 1))
cumulative_e_4km3hr_040000[0]=0.0 #No emission at start 
cumulative_e_4km3hr_040000[1]=total_matrix_040000_obs2_4km3hr[0]
for i in range(1,int(num_t_4km3hr)+1):
    cumulative_e_4km3hr_040000[i]=cumulative_e_4km3hr_040000[i-1]+total_matrix_040000_obs2_4km3hr[i-1]

cumulative_e_4km2hr_040000=np.zeros((int(num_t_4km2hr+1), 1))
cumulative_e_4km2hr_040000[0]=0.0
cumulative_e_4km2hr_040000[1]=total_matrix_040000_obs2_4km2hr[0]
for i in range(1,int(num_t_4km2hr)+1):
    cumulative_e_4km2hr_040000[i]=cumulative_e_4km2hr_040000[i-1]+total_matrix_040000_obs2_4km2hr[i-1]

cumulative_e_2km1hr_040000=np.zeros((int(num_t_2km1hr+1), 1))
cumulative_e_2km1hr_040000[0]=0.0
cumulative_e_2km1hr_040000[1]=total_matrix_040000_obs2_2km1hr[0]
for i in range(1,int(num_t_2km1hr)+1):
    cumulative_e_2km1hr_040000[i]=cumulative_e_2km1hr_040000[i-1]+total_matrix_040000_obs2_2km1hr[i-1]


#### 040600 run (Run 4)
cumulative_e_4km3hr_040600=np.zeros((int(num_t_4km3hr+1), 1))
cumulative_e_4km3hr_040600[0]=0.0 #No emission at start 
cumulative_e_4km3hr_040600[1]=total_matrix_040600_obs2_4km3hr[0]
for i in range(1,int(num_t_4km3hr)+1):
    cumulative_e_4km3hr_040600[i]=cumulative_e_4km3hr_040600[i-1]+total_matrix_040600_obs2_4km3hr[i-1]

cumulative_e_4km2hr_040600=np.zeros((int(num_t_4km2hr+1), 1))
cumulative_e_4km2hr_040600[0]=0.0
cumulative_e_4km2hr_040600[1]=total_matrix_040600_obs2_4km2hr[0]
for i in range(1,int(num_t_4km2hr)+1):
    cumulative_e_4km2hr_040600[i]=cumulative_e_4km2hr_040600[i-1]+total_matrix_040600_obs2_4km2hr[i-1]

cumulative_e_2km1hr_040600=np.zeros((int(num_t_2km1hr+1), 1))
cumulative_e_2km1hr_040600[0]=0.0
cumulative_e_2km1hr_040600[1]=total_matrix_040600_obs2_2km1hr[0]
for i in range(1,int(num_t_2km1hr)+1):
    cumulative_e_2km1hr_040600[i]=cumulative_e_2km1hr_040600[i-1]+total_matrix_040600_obs2_2km1hr[i-1]

#Produces labels for each 6 hourly interval 
labels2 = [
    t.strftime('%d/%m \n%H:%M') if i % 6 == 0 else ''
    for i, t in enumerate(time_labels_2km1hr)
]

###Plots total emission plots
fig5, ax5=plt.subplots(figsize=(7,7),constrained_layout=True)
ax5.plot(time_labels_2km1hr, cumulative_e_2km1hr_031200, lw=2.5,label='2km1hr')
ax5.plot(time_labels_4km2hr, cumulative_e_4km2hr_031200, lw=2.5,label='4km2hr')
ax5.plot(time_labels_4km3hr, cumulative_e_4km3hr_031200, lw=2.5,label='4km3hr')
ax5.yaxis.get_offset_text().set_fontsize(15)
ax5.tick_params(axis='y', labelsize=15)
ax5.set_xticks(time_labels_2km1hr)
ax5.set_xticklabels(labels2, fontsize=15)
plt.legend(fontsize=12)
plt.title("Run 1", fontsize=25)
plt.xlabel("Date", fontsize=20)
plt.ylabel("Total Emission (g)", fontsize=20)


fig6, ax6=plt.subplots(figsize=(7,7),constrained_layout=True)
ax6.plot(time_labels_2km1hr, cumulative_e_2km1hr_031800, lw=2.5,label='2km1hr')
ax6.plot(time_labels_4km2hr, cumulative_e_4km2hr_031800, lw=2.5,label='4km2hr')
ax6.plot(time_labels_4km3hr, cumulative_e_4km3hr_031800, lw=2.5,label='4km3hr')
ax6.yaxis.get_offset_text().set_fontsize(15)
ax6.tick_params(axis='y', labelsize=15)
ax6.set_xticks(time_labels_2km1hr)
ax6.set_xticklabels(labels2, fontsize=15)
plt.legend(fontsize=12)
plt.title("Run 2", fontsize=25)
plt.xlabel("Date", fontsize=20)
plt.ylabel("Total Emission (g)", fontsize=20)


fig7, ax7=plt.subplots(figsize=(7,7),constrained_layout=True)
ax7.plot(time_labels_2km1hr, cumulative_e_2km1hr_040000, lw=2.5,label='2km1hr')
ax7.plot(time_labels_4km2hr, cumulative_e_4km2hr_040000, lw=2.5,label='4km2hr')
ax7.plot(time_labels_4km3hr, cumulative_e_4km3hr_040000, lw=2.5,label='4km3hr')
ax7.yaxis.get_offset_text().set_fontsize(15)
ax7.tick_params(axis='y', labelsize=15)
ax7.set_xticks(time_labels_2km1hr)
ax7.set_xticklabels(labels2, fontsize=15)
plt.legend(fontsize=12)
plt.title("Run 3", fontsize=25)
plt.xlabel("Date", fontsize=20)
plt.ylabel("Total Emission (g)", fontsize=20)

fig8, ax8=plt.subplots(figsize=(7,7),constrained_layout=True)
ax8.plot(time_labels_2km1hr, cumulative_e_2km1hr_040600,lw=2.5, label='2km1hr')
ax8.plot(time_labels_4km2hr, cumulative_e_4km2hr_040600, lw=2.5,label='4km2hr')
ax8.plot(time_labels_4km3hr, cumulative_e_4km3hr_040600, lw=2.5,label='4km3hr')
ax8.yaxis.get_offset_text().set_fontsize(15)
ax8.tick_params(axis='y', labelsize=15)
ax8.set_xticks(time_labels_2km1hr)
ax8.set_xticklabels(labels2, fontsize=15)
plt.legend(fontsize=12)
plt.title("Run 4", fontsize=25)
plt.xlabel("Date", fontsize=20)
plt.ylabel("Total Emission (g)", fontsize=20)


plt.tight_layout()
plt.show()