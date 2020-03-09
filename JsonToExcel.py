#!/usr/bin/env python

# coding:utf-8

import pandas


#引用pandas插件处理
def JsonConverToExcels(path, toPath):
    pandas.read_json(path).to_excel(toPath)

def main():
    JsonConverToExcels("G:\\jsonToExcel\\jsonText.json", "G:\\jsonToExcel\\test2.xlsx");

if __name__ == '__main__':
    main()
