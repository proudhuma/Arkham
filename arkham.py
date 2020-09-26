import random
import datetime
import re
import os
from flask import Flask, flash, request, redirect, url_for, render_template, session

app = Flask(__name__)

#### lazy approach
def write_hist(input_str):
    with open("fake_db", "a") as file:
        file.write((input_str + os.linesep))

def read_hist():
    hist = ""
    with open("fake_db", "r") as file:
        all_lines = file.readlines()
        for line in all_lines:
            hist +=  line.replace("\n", "<br>")
    return hist

def clear_hist():
    os.remove("fake_db")
    file = open("fake_db", "w")
    file.close()
####

def generate_rand(max):
    random.seed(datetime.datetime.now())
    return random.randint(1, max)

# actually a state machine
#
# 0-------number or roll------->1
# ^                             |
# -----plus or minus-------------
#
def parse_regex(input_str):
    invalid = "invalid syntax"
    if input_str == "/help":
        return "usage: /roll.[expression]([+|-][expression])... where expression is [r_d_] OR number", -1
    cur_pos = 6 # /roll.
    cur_state = 0
    result_str = ""
    result_val_slice = []
    result_val = 0
    while cur_pos < len(input_str) :
        if cur_state == 0:
            # recv number OR r 
            if input_str[cur_pos] == "r" :
                # state change to 1
                cur_state = 1
                # deal with dice
                cur_pos += 1 # skip r
                end_pos, num_str = get_next_number(input_str, cur_pos)
                repeat_times = int(num_str)
                cur_pos = end_pos
                if input_str[end_pos] != "d" :
                    return invalid, -1
                cur_pos += 1 # skip d
                end_pos, num_str = get_next_number(input_str, cur_pos)
                dice_kind = int(num_str)
                cur_pos = end_pos
                # roll dice
                tmp_cnt = 0
                for i in range(repeat_times) :
                    roll = generate_rand(dice_kind)
                    result_str += str(roll)
                    tmp_cnt += roll
                    if i != repeat_times - 1 :
                        result_str += "+"
                result_val_slice.append(tmp_cnt)
            elif ord(input_str[cur_pos]) >= 48 and ord(input_str[cur_pos]) <= 57 :
                # state change to 1
                cur_state = 1
                # deal with number
                end_pos, num_str = get_next_number(input_str, cur_pos)
                num_val = int(num_str)
                cur_pos = end_pos
                result_str += num_str
                result_val_slice.append(num_val)
            else:
                return invalid, -1
        elif cur_state == 1 :
            if input_str[cur_pos] == "+" or input_str[cur_pos] == "-" :
                result_str += input_str[cur_pos]
                result_val_slice.append(input_str[cur_pos])
                cur_pos += 1
                cur_state = 0
            else :
                return invalid, -1
    print(result_str)
    print(result_val_slice)
    tmp_slice = []
    i = 0
    while i < len(result_val_slice) :
        if result_val_slice[i] != "+" and result_val_slice[i] != "-":
            result_val += result_val_slice[i]
            i += 1
        elif result_val_slice[i] == "+":
            i += 1
        elif result_val_slice[i] == "-":
            i += 1
            v = result_val_slice[i]
            result_val_slice[i] = -v
    # end state must be 1
    if cur_state == 1:
        return result_str, result_val
    else :
        return invalid, -1

# start_pos is a number
# return end_pos, substr
def get_next_number(input, start_pos):
    end_pos = start_pos
    while end_pos < len(input) and ord(input[end_pos]) >= 48 and ord(input[end_pos]) <= 57 :
        end_pos += 1
    return end_pos, input[start_pos:end_pos]

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/1D4', methods=['GET', 'POST'])
def d4():
    result = generate_rand(4)
    return render_template("success.html", result=result)

@app.route('/1D6', methods=['GET', 'POST'])
def d6():
    result = generate_rand(6)
    return render_template("success.html", result=result)

@app.route('/1D8', methods=['GET', 'POST'])
def d8():
    result = generate_rand(8)
    return render_template("success.html", result=result)

@app.route('/1D20', methods=['GET', 'POST'])
def d20():
    result = generate_rand(20)
    return render_template("success.html", result=result)

@app.route('/1D100', methods=['GET', 'POST'])
def d100():
    result = generate_rand(100)
    return render_template("success.html", result=result)

@app.route('/roll', methods=['POST'])
def regex():
    input_regex = request.form.get('regex')
    print(input_regex)
    result_str, result_val = parse_regex(input_regex)
    
    if result_val == -1 :
        write_hist(result_str)
    else : 
        write_hist(result_str + " = " + str(result_val))

    ret_val = read_hist()
    print(ret_val)

    return render_template("roll.html", history=ret_val)

@app.route('/roll/clear', methods=['GET','POST'])
def clear():
    clear_hist()
    return render_template("roll.html", history="")

if __name__ == '__main__':
    app.debug = True
    app.run("0.0.0.0","5000")