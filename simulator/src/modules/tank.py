# -*- coding: utf-8 -*-

import math
from base import processor


class Tank(processor.Processor):

    def __init__(self, name):
        self.lab_i_s = 0.0  # 输入水流速度（升/秒）
        self.lab_i_t = 0.0  # 输入水流温度（摄氏度）
        self.lab_o_s = 0.0  # 输出水流速度（升/秒）
        self.lab_o_t = 0.0  # 输出水流温度（摄氏度）
        self.lab_c_h = 0.0  # 当前液位高度（米）
        self.lab_s_s = 0.0  # 水罐底面积（平方米）
        self.lab_c_i = 0.0  # 加热电流（安培）
        self.lab_s_r = 0.0  # 加热电阻(欧姆)
        self.lab_s_l = 100  # 输出管道系数
        self.lab_c_g = 0    # 输出阀门开度（0 - 100）
        self.lab_c_t = 0.0  # 环境温度
        self.lab_s_p = 0.0  # 散热功率
        super(Tank, self).__init__(name)
        return

    def calc_inputs(self):
        if len(self.inputs) > 0:
            self.lab_i_t = self.inputs[0].lab_o_t
            self.lab_i_s = self.inputs[0].lab_o_s

        return

    def calc_outputs(self, interval):
        C = 4200

        if self.lab_s_s == 0 or self.lab_s_l == 0:
            return

        # 计算罐内水体积
        v0 = self.lab_c_h * self.lab_s_s * 1000
        v1 = v0 + (self.lab_i_s - self.lab_o_s) * interval
        if v1 < 0:
            v1 = 0

        # 计算管内水热量
        q0 = v0 * C * self.lab_o_t
        q1 = q0 + \
            (self.lab_i_s * self.lab_i_t - self.lab_o_s * self.lab_o_t) * interval * C + \
            self.lab_c_i * self.lab_c_i * self.lab_s_r * interval - \
            self.lab_s_p * (self.lab_o_t - self.lab_c_t) * interval
        if q1 < 0:
            q1 = 0

        self.lab_c_h = (v1 / 1000) / self.lab_s_s
        self.lab_o_s = math.sqrt(self.lab_c_h / self.lab_s_l) * self.lab_c_g
        if v1 == 0:
            self.lab_o_t = 0.0
        else:
            self.lab_o_t = (q1 / v1) / C

        return
