#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import os
import math
import tkinter as tk
from   tkinter import *
from   os.path import exists
from   collections import deque


# In[2]:


class Huff_Node(object):
    def __init__(self, value='', L = None, R = None, na = False,):
        self.V = value
        self.L = L
        self.R = R
        self.na = na
    def set_value(self, value):
        self.V = value
    def get_value(self):
        return self.V
    def set_child_L(self, L):
        self.L = L
    def set_child_R(self, R):
        self.R = R
    def get_child_L(self):
        return self.L
    def get_child_R(self):
        return self.R
    def has_child_L(self):
        return self.L != None
    def has_child_R(self):
        return self.R != None
    def set_na(self, boolean=False):
        self.na = boolean
    def is_na(self):
        return self.na  
    def __str__(self, level=0):
        ret = "\t"*level+repr(self.get_value())+"\n"
        if self.has_child_L():
            ret += (self.get_child_L()).__str__(level+1)
        if self.has_child_R():
            ret += (self.get_child_R()).__str__(level+1)
        return ret
    

    def __repr__(self):
        return str(self)

    
class Huff_Tree:
    def __init__(self, root = Huff_Node(), text = ''):
        self.R = root
        self.text = text
    def set_text(self, text):
        self.text = text
    def set_R(self, node):
        self.R = node
    def set_level_dict(self, d):
        self.level_dict = d
    def get_text(self):
        return self.text
    def get_R(self):
        return self.R
    def get_level_dict(self):
        return self.level_dict

    
    def get_visited(self):
        level   = 1
        visited = []
        node    = self.get_R()
        if not node:
            return []
        elif node is not None:
            node_s  = str(node.get_value()[1])
            size    = len(node_s)
            q       = Queue()
            q.enqueue((node, level))
            last_level = int(np.ceil(math.log2(size)))
            while level <= last_level:
                (node, level) = q.dequeue()
                visited.append((node, level))
                if node.has_child_L():
                    q.enqueue((node.get_child_L(), level+1))
                if node.has_child_R():
                    q.enqueue((node.get_child_R(), level+1))
        visited = [val[0].get_value() for val in visited]
        return visited
    
    def reset(self):
        self.R = None
        self.text = None
        
    def get_dict_variable(self):
        d = {}
        root = self.R.get_value()
        num_chars    = len(root[1])
        letters    = [c for c in root[1]]
        char_count = list(zip(letters,[to_binary(int(n)) for n in range(num_chars)]))
        d          = dict(char_count)
        return d

    def get_dict_fixed(self):
        d      = self.get_dict_variable()
        keys   = list(d.keys())
        values = [(str(v).zfill(5)) for v in list(d.values())]
        new_d  = dict(zip(keys,values))
        return new_d
    
    def __str__(self):
        r = self.get_R()
        ret = str(r)
        return ret
    
    def __repr__(self, level=0):
        return str(self)


# In[3]:


def file_exists(path):
    if os.path.exists(path):
        return True
    else:
        return False

def to_binary(number):
    binarynumber=""
    number = int(number)
    if (number!=0):
        while (number>=1):
            if (number %2==0):
                binarynumber=binarynumber+"0"
                number=number/2
            else:
                binarynumber=binarynumber+"1"
                number=(number-1)/2
    else:
        binarynumber="0"
    return "".join(reversed(binarynumber))



class Queue:
    def __init__(self):
        self.q = deque()
    def enqueue(self, value):
        self.q.appendleft(value)
    def dequeue(self):
        if len(self.q) > 0:
            return self.q.pop()
        else:
            return None
    def __len__(self):
        return len(self.q)
    def __repr__(self):
        if len(self.q) > 0:
            ret = "<enqueue>\n_____________\n"
            ret +=         "\n_____________\n".join([str(val) for val in self.q])
            ret +=         "\n_____________\n<dequeue>"
            return ret
        else:
            return "<empty>"


def return_freq(text):
    if not text:
        return []
    else:
        d = {}
        for char in text:
            if char in d.keys():
                d[char] += 1
            else:
                d[char] = 1

        d = dict(sorted(d.items(), key=lambda item: item[1], reverse = True))
        keys = []
        vals = []
        L = len(d)-1
        for i in range(len(d)-1):
            keys.append(list(d.items())[L-i][0])
            vals.append(list(d.items())[L-i][0])        
        d_ = list(zip(keys,vals))

        return d_

