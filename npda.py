from clean_tree_method import *
class Rule:
    def __init__(self,read_in_state,out_state,read_char,stack_top,stack_top_replace_str):
        self.read_state=read_in_state   # 读入状态
        self.read_char=read_char        # 读头读入符号
        self.stack_top=stack_top        # 当前栈顶元素

        self.out_state=out_state        # 转向状态
        self.stack_top_replace_str=stack_top_replace_str    # 栈顶更换的串

class NPDA:
    state_symbols=['q^0','q^1','q^2']
    # 'q^3','q^4','q^5','q^6','q^7','q^8','q^9','q^10'
    # 传入一个字典形式的Greibach范式
    def __init__(self,grammar):
        self.tape=['#','#']
        self.state='q^0'
        self.stack=[]   # 用列表模拟一个栈
        self.rules=[Rule('q^0','q^1','#','z','Sz'),
                    Rule('q^1','q^2','#','z','z')]
        # 根据greibach范式生成规则
        # self.transfer_rules={}
        for key in grammar:
            for right_str in grammar[key]:
                if right_str=='#':
                    pass
                elif len(right_str)==1:
                    self.rules.append(Rule('q^1','q^1',right_str,key,'#'))
                else:
                    self.rules.append(Rule('q^1', 'q^1', right_str[0], key, right_str[1:]))

    def show_rules(self):
        for e in self.rules:
            print('$('+e.read_state+','+e.read_char+','+e.stack_top+')=('+e.out_state+','+e.stack_top_replace_str+')')

if __name__=='__main__':
    case_1={
        'S':['0','0A','E'],
        'A':['0A','1A','B','#'],
        'B':['0C'],
        'C':['0','1','0C','1C'],
        'D':['1','1D','2D'],
        'E':['0E2','E02'],
    }
    case_2 = {
        'S': ['aAbBC'],
        'A': ['aA', 'B', '#'],
        'B': ['bcB', 'Cca'],
        'C': ['cC', 'c']
    }
    case_3={
        'S':['aABC','a'],
        'A':['aA','a','#'],
        'B':['bcB','bc','C','#'],
        'C':['cC','cb']
    }
    case_4={
        'S':['aSbb','a']
    }
    case_5={
        'S':['aA'],
        'A':['aABC','bB','a'],
        'B':['b'],
        'C':['c']
    }
    p=toGreibach(case_4)
    p.to_greibach()
    NPDA(case_5).show_rules()
