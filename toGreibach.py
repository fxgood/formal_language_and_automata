class toGreibach:
    def __init__(self, input: dict):
        self.input = input

    # 判断一个字符串是否满足greibach右侧表达式的要求：即A->b 或A->bCDEF
    # 注意，由于已经消除了单一产生式，故不会出现A->B这种形式
    @staticmethod
    def is_greibach_str(s):
        if s[0] >= 'A' and s[0] <= 'Z':
            return False
        if len(s) > 1:
            for char in s[1:]:
                if char >= 'a' and char <= 'z':
                    return False
        return True

    # 替换字符串中某个位置的字符
    @staticmethod
    def replace_char(string, char, index):
        string = list(string)
        string[index] = char
        return ''.join(string)

    # 上下文无关文法转格里巴克范式
    def type_two_grammar_to_Greibach(self):
        # 先消除单一产生式和空产生式
        self.simpilify_expression()
        print('*' * 100)
        self.show_grammar()
        new_dict = {}
        for key in self.input:
            for index_of_right, right_of_key in enumerate(self.input[key]):
                if not toGreibach.is_greibach_str(right_of_key):
                    list_right_of_key=list(right_of_key)
                    for index_of_list,char in enumerate(list_right_of_key):
                        if index_of_list==0:
                            continue
                        if char <= 'z' and char >= 'a':
                            list_right_of_key[index_of_list]=char.upper()+'_1'
                            new_dict[char.upper()+'_1']=char
                    self.input[key][index_of_right]=''.join(list_right_of_key)
        self.input.update(new_dict)

    # 判断一个文法是否为二型文法
    def is_type_two_grammar(self):
        # 对所有式子的左边进行检查，看是否满足0型文法要求（左侧**含有**非终结符）
        for key in self.input.keys():
            if not self.is_have_V(key):
                return False
        # 在0型文法的基础上，检查是否满足1型文法的要求（除了S->ε，左边的长度都要小于等于右边)
        for key in self.input.keys():
            left_len = len(key)
            value_list = self.input[key]
            for value in value_list:
                right_len = len(value)
                # 排除S->ε情况
                if key == 'S' and value == 'ε':
                    continue
                if left_len > right_len:
                    return False
        # 在1型文法的基础上，检查是否满足2型文法的要求(左边只有一个非终结符)
        for key in self.input.keys():
            if not (len(key) == 1 and key <= 'Z' and key >= 'A'):
                return False
        return True

    # 判断是否含有非终结符
    def is_have_V(self, key):
        for char in key:
            if char <= 'Z' and char >= 'A':
                return True
        return False

    # 消除单一产生式、空产生式
    def simpilify_expression(self):
        # 消除右侧以非终结符开头的式子
        still_have_V_start = True
        while still_have_V_start:
            still_have_V_start = False
            for key in self.input:
                for index_of_right_expression, right_expression in enumerate(self.input[key]):
                    start_char = right_expression[0]
                    if start_char >= 'A' and start_char <= 'Z':
                        still_have_V_start = True
                        # 删除该式子
                        del self.input[key][index_of_right_expression]
                        # 添加新式子
                        for right in self.input[start_char]:
                            new_add = right_expression.replace(start_char, right)
                            if new_add not in self.input[key]:
                                self.input[key].insert(0, new_add)

        # 消除空产生式
        for key in self.input:
            for index, right_expression in enumerate(self.input[key]):
                if right_expression == '#':
                    del self.input[key][index]
                    for left in self.input:
                        for right in self.input[left]:
                            if key in right:
                                new_add = right.replace(key, '')
                                if new_add not in self.input[left]:
                                    self.input[left].insert(0, new_add)

    #  展示文法
    def show_grammar(self):
        for key in self.input:
            print(key + "——>", end='')
            for index, right in enumerate(self.input[key]):
                if index != 0:
                    print('|', end='')
                print(right, end='')
            print()


# 写一个二型文法输入，其对应的语言而二型语言
type_two_grammar_1 = {
    'S': ['aAbBC'],
    'A': ['aA', 'B', '#'],
    'B': ['bcB', 'Cca'],
    'C': ['cC', 'c']
}
type_two_grammar_2 = {
    'S':['AB'],
    'A':['aAb','bB','b'],
    'B':['b']
}
type_two_grammar_3 = {
    'S':['DD','a'],
    'D':['SS','b'],
}

a = toGreibach(type_two_grammar_2)
a.show_grammar()
a.type_two_grammar_to_Greibach()
print('*' * 100)
a.show_grammar()
