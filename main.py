
from tkinter import *
from tkinter.ttk import *
from tkinter.filedialog import askopenfilename


def fu3(q:list):
    l =[]
    for i in q :
        if len(i)>1:
            for j in i:
                l.append(j)
        if len(i) == 1:
            l.append(i)
    q.clear()

    for i in l :
        q.append(i[0])

    return q


def fu1(chomsky_grammar:list , st:str):
    l=[]
    l.append(st)
    s = []
    for i in chomsky_grammar:
        if i[1] == st :
           s.append(i[0])
    l.append(s)
    return l

def fu2(chomsky_grammar:list , st:str, l:list):

    sf = []
    s1 = []
    st1 = st[0]
    for i in l[0]:
        if i[0] == st1 :
                s1.append(i[1])
    st2=st[1:]
    s2 = []
    for i in l[len(st2) - 1]:
        if i[0] == st2:
            s2.append(i[1])

    s1 = fu3(s1)
    s2 = fu3(s2)
    for i,j in zip(s1,s2):
        for k in chomsky_grammar:
            if i+j == k[1]:
                if not k[0] in sf :
                    sf.append(k[0])
            if j+i == k[1]:
                if not k[0] in sf:
                    sf.append(k[0])

    ###

    s3 = []
    st1 = st[-1]
    for i in l[0]:
        if i[0] == st1:
            s3.append(i[1])
    st2 = st[:-1]
    s4 = []
    for i in l[len(st2) - 1]:
        if i[0] == st2:
            s2.append(i[1])


    s3 = fu3(s3)
    s4 = fu3(s4)
    for i, j in zip(s3, s4):
        for k in chomsky_grammar:
            if i + j == k[1]:
                if not k[0] in sf:
                    sf.append(k[0])
            if j + i == k[1]:
                if not k[0] in sf:
                    sf.append(k[0])


    return [st, sf]


def cyk (chomsky_grammar:list , st:str):
    l=[]
    for i in range(len(st)):
        l.append([])

    for i in st:
        l[0].append(fu1(chomsky_grammar,i))

    for i in range(1,len(st)):
        for j in range(len(st)-i):
            l[i].append(fu2(chomsky_grammar,st[j:j+i+1] , l))


    # for i in l:
    #     print(i)

    if "S" in l[-1][0][-1]:
        return True
    else:
        return False




def re(grammer: list):
    class Edge:
        def __init__(self, src, dst, weight):
            self.src = src
            self.dst = dst
            self.weight = weight

        def __str__(self):
            return self.src + '\t' + self.dst + '\t' + self.weight

    def find_dst(string: str):
        for i in range(len(string)):
            if string[i].isupper():
                return string[:i], string[i:]
        return string, 'FINAL'

    def decode(label: int, n: int):
        result = 'S' if label == 0 else chr(label + 64)
        if label == n:
            result = 'FINAL'
        return result

    def check_nodes(n1, n2):
        for i in graph:
            if i.src == n1 and i.dst == n2:
                return i.weight
        return -1

    def find_parent(nodes: list, path: list, parent_for_cycle: list, vertex, init):
        if vertex == init:
            return init
        if vertex == parent_for_cycle[vertex]:  # if we have TOGHE throws Error
            return -1
        if type(path) != None:
            # print(vertex,parent_for_cycle[vertex],'vertex print')
            nodes.append(vertex)
            path.append(
                check_nodes(decode(vertex, len(grammer_dict)), decode(parent_for_cycle[vertex], len(grammer_dict))))
        return find_parent(nodes, path, parent_for_cycle, parent_for_cycle[vertex], init)

    def check_cycles(start: int):
        for i in range(len(node_cycles)):
            if start == node_cycles[i][0]:
                return i
        return -1

    def define_path(parent_for_cycle: list, path_name: list, n1: int, n2: int):
        if parent_for_cycle[n1] == n2:
            path_name.append(
                check_nodes(decode(n1, len(grammer_dict)), decode(parent_for_cycle[n1], len(grammer_dict))))
            return n1
        path_name.append(check_nodes(decode(n1, len(grammer_dict)), decode(parent_for_cycle[n1], len(grammer_dict))))
        return define_path(parent_for_cycle, path_name, parent_for_cycle[n1], n2)

    def convert():
        parent = list()
        parent_for_cycle = list()
        for i in range(len(grammer_dict)):
            parent_for_cycle.append(i)
        for i in range(len(grammer_dict) + 1):  # 1 extra size for final state
            parent.append(i)
            # print(i,parent[i])
        # we assume that ord('S') is 0
        all_nodes = list()
        for i in graph:
            if i.dst == 'FINAL':
                ord_src = ord(i.src) % 32
                ord_dst = len(grammer_dict)
            else:
                ord_src = ord(i.src) % 32
                ord_dst = ord(i.dst) % 32
            if ord_src == 19:
                ord_src = 0
            if ord_dst == 19:
                ord_dst = 0
            parent[ord_src] = ord_dst
        for i in all_without_final:
            ord_src = ord(i.src) % 32
            ord_dst = ord(i.dst) % 32
            if ord_src == 19:
                ord_src = 0
            if ord_dst == 19:
                ord_dst = 0
            parent_for_cycle[ord_src] = ord_dst

        # print(parent_for_cycle)
        road_to_final = list()
        for i in range(len(parent) - 1):
            if parent[i] == len(grammer_dict):
                road_to_final.append(i)
        # print(road_to_final)
        for i in range(len(parent_for_cycle)):
            path = list()
            nodes = list()
            # print(i,parent_for_cycle[i],'before')
            if find_parent(nodes, path, parent_for_cycle, parent_for_cycle[i], i) == i:
                nodes.insert(0, i)
                path.insert(0,
                            check_nodes(decode(i, len(grammer_dict)), decode(parent_for_cycle[i], len(grammer_dict))))
                # print(i,parent_for_cycle[i],'after')
                # print(path)
                # print('--------------------------')
                if path not in cycles:
                    cycles.append(path)
                if nodes not in node_cycles:
                    node_cycles.append(nodes)
        # print(cycles)
        # print(node_cycles)
        weight_of_cycles = list()
        for i in grammer_dict.keys():
            ord_src = ord(i) % 32
            if ord_src == 19:
                ord_src = 0
            all_nodes.append(ord_src)
        final_res = list()
        # print(all_nodes)
        for each in road_to_final:
            ind = check_cycles(each)
            if ind != -1:
                solve = ''
                if each != 0:
                    path_name = list()
                    # print(each,'each is')
                    define_path(parent_for_cycle, path_name, 0, each)
                    # path_name.insert(0, check_nodes('S', decode(parent_for_cycle[0],len(grammer_dict))))
                    # print(path_name)

                    solve += ''.join(x for x in path_name)
                if -1 not in cycles[ind]:
                    solve += '(' + ''.join(x for x in cycles[ind]) + ')*'
                if each in road_to_final:
                    solve += check_nodes(decode(each, len(grammer_dict)), 'FINAL')
                final_res.append(solve)
            elif each not in road_to_final:
                continue
        final = '+'.join(x for x in final_res)
        return final

    def l2d(grammer: list):
        # grammer.sort()
        grammer_final = dict()
        for each in grammer:
            if each[0] in grammer_final.keys():
                grammer_final[each[0]].append(each[1])
            else:
                grammer_final[each[0]] = list()
                grammer_final[each[0]].append(each[1])
        return grammer_final

    def check_state(string: str):
        for i in string:
            if i.isupper():
                return True
        return False

    grammer_dict = l2d(grammer)
    # grammer_dict['S'] = ['aB','b']
    # grammer_dict['A'] = ['aS','aa']
    # grammer_dict['B'] = ['cA','d']
    graph = list()
    all_without_final = list()
    cycles = list()
    node_cycles = list()
    for each in grammer_dict.keys():
        dst = grammer_dict[each]
        for i in dst:
            node = Edge(each, find_dst(i)[1], find_dst(i)[0])
            if check_state(i):
                all_without_final.append(node)
            graph.append(node)
    return convert()


