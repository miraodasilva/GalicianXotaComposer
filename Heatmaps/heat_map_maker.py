import os
import numpy as np
import subprocess


###
#SOME AUX FUNCTIONS
###
def get_stat(path,line_num):
	f = open(path,"r")
	lines = f.readlines()
	line = lines[line_num-1]
	name, value = line.split(":")
	name= name.lstrip()
	value = value.strip()
	value = float(value)
	return name,value


def get_name(rnn,rule_set):
	name = ""
	if "magenta/" in rnn:
		name+="1."
	elif "galician/" in rnn:
		name+="2."
	elif "magenta+galician/" in rnn:
		name+="3."
	if "zero_reward" in rule_set:
		name+="2"
	elif "original_rule_set" in rule_set:
		name+="3"
	elif "new_rule_set" in rule_set:
		name+="4"
	elif "both_rule_sets" in rule_set:
		name+="5"
	return name

#
#GETTING THE STATS FROM THE STAT FILES
#
relevant_lines_A = [16,17,18,19,20,22,23,24,33,36,40,41,47,49,51,53,55,57,59,67,69,71,73,75,77]
relevant_lines_B = [16,17,18,19,20,22,23,24,27,28,29,30,37,38,39,40,41,47,49,51,53,55,57,61,63,65,67,69,71,73,75,77]

section_list = ["section_A","section_B"]
relevant_rnns= ["magenta/","galician/","magenta+galician/"]
relevant_rule_sets_A = ["original_rule_set/","new_rule_set/section_A/","both_rule_sets/section_A/"]
relevant_rule_sets_B = ["original_rule_set/","new_rule_set/section_B/","both_rule_sets/section_B/"]

root = "/vol/gpudata/rs2517/venv1/myApp/outputs_revised/RL_TUNER_2/"
print("Root is: "+ root)
result_list = []
label_lists = []
for section in section_list:
	label_list = []
	config_list=[]
	for rnn in relevant_rnns:
		if section == "section_A":
			relevant_rule_sets= relevant_rule_sets_A
			relevant_lines = relevant_lines_A
		else:
			relevant_rule_sets= relevant_rule_sets_B
			relevant_lines = relevant_lines_B
		for rule_set in relevant_rule_sets:
			rule_list = []
			name = get_name(rnn,rule_set)
			label_list+=[name]
			diff_total = 0
			file_path = root + rnn + rule_set + "q/"
			#Get total number of notes and intervals
			pre_rl_notes = 0
			post_rl_notes = 0
			pre_rl_intervals = 0
			post_rl_intervals = 0
			for line in [26,27,28,29,30,32,33,34,35,36,37,38,39,40,41]:
				_,pre_rl_n = get_stat(file_path+"pre_rl_music_theory_stats.txt",line)
				_,post_rl_n = get_stat(file_path+"post_rl_music_theory_stats.txt",line)
				pre_rl_intervals += pre_rl_n
				post_rl_intervals += post_rl_n
			for line in [45,47,49,51,53,55,57]:
				_,pre_rl_n = get_stat(file_path+"pre_rl_music_theory_stats.txt",line)
				_,post_rl_n = get_stat(file_path+"post_rl_music_theory_stats.txt",line)
				pre_rl_notes += pre_rl_n
				post_rl_notes += post_rl_n
			#Get relevant lines
			for i,line in enumerate(relevant_lines):
				_,pre_rl_value = get_stat(file_path+"pre_rl_music_theory_stats.txt",line)
				_,post_rl_value = get_stat(file_path+"post_rl_music_theory_stats.txt",line)
				#since there are 3 autocorrelation stats we will average them
				if line in [22,23,24]:
					pre_rl_value = float(abs(pre_rl_value))/3.0
					post_rl_value = float(abs(post_rl_value))/3.0
				#Adjust the rules that were not measured in percentages (divide by number of notes or intervals depending on the nature of the rule)
				elif line in [53,55,57]:
					pre_rl_value /= pre_rl_notes
					post_rl_value /= post_rl_notes
				elif line in [40,41,75,77,33,36,41,27,28,29,30,37,38,39,40]:
					pre_rl_value /= pre_rl_intervals
					post_rl_value /= post_rl_intervals
				name,_ = get_stat(file_path+"pre_rl_music_theory_stats.txt",line)
				rule_list+=[(pre_rl_value*100,post_rl_value*100)]
			config_list += [rule_list]
	result_list+=[config_list]
	label_lists += [label_list]

