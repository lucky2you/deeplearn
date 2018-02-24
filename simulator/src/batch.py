# -*- coding: utf-8 -*-

import random
from pid import PID
from base.simulator import Simulator
from modules.tank import Tank


random.seed()

def load_topo():
    tank1_values = {
        'i_s': 10.0,  # 输入水流速度（升/秒）
        'o_s': 10.0,  # 输出水流速度（升/秒）
        'i_t': 20.0,  # 输入水流温度（摄氏度）
        'o_t': 30.0,  # 输出水流温度（摄氏度）
        'c_h': 5.0 ,  # 当前液位高度（米）
        's_s': 2.0 ,  # 水罐底面积（平方米）
        'c_i': 9.69,  # 加热电流（安培）
        's_r': 500.0, # 加热电阻(欧姆)
        's_l': 180.0, # 输出管道系数
        'c_g': 0.6 ,  # 输出阀门开度（0.0 - 1.0）
        'c_t': 20.0,  # 环境温度
        's_p': 500.0, # 散热功率
    }

    tank2_values = {
        'i_s': 10.0,  # 输入水流速度（升/秒）
        'o_s': 10.0,  # 输出水流速度（升/秒）
        'i_t': 30.0,  # 输入水流温度（摄氏度）
        'o_t': 40.0,  # 输出水流温度（摄氏度）
        'c_h': 5.0 ,  # 当前液位高度（米）
        's_s': 2.0 ,  # 水罐底面积（平方米）
        'c_i': 10.2 , # 加热电流（安培）
        's_r': 500.0, # 加热电阻(欧姆)
        's_l': 180.0, # 输出管道系数
        'c_g': 0.6 ,  # 输出阀门开度（0.0 - 1.0）
        'c_t': 20.0,  # 环境温度
        's_p': 500.0, # 散热功率
    }

    tank3_values = {
        'i_s': 10.0,  # 输入水流速度（升/秒）
        'o_s': 10.0,  # 输出水流速度（升/秒）
        'i_t': 40.0,  # 输入水流温度（摄氏度）
        'o_t': 50.0,  # 输出水流温度（摄氏度）
        'c_h': 5.0 ,  # 当前液位高度（米）
        's_s': 2.0 ,  # 水罐底面积（平方米）
        'c_i': 10.68, # 加热电流（安培）
        's_r': 500.0, # 加热电阻(欧姆)
        's_l': 180.0, # 输出管道系数
        'c_g': 0.6 ,  # 输出阀门开度（0.0 - 1.0）
        'c_t': 20.0,  # 环境温度
        's_p': 500.0, # 散热功率
    }

    tank4_values = {
        'i_s': 10.0,  # 输入水流速度（升/秒）
        'o_s': 10.0,  # 输出水流速度（升/秒）
        'i_t': 50.0,  # 输入水流温度（摄氏度）
        'o_t': 60.0,  # 输出水流温度（摄氏度）
        'c_h': 5.0 ,  # 当前液位高度（米）
        's_s': 2.0 ,  # 水罐底面积（平方米）
        'c_i': 11.13, # 加热电流（安培）
        's_r': 500.0, # 加热电阻(欧姆)
        's_l': 180.0, # 输出管道系数
        'c_g': 0.6 ,  # 输出阀门开度（0.0 - 1.0）
        'c_t': 20.0,  # 环境温度
        's_p': 500.0, # 散热功率
    }

    sim = Simulator()
    tank1 = Tank('Tank1')
    tank2 = Tank('Tank2')
    tank3 = Tank('Tank3')
    tank4 = Tank('Tank4')

    sim.add(tank1)
    sim.add(tank2)
    sim.add(tank3)
    sim.add(tank4)

    sim.connect(tank1, tank2)
    sim.connect(tank2, tank3)
    sim.connect(tank3, tank4)

    tank1.set_values(tank1_values)
    tank2.set_values(tank2_values)
    tank3.set_values(tank3_values)
    tank4.set_values(tank4_values)

    return sim

pid_t = []
for i in range(0, 4):
    pid_t.append(PID(P=40, I=1.0, D=0.5))
    pid_t[i].set_windup(50.0)
    pid_t[i].set_sample_time(10)
