import time
class Rule:
    def __init__(self, read_state, read_char, out_state, out_content, next_orientation):
        self.read_state = read_state
        self.read_char = read_char
        self.out_state = out_state
        self.out_content = out_content
        self.next_orientation = next_orientation  # True往左，False往右


class Turing:
    def __init__(self):
        self.tape = ['#']
        self.current_state = 0
        self.cur = 1

    # 复制只有1组成的字符串
    # rules=[
    #     Rule(0,'1',0,'x',False),
    #     Rule(0,'#',1,'#',True),
    #     Rule(1,'x',2,'1',False),
    #     Rule(2,'1',2,'1',False),
    #     Rule(2,'#',1,'1',True),
    #     Rule(1,'1',1,'1',True),
    #     Rule(1,'#',final_state,'#',False),
    # ]
    # 实现两数的乘法
    # rules=[
    #     Rule(0,'1',1,'a',False),    # 1
    #     Rule(1,'1',1,'1',False),    # 2
    #     Rule(1,'0',2,'0',False),    # 3
    #     Rule(2,'1',3,'b',False),    # 4
    #
    #     Rule(3,'1',3,'1',False),    # 5
    #     Rule(3,'0',4,'0',False),    # 6
    #     Rule(4,'0',5,'1',False),    # 7
    #     Rule(4,'1',4,'1',False),    # 8
    #     Rule(5,'#',6,'0',True),    # 9
    #     Rule(6,'0',6,'0',True),    # 10
    #     Rule(6,'1',6,'1',True),    # 11
    #     Rule(6,'b',2,'b',False),    # 12
    #
    #     Rule(2,'0',7,'0',True),    # 13
    #     Rule(7,'b',7,'1',True),    # 14
    #     Rule(7,'0',7,'0',True),    # 15
    #     Rule(7,'1',7,'1',True),    # 16
    #     Rule(7,'a',0,'a',False),    # 17
    #     Rule(0,'0',8,'0',True),    # 18
    #     Rule(8,'a',8,'1',True),    # 19
    #     Rule(8,'#',final_state,'#',False),    # 20
    # ]

    final_state = 100
    # 实现pow(x,y)

    rules = {
        # 第一阶段，将x^y转换为x*x*x*x
        Rule(0, '1', 0, '1', False),
        Rule(0, '0', 1, '0', False),
        Rule(1, '1', 2, 'x', False),
        Rule(2, '1', 2, '1', False),
        Rule(2, '$', 2, '$', False),
        Rule(2, '0', 2, '0', False),
        Rule(2, '#', 3, '1#', True),
        Rule(3, '1', 3, '1', True),
        Rule(3, '0', 3, '0', True),
        Rule(3, '$', 4, '$', True),
        Rule(4, '1', 7, '1', True),

        Rule(4, 'x', 5, 'x', False),
        Rule(5, '0', 5, '0', False),
        Rule(5, '1', 5, '1', False),
        Rule(5, '$', 5, '$', False),
        Rule(5, '#', 6, '0#', True),
        Rule(6, '0', 6, '0', True),
        Rule(6, '1', 6, '1', True),
        Rule(6, '$', 11, '$', True),

        Rule(7, '1', 7, '1', True),
        Rule(7, 'x', 8, 'x', False),
        Rule(8, '1', 16, 'x', False),
        Rule(16, '1', 16, '1', False),
        Rule(16, '$', 9, '$', False),
        Rule(9, '1', 9, '1', False),
        Rule(9, '0', 9, '0', False),
        Rule(9, '#', 10, '1#', True),
        Rule(10, '0', 10, '0', True),
        Rule(10, '1', 10, '1', True),
        Rule(10, '$', 4, '$', True),

        Rule(11, 'x', 11, '1', True),
        Rule(11, '0', 12, '0', True),
        Rule(12, 'y', 12, 'y', True),
        Rule(12, '1', 17, 'y', True),
        Rule(17, '1', 13, '1', False),
        Rule(17, '#', 14, '#', False),
        Rule(13, 'y', 13, 'y', False),
        Rule(13, '0', 1, '0', False),

        Rule(14, '0', 14, '0', False),
        Rule(14, '1', 14, '1', False),
        Rule(14, 'y', 14, '1', False),
        Rule(14, '$', 20, '$', False),

        # 第二阶段，计算x*x*x*x
        Rule(20, '0', 20, '0', False),
        Rule(20, '1', 21, 'x', False),
        Rule(21, '1', 21, '1', False),
        Rule(21, '0', 22, '0', False),
        # 处理终态
        Rule(22, '#', 40, '#', True),
        Rule(40, '0', 40, '0', True),
        Rule(40, '1', 40, '1', True),
        Rule(40, 'x', 41, '1', True),
        Rule(41, '0', final_state, '0', True),
        Rule(41, '$', final_state, '$', True),

        Rule(22, '1', 23, 'a', False),
        Rule(23, '1', 23, 'a', False),
        Rule(23, '0', 24, '0', False),

        Rule(24, '#', 25, '#', True),

        Rule(24, '1', 25, '1',True),
        Rule(25, '0', 26, '0',True),
        Rule(26, '1', 26, '1',True),
        Rule(26, 'a', 26, 'a',True),
        Rule(26, '0', 27, '0',True),

        Rule(27,'x',28,'0',True),

        Rule(28,'x',28,'0',True),
        Rule(28,'0',33,'0',False),
        Rule(28,'$',33,'$',False),
        Rule(33,'0',33,'0',False),
        Rule(33,'a',34,'1',False),
        Rule(34,'a',34,'1',False),
        Rule(34,'1',34,'1',False),
        Rule(34,'0',35,'0',True),
        Rule(35,'0',35,'0',True),
        Rule(35,'1',35,'1',True),
        Rule(35,'$',20,'$',False),
        # Rule(33,'1',21,'x',False),
        # Rule(33, 'a', 33, '1', False),

        Rule(27,'1',29,'1',True),
        Rule(29,'1',29,'1',True),
        Rule(29,'x',30,'x',False),
        Rule(30,'1',31,'x',False),
        Rule(31,'1',31,'1',False),
        Rule(31,'0',32,'0',False),
        Rule(32,'1',32,'1',False),
        Rule(32,'a',32,'a1',False),
        Rule(32,'0',24,'0',False),




    }

    # 计算x的y次方
    def caculate(self, x, y):
        # 初始化纸带
        for i in range(x):
            self.tape.append('1')
        self.tape.append('0')
        for i in range(y):
            self.tape.append('1')
        self.tape.append('#')
        self.__excute_rules()

    # 实现复制一个字符串
    def copy_str(self, s):
        for c in s:
            self.tape.append(c)
        self.tape.append('#')
        self.__excute_rules()

    # 实现两数相乘
    def multiply(self, a, b):
        for i in range(a):
            self.tape.append('1')
        self.tape.append('0')
        for i in range(b):
            self.tape.append('1')
        self.tape.append('0')
        self.tape.append('0')
        self.tape.append('#')
        self.__excute_rules()

    # 实现pow(x,y)
    def pow_x_y(self, x, y):
        for i in range(y):
            self.tape.append('1')
        self.tape.append('0')
        for i in range(x):
            self.tape.append('1')
        self.tape.append('$')
        self.tape.append('#')
        self.__excute_rules()

    def __excute_rules(self):
        start_time=time.time()
        while(1):
            if self.current_state == Turing.final_state:
                break
            self.show_tape()
            for rule in Turing.rules:
                if self.current_state == rule.read_state \
                        and self.tape[self.cur] == rule.read_char:
                    # 展示执行的rule的信息
                    if self.cur == 0:
                        print('↑')
                        print('p' + str(self.current_state))
                    else:
                        print('\t' * self.cur + '↑')
                        print('\t' * self.cur + 'p' + str(self.current_state))

                    print('执行规则：', end='')
                    print('(p' + str(rule.read_state) + ',' + rule.read_char + ')=(p' + str(
                        rule.out_state) + ',' + rule.out_content + ',', end='')
                    if rule.next_orientation:
                        print('Left)')
                    else:
                        print('Right)')
                    print('*' * 100)
                    self.current_state = rule.out_state
                    del self.tape[self.cur]
                    for c in rule.out_content[::-1]:
                        self.tape.insert(self.cur, c)
                    if rule.next_orientation:
                        self.cur -= 1
                    else:
                        self.cur += 1
                    break
        self.show_tape()
        print('共花费时间：'+str(time.time()-start_time))

    # 展示纸带
    def show_tape(self):
        for e in self.tape:
            print(e, end='\t')
        print()


if __name__ == '__main__':
    t = Turing()
    # t.multiply(2,3)
    # @todo 未考虑0次方的问题，直接规定x,y属于正整数
    t.pow_x_y(2, 3)
