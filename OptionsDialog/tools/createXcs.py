#!/opt/libreoffice5.2/program/python
# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
from helper import Elem
from config import getConfig
import os
def createXcs(c):
	os.chdir(c["src_path"])  # srcフォルダに移動。
	filename =  "config.xcs"
	c["backup"](filename)  # すでにあるファイルをバックアップ	
	with open(filename, "w", encoding="utf-8") as f:  # OptionsDialog.xcuファイルの作成
		root = Elem("oor:component-schema", {"oor:name": "ExtensionData", "oor:package": c["ExtentionID"], "xmlns:oor": "http://openoffice.org/2001/registry", "xmlns:xs": "http://www.w3.org/2001/XMLSchema", "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance", "xml:lang": "en-US"})  # 根の要素を作成。
		root.append(Elem("templates"))
		root[-1].append(Elem("group", {"oor:name": "Size"}))
		root[-1][-1].append(Elem("info"))
		root[-1][-1][-1].append(Elem("desc", text="width and hight."))
		root[-1][-1].append(Elem("prop", {"oor:name": "Width", "oor:type": "xs:string"}))
		root[-1][-1][-1].append(Elem("value", text="300"))
		root[-1][-1].append(Elem("prop", {"oor:name": "Height", "oor:type": "xs:string"}))		
		root[-1][-1][-1].append(Elem("value", text="300"))
		root.append(Elem("component"))
		root[-1].append(Elem("group", {"oor:name": "Leaves"}))
		root[-1][-1].append(Elem("node-ref", {"oor:name": "MaximumPaperSize", "oor:node-type": "Size"}))
		tree = ET.ElementTree(root)  # 根要素からxml.etree.ElementTree.ElementTreeオブジェクトにする。
		tree.write(f.name, "utf-8", True)  # xml_declarationを有効にしてutf-8でファイルに出力する。   
	print("{} has been created.".format(filename))	
if __name__ == "__main__":
	createXcs(getConfig(False))  # バックアップをとるときはTrue