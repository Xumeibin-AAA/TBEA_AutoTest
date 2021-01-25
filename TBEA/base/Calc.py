from TBEA.base.util import GetRedis
import ast, datetime


class calc:
    # 将字符串类型的日期转为数值类型（单位:天）
    def Str_Date(self, start, stop):
        start = datetime.datetime.strptime(start, '%Y-%m-%d')
        stop = datetime.datetime.strptime(stop, '%Y-%m-%d')
        s = str(stop - start)
        if s.find('-') == -1:
            if s.find('day') != -1:
                d = s[:s.index("day")]
                h = s[s.index(",") + 1:s.index(":")]
            else:
                d = 0
                h = 0
            m = s[s.index(":") + 1:s.rindex(":")]
            s = s[s.rindex(":") + 1:]
            value = int(d) + int(h) / 24 + int(m) / 60 / 24 + int(s) / 60 / 60 / 24
            return value
        else:
            return '取值错误！！！'

    def Test1_Result(self, data, t):
        redis = GetRedis()
        value = redis.GetDate(data)
        value = ast.literal_eval(value)
        # 第一次取样某气体浓度总烃浓度
        r1 = value['p4'] + value['p5'] + value['p6'] + value['p7']
        # 取样间隔d(天)
        r2 = self.Str_Date(value['p8'], value['p16'])
        # 取样间隔(月)
        r3 = self.Str_Date(value['p8'], value['p16']) / 30
        # 第二次取样某气体浓度总烃浓度
        r4 = value['p12'] + value['p13'] + value['p14'] + value['p15']
        # H2 绝对产气速率
        r5 = (value['p9'] - value['p1']) / r2 * (t / 0.885)
        # CO 绝对产气速率
        r6 = (value['p10'] - value['p2']) / r2 * (t / 0.885)
        # CO2 绝对产气速率
        r7 = (value['p11'] - value['p3']) / r2 * (t / 0.885)
        # CH4 绝对产气速率
        r8 = (value['p12'] - value['p4']) / r2 * (t / 0.885)
        # C2h4 绝对产气速率
        r9 = (value['p13'] - value['p5']) / r2 * (t / 0.885)
        # C2h6 绝对产气速率
        r10 = (value['p14'] - value['p6']) / r2 * (t / 0.885)
        # C2h2 绝对产气速率
        r11 = (value['p15'] - value['p7']) / r2 * (t / 0.885)
        # ΣCH 绝对产气速率
        r12 = (r4 - r1) / r2 * (t / 0.885)
        # H2相对产气速率
        r13 = f"{(value['p9'] - value['p1']) / value['p1'] * (1 / r3) * 100}%"
        # CO相对产气速率
        r14 = f"{(value['p10'] - value['p2']) / value['p1'] * (1 / r3) * 100}%"
        # CO2相对产气速率
        r15 = f"{(value['p11'] - value['p3']) / value['p1'] * (1 / r3) * 100}%"
        # CH4相对产气速率
        r16 = f"{(value['p12'] - value['p4']) / value['p1'] * (1 / r3) * 100}%"
        # C2H4相对产气速率
        r17 = f"{(value['p13'] - value['p5']) / value['p1'] * (1 / r3) * 100}%"
        # C2H6相对产气速率
        r18 = f"{(value['p14'] - value['p6']) / value['p1'] * (1 / r3) * 100}%"
        # C2H2相对产气速率
        r19 = f"{(value['p15'] - value['p7']) / value['p1'] * (1 / r3) * 100}%"
        # ΣCH 相对产气速率
        r20 = f"{(r4 - r1) / value['p1'] * (1 / r3) * 100}%"
        return {'r1': r1, 'r2': r2, 'r3': r3, 'r4': r4, 'r5': r5, 'r6': r6, 'r7': r7, 'r8': r8, 'r9': r9, 'r10': r10,
                'r11': r11, 'r12': r12, 'r13': r13, 'r14': r14, 'r15': r15, 'r16': r16, 'r17': r17, 'r18': r18,
                'r19': r19, 'r20': r20}

    def Test2_Result(self, data):
        redis = GetRedis()
        value = redis.GetDate(data)
        value = ast.literal_eval(value)
        # 高压绕组-最负分接
        ma = max([value['p2'], value['p3'], value['p4']])
        mi = min([value['p2'], value['p3'], value['p4']])
        avg = sum([value['p2'], value['p3'], value['p4']]) / 3
        r1 = (ma - mi) / avg
        # 高压绕组-主分接
        ma = max([value['p5'], value['p6'], value['p7']])
        mi = min([value['p5'], value['p6'], value['p7']])
        avg = sum([value['p5'], value['p6'], value['p7']]) / 3
        r2 = (ma - mi) / avg
        # 高压绕组-最正分接
        ma = max([value['p8'], value['p9'], value['p10']])
        mi = min([value['p8'], value['p9'], value['p10']])
        avg = sum([value['p8'], value['p9'], value['p10']]) / 3
        r3 = (ma - mi) / avg
        # 中压绕组-最负分接
        ma = max([value['p12'], value['p13'], value['p14']])
        mi = min([value['p12'], value['p13'], value['p14']])
        avg = sum([value['p12'], value['p13'], value['p14']]) / 3
        r4 = (ma - mi) / avg
        # 中压绕组-主分接
        ma = max([value['p15'], value['p16'], value['p17']])
        mi = min([value['p15'], value['p16'], value['p17']])
        avg = sum([value['p15'], value['p16'], value['p17']]) / 3
        r5 = (ma - mi) / avg
        # 中压绕组-最正分接
        ma = max([value['p18'], value['p19'], value['p20']])
        mi = min([value['p18'], value['p19'], value['p20']])
        avg = sum([value['p18'], value['p19'], value['p20']]) / 3
        r6 = (ma - mi) / avg
        # 低压绕组-1个
        ma = max([value['p22'], value['p23'], value['p24']])
        mi = min([value['p22'], value['p23'], value['p24']])
        avg = sum([value['p22'], value['p23'], value['p24']]) / 3
        r7 = (ma - mi) / avg
        return {'r1': r1, 'r2': r2, 'r3': r3, 'r4': r4, 'r5': r5, 'r6': r6, 'r7': r7}

    def Test3_Result(self, data):
        redis = GetRedis()
        value = redis.GetDate(data)
        value = ast.literal_eval(value)
        # 高压 - 吸收比d
        r1 = value['p2'] / value['p1']
        # 高压 - 极化指数k
        r2 = value['p3'] / value['p2']
        # 中压 - 吸收比d
        r3 = value['p5'] / value['p4']
        # 中压 - 极化指数k
        r4 = value['p6'] / value['p5']
        # 低压 - 吸收比d
        r5 = value['p8'] / value['p7']
        # 低压 - 极化指数k
        r6 = value['p9'] / value['p8']
        # 高压和中压 - 吸收比d
        r7 = value['p11'] / value['p10']
        # 高压和中压 - 极化指数k
        r8 = value['p12'] / value['p11']
        # 高压中压和低压 - 吸收比d
        r9 = value['p14'] / value['p13']
        # 高压中压和低压 - 极化指数k
        r10 = value['p15'] / value['p14']
        return {'r1': r1, 'r2': r2, 'r3': r3, 'r4': r4, 'r5': r5, 'r6': r6, 'r7': r7, 'r8': r8, 'r9': r9, 'r10': r10}

    def Test4_Result(self, data):
        redis = GetRedis()
        value = redis.GetDate(data)
        value = ast.literal_eval(value)
        # 高压 tanδ(%)（20℃）
        r1 = value['p2'] * 1.3 ** ((20 - value['p1']) / 10)
        # 中压 tanδ(%)（20℃）
        r2 = value['p4'] * 1.3 ** ((20 - value['p1']) / 10)
        # 低压 tanδ(%)（20℃）
        r3 = value['p6'] * 1.3 ** ((20 - value['p1']) / 10)
        # 高压和中压 tanδ(%)（20℃）
        r4 = value['p8'] * 1.3 ** ((20 - value['p1']) / 10)
        # 高压中压和低压 tanδ(%)（20℃）
        r5 = value['p10'] * 1.3 ** ((20 - value['p1']) / 10)
        return {'r1': r1, 'r2': r2, 'r3': r3, 'r4': r4, 'r5': r5}

    def Test5_Result(self, data):
        redis = GetRedis()
        value = redis.GetDate(data)
        value = ast.literal_eval(value)
        # 高压 tanδ(%)（20℃）
        r1 = value['p2'] * 1.3 ** ((20 - value['p1']) / 10)
        # 中压 tanδ(%)（20℃）
        r2 = value['p4'] * 1.3 ** ((20 - value['p1']) / 10)
        # 低压 tanδ(%)（20℃）
        r3 = value['p6'] * 1.3 ** ((20 - value['p1']) / 10)
        # 高压和中压 tanδ(%)（20℃）
        r4 = value['p8'] * 1.3 ** ((20 - value['p1']) / 10)
        # 高压中压和低压 tanδ(%)（20℃）
        r5 = value['p10'] * 1.3 ** ((20 - value['p1']) / 10)
        return {'r1': r1, 'r2': r2, 'r3': r3, 'r4': r4, 'r5': r5}

    def Test6_Result(self, data):
        pass

    def Test7_Result(self, data):
        pass

    def Test8_Result(self, data):
        pass

    def Test9_Result(self, data, height, centre, low):
        redis = GetRedis()
        value = redis.GetDate(data)
        value = ast.literal_eval(value)
        # 最负分接 电压比 AB
        r1 = value['p1'] / centre
        # 最负分接 电压比 BC
        r2 = value['p2'] / centre
        # 最负分接 电压比 CA
        r3 = value['p3'] / centre
        # 最负分接 电压比偏差 AB
        r4 = r1 - height / centre
        # 最负分接 电压比偏差 BC
        r5 = r2 - height / centre
        # 最负分接 电压比偏差 CA
        r6 = r3 - height / centre
        # 主分接 电压比 AB
        r7 = value['p5'] / centre
        # 主分接 电压比 BC
        r8 = value['p6'] / centre
        # 主分接 电压比 CA
        r9 = value['p7'] / centre
        # 主分接 电压比偏差 AB
        r10 = r7 - height / centre
        # 主分接 电压比偏差 BC
        r11 = r8 - height / centre
        # 主分接 电压比偏差 CA
        r12 = r9 - height / centre
        # 最正分接 电压比 AB
        r13 = value['p8'] / centre
        # 最正分接 电压比 BC
        r14 = value['p9'] / centre
        # 最正分接 电压比 CA
        r15 = value['p10'] / centre
        # 最正分接 电压比偏差 AB
        r16 = r13 - height / centre
        # 最正分接 电压比偏差 BC
        r17 = r14 - height / centre
        # 最正分接 电压比偏差 CA
        r18 = r15 - height / centre
        # 最负分接 电压比 AB
        r19 = value['p11'] / low
        # 最负分接 电压比 BC
        r20 = value['p12'] / low
        # 最负分接 电压比 CA
        r21 = value['p13'] / low
        # 最负分接 电压比偏差 AB
        r22 = r19 - height / low
        # 最负分接 电压比偏差 BC
        r23 = r20 - height / low
        # 最负分接 电压比偏差 CA
        r24 = r21 - height / low
        # 主分接 电压比 AB
        r25 = value['p15'] / low
        # 主分接 电压比 BC
        r26 = value['p16'] / low
        # 主分接 电压比 CA
        r27 = value['p17'] / low
        # 主分接 电压比偏差 AB
        r28 = r25 - height / low
        # 主分接 电压比偏差 BC
        r29 = r26 - height / low
        # 主分接 电压比偏差 CA
        r30 = r27 - height / low
        # 最正分接 电压比 AB
        r31 = value['p18'] / low
        # 最正分接 电压比 BC
        r32 = value['p19'] / low
        # 最正分接 电压比 CA
        r33 = value['p20'] / low
        # 最正分接 电压比偏差 AB
        r34 = r31 - height / low
        # 最正分接 电压比偏差 BC
        r35 = r32 - height / low
        # 最正分接 电压比偏差 CA
        r36 = r33 - height / low
        # 最负分接 电压比 AB
        r37 = value['p21'] / low
        # 最负分接 电压比 BC
        r38 = value['p22'] / low
        # 最负分接 电压比 CA
        r39 = value['p23'] / low
        # 最负分接 电压比偏差 AB
        r40 = r37 - centre / low
        # 最负分接 电压比偏差 BC
        r41 = r38 - centre / low
        # 最负分接 电压比偏差 CA
        r42 = r39 - centre / low
        # 主分接 电压比 AB
        r43 = value['p25'] / low
        # 主分接 电压比 BC
        r44 = value['p26'] / low
        # 主分接 电压比 CA
        r45 = value['p27'] / low
        # 主分接 电压比偏差 AB
        r46 = r43 - centre / low
        # 主分接 电压比偏差 BC
        r47 = r44 - centre / low
        # 主分接 电压比偏差 CA
        r48 = r45 - centre / low
        # 最正分接 电压比 AB
        r49 = value['p28'] / low
        # 最正分接 电压比 BC
        r50 = value['p29'] / low
        # 最正分接 电压比 CA
        r51 = value['p30'] / low
        # 最正分接 电压比偏差 AB
        r52 = r49 - centre / low
        # 最正分接 电压比偏差 BC
        r53 = r50 - centre / low
        # 最正分接 电压比偏差 CA
        r54 = r51 - centre / low
        return {'r1': r1, 'r2': r2, 'r3': r3, 'r4': r4, 'r5': r5, 'r6': r6, 'r7': r7, 'r8': r8, 'r9': r9, 'r10': r10,
                'r11': r11, 'r12': r12, 'r13': r13, 'r14': r14, 'r15': r15, 'r16': r16, 'r17': r17, 'r18': r18,
                'r19': r19, 'r20': r20, 'r21': r21, 'r22': r22, 'r23': r23, 'r24': r24, 'r25': r25, 'r26': r26,
                'r27': r27, 'r28': r28, 'r29': r29, 'r30': r30, 'r31': r31, 'r32': r32, 'r33': r33, 'r34': r34,
                'r35': r35, 'r36': r36, 'r37': r37, 'r38': r38, 'r39': r39, 'r40': r40, 'r41': r41, 'r42': r42,
                'r43': r43, 'r44': r44, 'r45': r45, 'r46': r46, 'r47': r47, 'r48': r48, 'r49': r49, 'r50': r50,
                'r51': r51, 'r52': r52, 'r53': r53, 'r54': r54}

    def Test10_Result(self, data):
        pass

    def Test11_Result(self, data,electricity):
        '''

        :param data:
        :param electricity: 额定电流 额定电流=基本信息中的额定容量/额定电压/根号3
        :return:
        '''
        redis = GetRedis()
        value = redis.GetDate(data)
        value = ast.literal_eval(value)
        # 空载电流 励磁倍率: 90%
        r1 = (value['p3']+value['p4']+value['p5'])/3/electricity
        # 空载损耗 励磁倍率: 90%
        r2 = value['p6']*(1+((value['p1']-value['p2'])/value['p1']))
        # 空载电流 励磁倍率: 100%
        r3 = (value['p9']+value['p10']+value['p11'])/3/electricity
        # 空载损耗 励磁倍率: 100%
        r4 = value['p12']*(1+((value['p7']-value['p8'])/value['p7']))
        # 空载电流 励磁倍率: 110%
        r5 = (value['p15']+value['p16']+value['p17'])/3/electricity
        # 空载损耗 励磁倍率: 110%
        r6 = value['p18']*(1+((value['p13']-value['p14'])/value['p13']))
        # 空载电流 励磁倍率: 90%
        r7 = (value['p21']+value['p22']+value['p23'])/3/electricity
        # 空载损耗 励磁倍率: 90%
        r8 = value['p24']*(1+((value['p18']-value['p20'])/value['p19']))
        # 空载电流 励磁倍率: 100%
        r9 = (value['p27']+value['p28']+value['p29'])/3/electricity
        # 空载损耗 励磁倍率: 100%
        r10 = value['p30']*(1+((value['p24']-value['p26'])/value['p25']))
        # 空载电流 励磁倍率: 100%
        r11 = (value['p33']+value['p34']+value['p35'])/3/electricity
        # 空载损耗 励磁倍率: 100%
        r12 = value['p36']*(1+((value['p30']-value['p32'])/value['p31']))
        return {'r1':r1,'r2':r2,'r3':r3,'r4':r4,'r5':r5,'r6':r6,'r7':r7,'r8':r8,'r9':r9,'r10':r10,'r11':r11,'r12':r12}

    def Test12_Result(self, data,P0):
        redis = GetRedis()
        value = redis.GetDate(data)
        value = ast.literal_eval(value)
        # 高对中 - 最负分接
        r1 = P0 + value['p5']
        # 高对中 - 主分接
        r2 = P0 + value['p10']
        # 高对中 - 最正分接
        r3 = P0 + value['p15']
        # 高对低 最负分接
        r4 = P0 + value['p20']
        # 高对低 主分接
        r5 = P0 + value['p25']
        # 高对低 最负分接
        r6 = P0 + value['p30']
        # 中对低 最负分接
        r7 = P0 + value['p35']
        # 中对低 主分接
        r8 = P0 + value['p40']
        # 中对低 最负分接
        r9 = P0 + value['p45']
        return {'r1':r1,'r2':r2,'r3':r3,'r4':r4,'r5':r5,'r6':r6,'r7':r7,'r8':r8,'r9':r9}

    def Test13_Result(self, data):
        pass

    def Test14_Result(self, data):
        pass

    def Test15_Result(self, data):
        pass

    def Test16_Result(self, data):
        pass

    def Test17_Result(self, data):
        pass

    def Test18_Result(self, data):
        pass

    def Test19_Result(self, data):
        pass

    def Test20_Result(self, data):
        pass

    def Test21_Result(self, data):
        pass

    def Test22_Result(self, data):
        pass

    def Test23_Result(self, data):
        pass


if __name__ == '__main__':
    Calc = calc()
    temp = Calc.Test12_Result('Test12_A', 200)
    print(temp)