pid_t[0].SetPoint = 30.0
pid_t[1].SetPoint = 40.0
pid_t[2].SetPoint = 50.0
pid_t[3].SetPoint = 60.0

pid_s = []
for i in range(0, 4):
    pid_s.append(PID(P=0.8, I=0.05, D=0.1))
    pid_s[i].set_windup(20.0)
    pid_s[i].set_sample_time(10)
    pid_s[i].SetPoint = 1.0

def get_i(output):
    i = output
    i = 80 if i > 80 else i
    i = 0  if i <  0 else i
    return i

def get_g(output):
    g = 50 + output * 50
    g = int((g + 4) / 5) * 5
    if g < 0:
        g = 0
    if g > 100:
        g = 100
    return g
    
def get_settings(ts, values):

    h = ts / 3600
    m = (ts % 3600) / 60
    s = ts % 60

    i_s = (float(m - 30) / 30.0) * 3 + 10.0
    i_t = (float((m + 20) % 60 - 30)/ 30.0) * 5 + 20.0

    if h > 12:
        c_t = (float(24 - h) / 12) * 10 + 20
    else:
        c_t = (float(h) / 12) * 10 + 20

    pid_s[0].update(values['Tank1_o_s']/10.0, ts)
    pid_s[1].update(values['Tank2_o_s']/10.0, ts)
    pid_s[2].update(values['Tank3_o_s']/10.0, ts)
    pid_s[3].update(values['Tank4_o_s']/10.0, ts)

    pid_t[0].update(values['Tank1_o_t'], ts)
    pid_t[1].update(values['Tank2_o_t'], ts)
    pid_t[2].update(values['Tank3_o_t'], ts)
    pid_t[3].update(values['Tank4_o_t'], ts)

    settings = {
        'Tank1_i_s': i_s,  # 输入水流速度（升/秒）
        'Tank1_i_t': i_t,  # 输入水流温度（摄氏度）
        'Tank1_c_i': get_i(pid_t[0].output), # 加热电流（安培）
        'Tank1_c_g': get_g(pid_s[0].output), # 输出阀门开度（0.0 - 1.0）
        'Tank1_c_t': c_t,  # 环境温度
        'Tank2_c_i': get_i(pid_t[1].output), # 加热电流（安培）
        'Tank2_c_g': get_g(pid_s[1].output), # 输出阀门开度（0.0 - 1.0）
        'Tank2_c_t': c_t,  # 环境温度
        'Tank3_c_i': get_i(pid_t[2].output), # 加热电流（安培）
        'Tank3_c_g': get_g(pid_s[2].output), # 输出阀门开度（0.0 - 1.0）
        'Tank3_c_t': c_t,  # 环境温度
        'Tank4_c_i': get_i(pid_t[3].output), # 加热电流（安培）
        'Tank4_c_g': get_g(pid_s[3].output), # 输出阀门开度（0.0 - 1.0）
        'Tank4_c_t': c_t,  # 环境温度
    }

    return settings

def noise(values):
    for k in values:
        if k.find('_i_') > 0:
            values[k] = round(values[k] * (1 + random.uniform(-0.005, 0.005)), 2)
        if k.find('_o_') > 0:
            values[k] = round(values[k] * (1 + random.uniform(-0.005, 0.005)), 2)
        if k.find('_c_t') > 0:
            values[k] = round(values[k] * (1 + random.uniform(-0.01, 0.01)), 2)

    return values

def title(values):
    dict_a=sorted(values.keys())

    s = 'ID'
    for i in range(len(dict_a)):
        s += ',' + str(dict_a[i])
    print(s)

def save(ts, values):
    dict_a=sorted(values.keys())

    s = '%d' % ts
    for i in range(len(dict_a)):
        s += ',' + str(values[dict_a[i]])
    print(s)

def main():

    sim = load_topo()

    values = sim.dump_values()
    title(values)

    interval = 1
    for step in range(0, int(24*60*60/interval)):
        ts = step * interval
        settings = get_settings(ts, values)
        
        sim.set_values(settings)
        sim.step(interval)
        values = sim.dump_values()

        noise(values)
        save(ts, values)
        values = sim.dump_values()

    return 0


if __name__ == "__main__":
    main()
