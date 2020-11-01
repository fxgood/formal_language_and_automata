# 消除无用符号的树形算法
class Node:
    def __init__(self,char=None):
        self.char=char
        self.children=[]
        self.father=None    # 记录父节点

class Flag:
    def __init__(self,flag):
        self.flag=flag

    def changeFlag(self,new_flag):
        self.flag=new_flag

class CleanTree:
    def __init__(self):
        self.root_node=Node('S')
        self.__used_nodes=[]
        self.__useful_nodes=[]


    def bulid_clean_tree(self,current_node,input_dict:dict):
        # 为了实现从根结点到当前节点的通路上，p中的每个产生式最多只能出现一次
        # 在每个非空白节点上记录已经使用的产生式
        if not (current_node.char<='Z' and current_node.char >='A'):
            return
        if current_node.char in self.__used_nodes:
            return
        print('当前处理的根节点为:' +current_node.char)
        self.__used_nodes.append(current_node.char)
        record_dict={}
        for right_str in input_dict[current_node.char]:
            print('当前处理的右侧产生式为:'+right_str)
            # 如果长度为1，则直接创建节点
            if len(right_str)==1:
                new_node=Node(right_str)
                new_node.father=current_node
                current_node.children.append(new_node)
                print('生成'+current_node.char+'子节点：'+str(new_node.char))
                # self.bulid_clean_tree(new_node,input_dict) # 递归创建子树
            # 长度大于1，则创建空白节点
            else:
                new_node=Node()
                new_node.father=current_node
                current_node.children.append(new_node)
                print('生成'+current_node.char+'空白子节点：' + str(new_node.char))
                for every_char in right_str:
                    new_node_2=Node(every_char)
                    new_node_2.father=new_node
                    new_node.children.append(new_node_2)
                    print('生成'+current_node.char+'的孙子节点：' + str(new_node_2.char))
                    # self.bulid_clean_tree(new_node_2,input_dict) # 递归创建子树
        for child in current_node.children:
            if child.char is not None:
                self.bulid_clean_tree(child, input_dict)
            else:
                for grand_child in child.children:
                    self.bulid_clean_tree(grand_child,input_dict)

        # print(current_node.char + "的孩子节点：",end='')
        # for e in current_node.children:
        #     print(e.char,end='\t')
        # print()

    def __cut_useless_nodes(self):
        while(True):
            finished = Flag(True)
            # 如果发生了操作，则将标志finished改成False
            self.__travse_tree_and_cut(self.root_node,finished)
            # 如果遍历完了还是True则已完成
            if finished.flag:
                return

    def __travse_tree_and_cut(self,node,flag):
        should_delete_node_lst=[]
        for child_node in node.children:
            child_node_should_delete=False
            # 对非空白节点进行处理
            if child_node.char!=None:
                # 如果是叶节点
                if (not child_node.children) and child_node.char<='Z' and child_node.char>='A':
                    child_node_should_delete = True
            # 对空白节点进行处理
            else:
                should_delete=False
                for child_child_node in child_node.children:
                    # 如果空白节点的孩子节点是叶节点
                    if (not child_child_node.children)  and child_child_node.char<='Z' and child_child_node.char>='A':
                        should_delete=True
                        break
                if should_delete:
                    child_node_should_delete = True
            if child_node_should_delete:
                should_delete_node_lst.append(child_node)
        for e in should_delete_node_lst:
            flag.changeFlag(False)
            print('删除了'+node.char+'的子节点'+str(e.char))
            node.children.remove(e)


        for child_node in node.children:
            self.__travse_tree_and_cut(child_node,flag)

    def __find_useful_nodes(self,node):
        if node is None:
            return
        if node.char!=None and node.char<='Z' and node.char>='A' and node.char not in self.__useful_nodes:
            self.__useful_nodes.append(node.char)
        for child_node in node.children:
            self.__find_useful_nodes(child_node)

    def return_useful_nodes(self):
        # self.travse()
        # print('*'*100)
        self.__cut_useless_nodes()
        # self.travse()
        # print('*' * 100)
        self.__find_useful_nodes(self.root_node)
        return self.__useful_nodes

    def __travse(self,node):
        if node.char is None:
            print('空节点')
        else:
            print(node.char)
        for child in node.children:
            self.__travse(child)

    def travse(self):
        self.__travse(self.root_node)

class toGreibach:
    def __init__(self,input_grammar:dict):
        self.grammar=input_grammar

    def __eliminate_empty_production(self):
        for key in self.grammar:
            # 如果该非终结符推出空产生式
            if '#' in self.grammar[key]:
                self.grammar[key].remove('#')
                for other_key in self.grammar:
                    if other_key!=key:
                        # 检查右边的情况
                        for right_str in self.grammar[other_key]:
                            if len(right_str)>1 and key in right_str:
                                #@todo 其实这里有大坑，比如BaB B是可空集合中的非终结符，那么消除空产生式有三种情况aB Ba a，目前先不考虑这种情况
                                new_add=right_str.replace(key,'')
                                if new_add!='' and new_add not in self.grammar[other_key]:
                                    self.grammar[other_key].append(new_add)

    def to_greibach(self):
        # 消除无用符号
        p = CleanTree()
        p.bulid_clean_tree(p.root_node, self.grammar)
        useful_nodes=p.return_useful_nodes()
        print(useful_nodes)
        record=[]
        for key in self.grammar:
            if key not in useful_nodes:
                record.append(key)
        for e in record:
            self.grammar.pop(e)
        self.show_grammar()
        # 消除空产生式
        self.__eliminate_empty_production()
        self.show_grammar()

    def show_grammar(self):
        for key in self.grammar:
            print(key + "——>", end='')
            for index, right in enumerate(self.grammar[key]):
                if index != 0:
                    print('|', end='')
                print(right, end='')
            print()
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
    p=CleanTree()
    p.bulid_clean_tree(p.root_node,case_2)
    print(p.return_useful_nodes())