def find_max_ord (l:list):
    ll =[ ]
    for i in l:
        ll.append(ord(i))
    return max(ll)

def find_fist_upper(st:str):
    for i in range(len(st)):
        if st[i].isupper():
            return i
            break
        else:
            return -1


def to_chomsky_form(grammar : list):

    grammar_keys=[]
    for i in grammar:
        grammar_keys.append(i[0])
    sn = find_max_ord(grammar_keys) + 1
    chomsky=[]
    for i in grammar:
        if len(i[1]) == 1:
            chomsky.append([i[0],i[1]])
            for k in grammar:
                if i[1] in k[1]:
                    k[1].replace(i[1],i[0])
        # elif i[1].isupper():
        #     for k in i[1]:
        #         chomsky.append([i[0], i[1]])
        else:
            for j in i[1]:
                if j.islower():
                    chomsky.append( [chr(sn) ,j ] )
                    for k in grammar:
                        if j in k[1]:
                            k[1].replace(j, chr(sn))
                    sn += 1
    return chomsky


class gui:

    def btn0_listener(self):
        self.win0.destroy()
        self.window1()

    def __init__(self):
        self.win0 = Tk()
        self.win0.resizable(False, False)
        self.win0.geometry("300x280")
        self.win0.title("Hello")
        s = '''
        Formal Languages and
          Automata Project
        
            Arshia Hemmat
          Alireza Tabatabaei
        
        
         University of Isfahan
                     2021
        '''

        lb0 = Label(self.win0, text=s).pack()
        btn0 = Button(self.win0, text='START', command=self.btn0_listener).pack()
        self.grams = []
        self.strs=[]
        mainloop()



    def btn_strings_listener(self):
        self.strs = []
        addr = askopenfilename()
        f = open(addr)
        for i in f:
            self.strs.append(i)
        self.result_win()

    def btn_grams_listener(self):
        self.grams = []
        addr = askopenfilename()
        #print(addr)
        f = open(addr)
        for i in f:
            self.grams.append(i.split())



    def window1(self):
        self.win1 = Tk()
        self.win1.resizable(False, False)
        self.win1.title("options")
        self.btn1 = Button(self.win1, text="select grammar file", command=lambda: self.btn_grams_listener())
        self.btn2 = Button(self.win1, text="select expression file", command=lambda: self.btn_strings_listener())
        #self.btn3 = Button(self.win1, text="Show result", command=self.result_win())
        self.btn1.pack()
        self.btn2.pack()
        #self.btn3.pack()
        mainloop()

    def result_win(self):
        self.win1.destroy()
        s = '\n\n\n the regular expresion is \n'+ re(self.grams)+"\n\n\n"
        for i in self.strs:
            s += 'the depence string  '+ i  + '  to this language is   '+ str(cyk(self.grams,i))+"\n\n"
        self.winn = Tk()
        self.winn.title("result")
        lbn = Label(self.winn, text=s).pack()
        mainloop()


if __name__ == '__main__':

    guie = gui()