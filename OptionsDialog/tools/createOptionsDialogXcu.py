#!/opt/libreoffice5.2/program/python
# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
from helper import Elem



def createOptionsXcu(c):  #Creation of OptionsDialog.xcu
    os.chdir(c["src_path"])  # srcフォルダに移動。
    filename =  "OptionsDialog.xcu"
    c["backup"](filename)  # すでにあるファイルをバックアップ
    with open(filename, "w", encoding="utf-8") as f:  # OptionsDialog.xcuファイルの作成
        rt = Elem("oor:component-data", {"oor:name": "OptionsDialog", "oor:package": "org.openoffice.Office", "xmlns:oor": "http://openoffice.org/2001/registry", "xmlns:xs": "http://www.w3.org/2001/XMLSchema", "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance"})  # 根の要素を作成。
        rt.append(Elem("node", {'oor:name': "Nodes"}))
        
        
        rt[-1].append(Elem("node", {'oor:name': "mytools.Extensions", "oor:op": "fuse"}))
        rt[-1][-1].append(Elem("prop",{'oor:name': "Protocols", "oor:type": "oor:string-list"}))
        rt[-1][-1][-1].append(Elem("value", text = "{}:*".format(c["HANDLED_PROTOCOL"])))
        tree = ET.ElementTree(rt)  # 根要素からxml.etree.ElementTree.ElementTreeオブジェクトにする。
        tree.write(f.name, "utf-8", True)  # xml_declarationを有効にしてutf-8でファイルに出力する。   
        print("{} has been created.".format(filename))    
if __name__ == "__main__":
    createOptionsXcu(getConfig())