def node_and_children(text):
    if text == '' or text is None:
        return [], [], [], Huff_Node()
    node       = Huff_Node()
    levels, new_list = [], []
    level      = 0
    lst        = return_frequency(text)
    nodes_list = [Huff_Node(v) for v in lst]

    while len(nodes_list)>1:
        node_1,  node_2  = nodes_list.pop(),  nodes_list.pop()
        (v1,c1), (v2,c2) = node_1.get_value(), node_2.get_value()
        node             = Huff_Node((v1+v2,c1+c2))
        node.set_child_L(node_1)
        node.set_child_R(node_2)
        zipped = list(zip([nodes_list],[levels]))
        for (n,l) in [(node_1,level),(node_2,level)]:
            if (n,l) not in zipped:
                new_list.append(n)
                levels.append(l) 
        nodes_list = sort_values(nodes_list, node)
        level -= 1  
    levels   = [l + np.abs(level) for l in levels]
    return levels, new_list, level, node

def sort_nodes(existing_nodes, new_nodes):
    zipped = list(zip([nodes_list],[levels]))
    for (n,l) in [(node_1,level),(node_2,level),(node,level-1)]:
        if (n,l) not in zipped:
            new_list.append(n)
            levels.append(l) 

def sort_node(existing_nodes, one_node):
    stop = False
    i = 0
    val = one_node.get_value()[0]
    while stop == False and i < len(existing_nodes):
        if  val >= existing_nodes[i].get_value()[0]:
            stop = True
        i += 1
    nodes_list = existing_nodes[:i] + [one_node] + existing_nodes[i+1:]
    return nodes_list


def get_root(text):
    return (node_and_children(text))[3]

def get_tree_text(text=''):
    t = Huff_Tree()
    R = get_root(text)
    t.set_R(R)
    return t

def build_tree(text):
    levels, new_list, level, node = node_and_children(text)
    def printtt(node):
        if node:
            print(node)
        if node.has_child_L():
            print('left child')
            printtt(node.get_child_L())
        if node.has_child_R():
            print('right child')
            printtt(node.get_child_R())
    new_dict = dict(zip(levels, []*len(levels)))

    
    new_list_val, levels_val = None, 0
    if len(new_list) > 0:
        new_list_val = new_list[0]
    if len(levels) > 0:
        levels_val = levels[0]
    
    this_n, largest_n, this_key = N, new_list_val, levels_val
    
    
    if len(levels) == 0:
        pass
    else:
        for i in range(len(levels)-1):
            this_n, this_key = new_list[i], levels[i]
            if this_key in set(new_dict.keys()):
                if this_n in new_dict[this_key]:
                    pass
                else:
                    new_dict[this_key] += [this_n]
            else:
                new_dict[levels[i]] = [new_list[i]]
                
    new_dict[0] = [largest_n]
    tree = Huff_Tree()
    tree.set_R(largest_n)
    tree.level_dict = new_dict
    t = Huff_Tree()
    t.set_R(node)
    return t, new_dict

def bubble_sort_rev(freq_list):
    l=len(freq_list)
    for i in range(l-1):
        for j in range(i+1,l):
            if freq_list[i][0]<freq_list[j][0]:
                text         = freq_list[i]
                freq_list[i] = freq_list[j]
                freq_list[j] = text
    return freq_list

def bubble_sort_rev_nodes(nodes):
    nodes = [n.V for n in nodes]
    l=len(nodes)
    for i in range(l-1):
        for j in range(i+1,l):
            if type(nodes[i][0]) != type(nodes[j][0]):
                print('types don\'t match')
                print('i: ' + str(i) + '\nj: ' + str(j))
                print(nodes[i])
                print(nodes[j])
    nodes = [Huff_Node(n) for n in nodes]
    return nodes
    

def return_frequency(text):
    freq_dict = {}
    if not text or text == '':
        return []
    for char in text:
        if char in freq_dict:
            freq_dict[char] += 1
        else:
            freq_dict[char] =  1
    lst = [(v, k) for (k, v) in freq_dict.items()]
    return bubble_sort_rev(lst)


