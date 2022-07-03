#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File     :   main.py
@Time     :   2022/06/04 23:11:07
@Author   :   Last
@Version  :   1.0
@Contact  :   lustrously_@outlook.com
@Software :   Microsoft_VS_Code
'''

import sys
sys.setrecursionlimit(100000)


def main():
    print("Please Enter the Sudoku Line by Line:")
    sudoku = sudoku_in()

    su = Sudoku(sudoku)

    # 找到所有空格子的位置并和它们对应可能填入的数字一起放进字典node_dict
    for position in su.find_empty():
        su.append_node(position)

    print("Initialization Completed.")
    print("Solving...")

    su.dfs_solution(0,su.line_list,su.column_list,su.unit_list)

def sudoku_in() -> list:
    init_sudoku = []
    for _ in range(9):
        line = list(map(int,input().split()))
        init_sudoku.append(line)

    return init_sudoku


class Sudoku():

    def __init__(self,init_sudoku:list) -> None:

        self.node_dict = {} # 所有空格子位置和它们对应的可能填入的数字
        self.line_list = init_sudoku

        self.column_list = []
        for column_number in range(9):
            column = []
            for line_number in range(9):
                column.append(init_sudoku[line_number][column_number])
            self.column_list.append(column)

        self.unit_list = [
            [],[],[],
            [],[],[],
            [],[],[]
        ]
        for i in range(9):
            for j in range(9):
                self.unit_list[3*(i//3)+j//3].append(init_sudoku[i][j])


    # 将空格子的位置和它们对应可能填入的数字组合成键值对填入字典node_dict
    def append_node(self,pos:tuple) -> None:
        self.node_dict[pos] = self.get_possibility(pos=pos)


    # 检查在该位置填入的数字是否符合数独规则
    def check(self,pos:tuple,num:int,line:list,column:list,unit:list) -> bool:
        if line[pos[0]].count(num) >= 1:
            return False
        if column[pos[1]].count(num) >= 1:
            return False
        if unit[3*(pos[0]//3)+pos[1]//3].count(num) >= 1:
            return False

        return True


    # 找到所有空格子的位置
    def find_empty(self) -> tuple:
        self.empty_item = []
        for line_number,line in enumerate(self.line_list):
            for column_numer,item in enumerate(line):
                if item == 0:
                    self.empty_item.append((line_number,column_numer))

        return self.empty_item


    # 获取某位置处的空格子可能填入的数字
    def get_possibility(self,pos:tuple) -> list:
        possibilities = []
        for i in range(1,10):
            if i in self.line_list[pos[0]] or i in self.column_list[pos[1]] or i in self.unit_list[3*(pos[0]//3)+pos[1]//3]:
                continue
            possibilities.append(i)

        return possibilities


    def dfs_solution(self,progress:int,line,column,unit) -> bool:
        while True:
            if progress == len(self.empty_item):
                for lines in line:
                    print(*lines)
                print("Problem Solved.")
                return True
            for item in self.node_dict[self.empty_item[progress]]:
                if self.check(self.empty_item[progress],item,line,column,unit):
                    pos = self.empty_item[progress]
                    line[pos[0]][pos[1]] = item
                    column[pos[1]][pos[0]] = item
                    unit[3*(pos[0]//3)+pos[1]//3][3*(pos[0]%3)+pos[1]%3] = item

                    if self.dfs_solution(progress+1,line,column,unit):
                        return True
                    else:
                        return False

            line[self.empty_item[progress][0]][self.empty_item[progress][1]] = 0
            column[self.empty_item[progress][1]][self.empty_item[progress][0]] = 0
            unit[3*(self.empty_item[progress][0]//3)+self.empty_item[progress][1]//3][3*(self.empty_item[progress][0]%3)+self.empty_item[progress][1]%3] = 0
            return False



if __name__ == "__main__":
    main()