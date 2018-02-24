# -*- coding: utf-8 -*-

import random
from pid import PID
from base.simulator import Simulator
from modules.tank import Tank


random.seed()

def load_topo():
    tank1_values = {
        'i_s': 10.0,  # 输入水流速度（升/秒）
        'o_s': 0.0,   # 输出水流速度（升/秒）
        'i_t': 20.0,  # 输入水流温度（摄氏度）
        'o_t': 25.0,  # 输出水流温度（摄氏度）
        'c_h': 5.0 ,  # 当前液位高度（米）
        's_s': 2.0 ,  # 水罐底面积（平方米）
        'c_i': 10.0,  # 加热电流（安培）
        's_r': 500.0, # 加热电阻(欧姆)
        's_l': 180.0, # 输出管道系数
        'c_g': 50,    # 输出阀门开度（0 - 100）
        'c_t': 20.0,  # 环境温度
        's_p': 500.0, # 散热功率
    }

    sim = Simulator()
    tank1 = Tank('Tank1')

    sim.add(tank1)

    tank1.set_values(tank1_values)

    return sim

pid_t = PID(P=40.0, I=1.0, D=0.5)
pid_t.set_sample_time(10)
pid_t.set_windup(50.0)
pid_t.SetPoint = 30.0

pid_s = PID(P=0.8, I=0.05, D=0.1)
pid_s.set_sample_time(5)
pid_t.set_windup(20)
pid_s.SetPoint = 1.0


def get_settings(ts, values):
    pid_t.update(values['Tank1_o_t'], ts)
    pid_s.update(values['Tank1_o_s']/10.0, ts)

    i = pid_t.output
    if i > 80:
        i = 80
    if i < 0:
        i = 0

    g = 50 + pid_s.output * 50
    g = int((g + 4) / 5) * 5
    if g < 0:
        g = 0
    if g > 100:
        g = 100

    settings = {
        'Tank1_c_i': i,
        'Tank1_c_g': g
    }

    return settings

def title(values):
    dict_a=sorted(values.keys())

    s = 'ID'
    for i in range(len(dict_a)):
        s += ',' + str(dict_a[i])

    print(s + 'End')

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
    for step in range(0, 1000):
        ts = step * interval
        settings = get_settings(ts, values)

        sim.set_values(settings)
        sim.step(interval)
        values = sim.dump_values()
        save(ts, values)

    return 0


if __name__ == "__main__":
    main()