def sort_values(nodes_list=[], node=Huff_Node()):
    node_value, char1 = node.V
    i, max_i = 0, len(nodes_list)
    while True:
        if i == max_i:
            nodes_list.append(node)
            return nodes_list
        current_val, char2 = nodes_list[i].V
        if current_val <= node_value:
            nodes_list.insert(i, node)
            return nodes_list
        i += 1
    return nodes_list

def encode_bin(text=''):
    t = Huff_Tree()
    t.R = Huff_Node()
    t = get_tree_text(text)
    if text == None or text == '':
        return ''
    else:
        d = t.get_dict_fixed()
        codes = ''
        for char in text:
            codes += d[char]
        return t, codes
    
def decode_bin(binary_number,tree):
    if (not binary_number) or (str(binary_number) == ''):
        return ''
    ret = ''
    n   = 5
    binary_number = str(binary_number)
    dict_         = tree.get_dict_fixed()
    reversed_dict = {}

    for value, key in dict_.items():
        reversed_dict[str(key)] = str(value)

    split   = [binary_number[i:i+n] for i in range(0, len(binary_number), n)]
    decoded = [reversed_dict[s] for s in split]
    ret     = ret + ''.join(decoded)
    return ret


# In[4]:


class App:
    def __init__(self, master, original_file = '', encoded_file = '', decoded_file = '', t = None, txt = ''):
        self.master        = master
        self.frame         = tk.Frame(self.master,bd=15,fg=None, bg=None)
        self.frame_encode  = tk.Frame(self.master,bd=15,fg=None, bg=None)
        self.frame_decode  = tk.Frame(self.master,bd=15,fg=None, bg=None)     
        self.error_label   = tk.Label()
        self.tree          = t
        self.text          = txt
        self.this_command  = ''
        self.this_title    = ''
        self.entry_OriginalFileName = original_file
        self.entry_EncodedFileName  = encoded_file
        self.entry_DecodedFileName  = decoded_file

        master.title("Huffman Tree Encoding")
        master.geometry("1028x500")
        master.configure(bg=None)

        ################ Home Page ################ 
    def set_tree(self, tree):
        self.tree = tree
    def set_text(self, text):
        self.text = text
    def set_original(self, filename):
        self.entry_OriginalFileName = filename
    def set_encoded(self, filename):
        self.entry_EncodedFileName = filename
    def set_decoded(self, filename):
        self.entry_DecodedFileName = filename
    def get_tree(self):
        return self.tree
    def get_text(self):
        return self.text
    def get_original(self):
        return self.entry_OriginalFileName
    def get_encoded(self, filename):
        return self.entry_EncodedFileName
    def get_decoded(self, filename):
        return self.entry_DecodedFileName

    def start_up(self):
        for thing in (self.frame, self.frame_encode, self.frame_decode, self.error_label, self.text,
                      self.entry_OriginalFileName, self.entry_EncodedFileName, self.entry_DecodedFileName):
            if thing:
                thing.destroy()
        if self.tree:
            self.tree.reset()
        self.frame = tk.Frame(self.master, bd=15, bg = None)
        #_________ Page info _________ 

        self.page_title = tk.Label(self.frame, text="Huffman Tree Encoding",
                                   font="{U.S. 101} 30 bold",bg=None, fg=None)
        self.page_title.grid(row=0,column=0)

        # encode/decode buttons
        encode_button = tk.Button(self.frame, text='Step 1: Encode', command=self.encode, width=16, bg=None)
        encode_button.grid(row=5, column=0, pady=(10, 0))
        decode_button = tk.Button(self.frame, text='Step 2: Decode', command=self.decode, width=16, bg=None)
        decode_button.grid(row=6, column=0, pady=(10, 0))
        self.frame.pack()



    def main_page(self):
        for thing in (self.frame, self.frame_encode, self.frame_decode, self.error_label):
            if thing:
                thing.destroy()
        self.frame = tk.Frame(self.master, bd=15, bg = None)
        #_________ Page info _________ 

        self.page_title = tk.Label(self.frame, text="Huffman Tree Encoding",
                                   font="{U.S. 101} 30 bold",bg=None, fg=None)
        self.page_title.grid(row=0,column=0)

        # encode/decode buttons
        encode_button = tk.Button(self.frame, text='Step 1: Encode', command=self.encode, width=16, bg=None)
        encode_button.grid(row=5, column=0, pady=(10, 0))
        decode_button = tk.Button(self.frame, text='Step 2: Decode', command=self.decode, width=16, bg=None)
        decode_button.grid(row=6, column=0, pady=(10, 0))
        self.frame.pack()


    def encode(self):    
        if self.frame:
            self.frame.destroy()
        if self.error_label:
            self.error_label.destroy()
        self.frame_encode = tk.Frame(self.master,bg=None)

        #------ filepath entry ------ #
        label_OriginalFileName = tk.Label(self.frame_encode,text='Enter input file path here   >>',
                                        fg=None, bg=None)
        label_OriginalFileName.grid(row=0, column=0, sticky = tk.SE)
        self.entry_OriginalFileName = tk.Entry(self.frame_encode,
                                             width=18, fg=None, bg=None)
        self.entry_OriginalFileName.grid(row=0, column=1, sticky = tk.SE)
        label_EncodedFileName = tk.Label(self.frame_encode,text='Enter output file path here   >>',
                                        fg=None, bg=None)
        label_EncodedFileName.grid(row=1, column=0)
        self.entry_EncodedFileName = tk.Entry(self.frame_encode,
                                             width=18, fg=None, bg=None)
        self.entry_EncodedFileName.grid(row=1, column=1, sticky = tk.S)
        label_left_arrows = tk.Label(self.frame_encode,text='<<',
                                        fg=None, bg=None)
        label_left_arrows.grid(row=0, column=2)
        label_left_arrows = tk.Label(self.frame_encode,text='<<',
                                        fg=None, bg=None)
        label_left_arrows.grid(row=1, column=2)


        # ------ encode button ----- #
        encode_button = tk.Button(self.frame_encode,text='Encoded Text',command=self.go_read_encode,
                                  width=16, bg=None, fg=None)
        encode_button.grid(row=2, column=0, sticky = tk.S)
        encode_button = tk.Button(self.frame_encode,text='Dictionary',command=self.go_read_dict,
                                  width=16, bg=None, fg=None)
        encode_button.grid(row=3, column=0, sticky = tk.S)
        encode_button = tk.Button(self.frame_encode,text='Tree',command=self.go_read_tree,
                                  width=16, bg=None, fg=None)
        encode_button.grid(row=4, column=0, sticky = tk.S)
        exit_button = tk.Button(self.frame_encode,text='Exit',command=self.main_page,
                                  width=16, bg=None, fg=None)
        exit_button.grid(row=5, column=0, sticky = tk.S)
        self.frame_encode.pack()

    def go_read_encode(self):
        self.this_command = 'read_encode'
        self.this_title = 'Encoded Text'
        self.read_encode()
    def go_read_dict(self):
        self.this_command = 'read_dict'
        self.this_title = 'Dictionary'
        self.read_encode()
    def go_read_tree(self):
        self.this_command = 'read_tree'
        self.this_title = 'Huffman Tree'
        self.read_encode()

    def read_encode(self):
        if not file_exists(self.entry_OriginalFileName.get()):
            self.error_label = tk.Label(self.frame_encode, text = 'File does not exist', fg='red')
            self.error_label.grid(row=6,column=0)  
        else:
            if self.error_label:
                self.error_label.destroy()
            self.frame = tk.Frame(self.master)
            original_filename=(self.entry_OriginalFileName).get()
            encoded_filename=(self.entry_EncodedFileName).get()

            with open((self.entry_OriginalFileName).get(), 'r') as f1:
                lines = f1.readlines()
            txt = ''.join(lines)
            t = get_tree_text(txt)
            self.set_tree(t)

            d_fixed = t.get_dict_fixed()
            d_variable = t.get_dict_variable()
            code = encode_bin(txt)[1]
            code


            with open(encoded_filename, 'w') as f2:
                f2.write(code)

            f1.close()
            f2.close()

            if self.this_command == 'read_encode':
                s = ('Original Text:\n\n' + txt +
                     '\n\nEncoded Text:\n\n' + code)
            elif self.this_command == 'read_dict':
                s = '\n\nFixed Length Dictionary:\n\n' + str(d_fixed) + '\n\nVariable Length Dictionary:\n\n' + str(d_variable)
            else:
                s = '\n\nHuffman Tree:\n\n' + str(self.tree)

            def showEncoded_(t):
                showEncoded = Tk()
                showEncoded.title(self.this_title)
                showEncoded.geometry("1500x1000")

                info = Label(showEncoded, text=t, justify=LEFT, wraplength=1000).pack()
                buttonClose = Button(showEncoded, text='exit',
                                     command=showEncoded.destroy).pack(side= BOTTOM, pady = 100)
                showEncoded.mainloop()
            showEncoded_(s)
            self.frame.pack


    def decode(self):    
        if self.get_encoded == None:
            self.error_label = tk.Label(self.frame, text = 'No file to decode', fg=None)
            self.error_label.grid(row=7,column=0)           
        if self.get_original == None:
            self.error_label = tk.Label(self.frame, text = 'Must encode before decoding', fg=None)
            self.error_label.grid(row=7,column=0)
        for thing in (self.frame, self.frame_encode, self.error_label):
            if thing:
                thing.destroy()
        self.frame_decode = tk.Frame(self.master,bg=None)

        #------ filepath entry ------ #
        label_EncodedFileName = tk.Label(self.frame_decode,text='Enter input file path here    >>',
                                        fg=None, bg=None)
        label_EncodedFileName.grid(row=0, column=0, sticky = tk.SE)
        self.entry_EncodedFileName = tk.Entry(self.frame_decode,
                                             width=18, fg=None, bg=None)
        self.entry_EncodedFileName.grid(row=0, column=1, sticky = tk.S)

        label_DecodedFileName = tk.Label(self.frame_decode,text='Enter output file path here    >>',
                                        fg=None, bg=None)
        label_DecodedFileName.grid(row=1, column=0, sticky = tk.S)
        self.entry_DecodedFileName = tk.Entry(self.frame_decode,
                                             width=18, fg=None, bg=None)
        self.entry_DecodedFileName.grid(row=1, column=1, sticky = tk.S)
        label_left_arrows = tk.Label(self.frame_decode,text='<<',
                                        fg=None, bg=None)        
        label_left_arrows.grid(row=0, column=2)
        label_left_arrows = tk.Label(self.frame_decode,text='<<',
                                        fg=None, bg=None)
        label_left_arrows.grid(row=1, column=2)


        # ------ encode button ----- #
        decode_button = tk.Button(self.frame_decode, text='Decode',command=self.read_decode,
                                  width=16, bg=None, fg=None)
        decode_button.grid(row=2, column=0, sticky = tk.S)
        exit_button = tk.Button(self.frame_decode,text='Exit',command=self.main_page,
                                width=16, bg=None, fg=None)
        exit_button.grid(row=3, column=0, sticky = tk.S)
        self.frame_decode.pack()


    def read_decode(self):
        if not file_exists(self.entry_EncodedFileName.get()):
            self.error_label = tk.Label(self.frame_decode, text = 'Invalid file path', fg='red')
            self.error_label.grid(row=4,column=0)   
        else:
            if self.error_label:
                self.error_label.destroy()
            self.frame = tk.Frame(self.master)


            encoded_filename = (self.entry_EncodedFileName).get()
            decoded_filename = (self.entry_DecodedFileName).get()

            with open(encoded_filename, 'r') as f1:
                lines = f1.readlines()

            encoded_text = ''.join(lines)
            tree = self.tree
            decoded_text = decode_bin(encoded_text,tree)

            with open(decoded_filename, 'w') as f2:
                f2.write(decoded_text)

            f1.close()
            f2.close()


            def showResults(t):
                showInfo = Tk()
                showInfo.title("Decoded Text")
                showInfo.geometry("1500x1000")

                info = Label(showInfo, text=t, justify=LEFT, wraplength=1000).pack()
                buttonClose = Button(showInfo, text='exit',
                                     command=showInfo.destroy).pack(side= BOTTOM, pady=100)
                showInfo.mainloop()

            showResults('Encoded Text:\n\n' + encoded_text +
                        '\n\nDecoded Text:\n\n' + decoded_text)
            self.frame.pack

root = tk.Tk()
application = App(root)
application.start_up()
root.mainloop()


# In[ ]:




