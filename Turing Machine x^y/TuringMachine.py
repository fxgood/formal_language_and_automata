class Rule:
    def __init__(self,read_state,read_char,out_state,out_content,next_orientation):
        self.read_state=read_state
        self.read_char=read_char
        self.out_state=out_state
        self.out_content=out_content
        self.next_orientation=next_orientation  # True往左，False往右

class Turing:
    final_state=100
    # rules=[
    #     # 读头读入状态，读入字符，转入状态，替换的字符，转向
    #     Rule(0,'1',0,'x',False),
    #     Rule(0,'#',1,'#',True),
    #     Rule(1,'x',2,'1',False),
    #     Rule(2,'1',2,'1',False),
    #     Rule(2,'#',1,'1',True),
    #     Rule(1,'1',1,'1',True),
    #     Rule(1,'#',final_state,'#',False),
    # ]
    rules=[
        Rule(0,'1',1,'a',False),    # 1
        Rule(1,'1',1,'1',False),    # 2
        Rule(1,'0',2,'0',False),    # 3
        Rule(2,'1',3,'b',False),    # 4

        Rule(3,'1',3,'1',False),    # 5
        Rule(3,'0',4,'0',False),    # 6
        Rule(4,'0',5,'1',False),    # 7
        Rule(4,'1',4,'1',False),    # 8
        Rule(5,'#',6,'0',True),    # 9
        Rule(6,'0',6,'0',True),    # 10
        Rule(6,'1',6,'1',True),    # 11
        Rule(6,'b',2,'b',False),    # 12

        Rule(2,'0',7,'0',True),    # 13
        Rule(7,'b',7,'1',True),    # 14
        Rule(7,'0',7,'0',True),    # 15
        Rule(7,'1',7,'1',True),    # 16
        Rule(7,'a',0,'a',False),    # 17
        Rule(0,'0',8,'0',True),    # 18
        Rule(8,'a',8,'1',True),    # 19
        Rule(8,'#',final_state,'#',False),    # 20
    ]

    def __init__(self):
        # self.tape=['#','0','0']
        self.tape=['#']
        self.current_state=0
        self.cur=1

    # 计算x的y次方
    def caculate(self,x,y):
        # 初始化纸带
        for i in range(x):
            self.tape.append('1')
        self.tape.append('0')
        for i in range(y):
            self.tape.append('1')
        self.tape.append('#')
        self.__excute_rules()

    # 实现复制一个字符串
    def copy_str(self,s):
        for c in s:
            self.tape.append(c)
        self.tape.append('#')
        self.__excute_rules()

    # 实现两树相乘
    def multiply(self,a,b):
        for i in range(a):
            self.tape.append('1')
        self.tape.append('0')
        for i in range(b):
            self.tape.append('1')
        self.tape.append('0')
        self.tape.append('0')
        self.tape.append('#')
        self.__excute_rules()

    def __excute_rules(self):
        # 递归终止条件
        if self.current_state==Turing.final_state:
            return
        self.show_tape()
        for rule in Turing.rules:
            if self.current_state==rule.read_state \
                and self.tape[self.cur]==rule.read_char:
                self.current_state=rule.out_state
                del self.tape[self.cur]
                for c in rule.out_content[::-1]:
                    self.tape.insert(self.cur,c)
                if rule.next_orientation:
                    self.cur-=1
                else:
                    self.cur+=1
                break
        # 每当右侧的'#'边界符号被替换掉，立马补上一个新的
        if self.tape[-1]!='#':
            self.tape.append('#')
        self.__excute_rules()

    # 展示纸带
    def show_tape(self):
        for e in self.tape:
            # if e!='#':
            #     print(e,end='\t')
            print(e, end='\t')
        print()

if __name__=='__main__':
    t=Turing()
    t.multiply(2,3)