#
#AGREGATE STATS INTO RULE SCORES
#

RNN_conversion = [[0],[1],[2],[3],[4],[5],[6],[7],[8]]
rule_conversion = [[17],[20],[40,41],[16],[22,23,24],[18],[19],[67],[69],[73],[75],[77]]
invert =            [1,   1,   0,      0,   1,         0,   0,   0,   0,   0,   0,    0]
rule_conversion_A = [[55,57],[33,36,41],[59]]
rule_conversion_B = [[53,55],[27,28,29,30,37,38,39,40],[63]]
new_results_pre= np.zeros((9,21))
new_results_post= np.zeros((9,21))

#both sections
for i,newline in enumerate(RNN_conversion):
	for j,newrule in enumerate(rule_conversion):
		for x in newline:
			for y in newrule:
				yA = relevant_lines_A.index(y)
				yB = relevant_lines_B.index(y)
				new_results_pre[i,j]+=(result_list[0][x][yA][0])/2
				new_results_pre[i,j]+=(result_list[1][x][yB][0])/2
				new_results_post[i,j]+=(result_list[0][x][yA][1])/2
				new_results_post[i,j]+=(result_list[1][x][yB][1])/2
				#Invert the percentage if necessary (ie we want notes not repeated rather than notes repeated)
		if invert[j]:
			new_results_pre[i,j] = 100 - new_results_pre[i,j]
			new_results_post[i,j] = 100 - new_results_post[i,j]
#sectionA
for i,newline in enumerate(RNN_conversion):
	for j,newrule in enumerate(rule_conversion_A):
		for x in newline:
			for y in newrule:
				yA = relevant_lines_A.index(y)
				new_results_pre[i,j+12]+=result_list[0][x][yA][0]
				new_results_post[i,j+12]+=result_list[0][x][yA][1]
#sectionB
for i,newline in enumerate(RNN_conversion):
	for j,newrule in enumerate(rule_conversion_B):
		for x in newline:
			for y in newrule:
				yB = relevant_lines_B.index(y)
				new_results_pre[i,j+15]+=result_list[1][x][yB][0]
				new_results_post[i,j+15]+=result_list[1][x][yB][1]

#Adding total scores to Pre-RL and Diffs
for i in range(9):
	magenta_total= 0
	xotas_total= 0
	total=0
	for j in range(7):
		magenta_total+= new_results_pre[i,j]
	for j in range(7,18):
		xotas_total+= new_results_pre[i,j]
	for j in range(18):
		total+= new_results_pre[i,j]
	magenta_avg = magenta_total / 7
	xotas_avg = xotas_total / 11
	avg = total / 18
	new_results_pre[i,18]=magenta_avg
	new_results_pre[i,19]=xotas_avg
	new_results_pre[i,20]=avg

for i in range(9):
	magenta_total= 0
	xotas_total= 0
	total=0
	for j in range(7):
		magenta_total+= new_results_post[i,j]
	for j in range(7,18):
		xotas_total+= new_results_post[i,j]
	for j in range(18):
		total+= new_results_post[i,j]
	magenta_avg = magenta_total / 7
	xotas_avg = xotas_total / 11
	avg = total / 18
	new_results_post[i,18]=magenta_avg
	new_results_post[i,19]=xotas_avg
	new_results_post[i,20]=avg

#Rounding values
for i,line in enumerate(new_results_pre):
	for j, col in enumerate(line):
		new_results_pre[i,j] = round(new_results_pre[i,j])
		new_results_post[i,j] = round(new_results_post[i,j])

#Adjusting Pre-RL to feature only 3 lines (1 for every RNN)
newer_results_pre = np.zeros((3,21))
newer_results_pre[0,:] = new_results_pre[0,:]
newer_results_pre[1,:] = new_results_pre[3,:]
newer_results_pre[2,:] = new_results_pre[6,:]
new_results_pre = newer_results_pre

ninex_new_results_pre = np.zeros((9,21))
ninex_new_results_pre[0,:] = newer_results_pre[0,:]
ninex_new_results_pre[1,:] = newer_results_pre[0,:]
ninex_new_results_pre[2,:] = newer_results_pre[0,:]
ninex_new_results_pre[3,:] = newer_results_pre[1,:]
ninex_new_results_pre[4,:] = newer_results_pre[1,:]
ninex_new_results_pre[5,:] = newer_results_pre[1,:]
ninex_new_results_pre[6,:] = newer_results_pre[2,:]
ninex_new_results_pre[7,:] = newer_results_pre[2,:]
ninex_new_results_pre[8,:] = newer_results_pre[2,:]


new_results_diff = new_results_post - ninex_new_results_pre

#Establishing labels for corrplots
new_line_labels_diff = ["M.1","M.2","M.3","X.1","X.2","X.3","MX.1","MX.2","MX.3"]
new_line_labels_pre = ["M.0","X.0","MX.0"]
new_column_labels = ["M1","M3","M4","M5","M7","M8","M9","X1","X2","X3","X4","X5","XA1","XA2","XA3","XB1","XB2","XB3","M_Avg.","X_Avg.","Total_Avg."]

#Rearrange post rl
"""
newer_line_labels = [None]*9
newer_results = np.zeros((9,21))
for rnn in range(3):
	for ruleset  in range(3):
		newer_results[ruleset*3+rnn,:] = new_results_post[rnn*3+ruleset,:]
		newer_line_labels[ruleset*3+rnn] = new_line_labels_diff[rnn*3+ruleset]
new_results_post = newer_results
new_line_labels_diff = newer_line_labels
"""
#create CSV file

f = open("diff_heat.csv","w")

for i,col in enumerate(new_column_labels):
	if i:
		f.write(",")
	f.write(col)
f.write("\n")
for i,label in enumerate(new_line_labels_diff):
	f.write(str(label))
	for val in new_results_diff[i,:]:
		f.write(",")
		f.write(str(val))
	f.write("\n")
f.close()

#Create corrplot using R
r_command = "Rscript diff_corrplot.R"
process = subprocess.Popen(r_command.split(),stdout=subprocess.PIPE)
output,error = process.communicate()

f = open("pre_rl_heat.csv","w")

for i,col in enumerate(new_column_labels):
	if i:
		f.write(",")
	f.write(col)
f.write("\n")
for i,label in enumerate(new_line_labels_pre):
	f.write(str(label))
	for val in new_results_pre[i,:]:
		f.write(",")
		f.write(str(val))
	f.write("\n")
f.close()

#Create corrplot using R
r_command = "Rscript pre_rl_corrplot.R"
process = subprocess.Popen(r_command.split(),stdout=subprocess.PIPE)
output,error = process.communicate()

f = open("post_rl_heat.csv","w")

for i,col in enumerate(new_column_labels):
	if i:
		f.write(",")
	f.write(col)
f.write("\n")
for i,label in enumerate(new_line_labels_diff):
	f.write(str(label))
	for val in new_results_post[i,:]:
		f.write(",")
		f.write(str(val))
	f.write("\n")
f.close()

#Create corrplot using R
r_command = "Rscript post_rl_corrplot.R"
process = subprocess.Popen(r_command.split(),stdout=subprocess.PIPE)
output,error = process.communicate()
