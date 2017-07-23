#!/opt/libreoffice5.2/program/python
# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
from helper import Elem, ElemProp, ElemPropLoc
from config import getConfig
import os
class ElemLeaf(Elem):  # node-type=Leaf
	def __init__(self, name, c):
		super().__init__("node", {'oor:name': name, "oor:op": "fuse"})
		self.append(ElemProp("Id", c["ExtentionID"]))  # 拡張機能マネージャーのオプションボタンで表示させるオプションページのみ拡張機能IDにする。
		self.append(ElemPropLoc("Label", {"en-US": "Maximum Paper Size", "ja-JP": "最大用紙サイズ"}))  # 拡張機能のロードマップコントロールの副項目名。
		self.append(ElemProp("OptionsPage", "%origin%/dialogs/optionsdialog.xdl"))  # オプションダイアログxdlファイル名。UnoControlDialogオブジェクトになる。
		self.append(ElemProp("EventHandlerService", c["ExtentionID"]))  # オプションダイアログの呼び出しと共に呼び出す実装サービス名。
# 		self.append(ElemProp("GroupId", "GropuIDString"))
# 		self.append(ElemProp("GroupIndex", "int"))
class ElemNode(Elem):  # node-type=Node
	def __init__(self, name, c):
		super().__init__("node", {'oor:name': name, "oor:op": "fuse"})
		self.append(ElemPropLoc("Label",  {"en-US": "Extensions", "ja-JP": "拡張機能"}))
# 		self.append(ElemProp("OptionsPage", "PathToxdlFile"))  # 必要性がわからない。
		self.append(ElemProp("AllModules", "false"))  # どのモジュールで表示させるかはnode-type=Moduleで指定する。
# 		self.append(ElemProp("GroupId", "GropuIDString"))
# 		self.append(ElemProp("GroupIndex", "int"))
		self.append(Elem("node", {'oor:name': "Leaves"}))  # セットノードLeaves
		self[-1].append(ElemLeaf("Leaf1", c))  #  node-type=LeafをセットノードLeavesに追加。
class ElemOrderdNode(Elem):  # node-type=OrderdNode
	def __init__(self, node):  # nodeはノード名。
		super().__init__("node", {'oor:name': node, "oor:op": "fuse"})	
# 		self.append(ElemProp("Index", "0"))  # 位置の指定。省略可。
class ElemModeule(Elem):  # node-type=Module
	def __init__(self, module, nodes):  # moduleはオプションダイアログを表示させるモジュールを指定。有効にするためにはnode-type=NodeのAllModulesをfalseにする必要がある。
		super().__init__("node", {'oor:name': module, "oor:op": "fuse"})
		self.append(Elem("node", {'oor:name': "Nodes"}))  # セットノードNodes
		for node in nodes:
			self[-1].append(ElemOrderdNode(node))  #  node-type=OrderdNodeをセットノードNodesに追加。
class ElemSingleOption(Elem):  #  node-type=SingleOption
	def __init__(self, name):
		super().__init__("node", {'oor:name': name, "oor:op": "fuse"})
		self.append(ElemProp("Hide", "true"))
class ElemOptionsPage(Elem):  #  node-type=OptionsPage
	def __init__(self, name):
		super().__init__("node", {'oor:name': name, "oor:op": "fuse"})
		self.append(ElemProp("Hide", "true"))
# 		self.append(Elem("node", {'oor:name': "Options"}))  # セットノードOptions。
# 		self[-1].append(ElemSingleOption("Op1"))  #  node-type=SingleOptionをセットノードOptionsに追加。
class ElemOptionsGroup(Elem):  #  node-type=OptionsGroup
	def __init__(self, name):
		super().__init__("node", {'oor:name': name, "oor:op": "fuse"})
# 		self.append(ElemProp("Hide", "true"))
		self.append(Elem("node", {'oor:name': "Pages"}))  # セットノードPages。
		self[-1].append(ElemOptionsPage("Security"))  #  node-type=OptionsPageをセットノードPagesに追加。
def createOptionsDialogXcu(c):  #Creation of OptionsDialog.xcu
	os.chdir(c["src_path"])  # srcフォルダに移動。
	filename =  "OptionsDialog.xcu"
	c["backup"](filename)  # すでにあるファイルをバックアップ
	with open(filename, "w", encoding="utf-8") as f:  # OptionsDialog.xcuファイルの作成
		nodes = "{}.Node1".format(c["ExtentionID"]),  # ロードマップコントロールに表示させる大項目のID。ユニークの必要があると考えるので拡張機能IDにくっつける。
		root = Elem("oor:component-data", {"oor:name": "OptionsDialog", "oor:package": "org.openoffice.Office", "xmlns:oor": "http://openoffice.org/2001/registry", "xmlns:xs": "http://www.w3.org/2001/XMLSchema", "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance"})  # 根の要素を作成。



		root.append(Elem("node", {'oor:name': "OptionsDialogGroups"}))  # セットノードOptionsDialogGroups。オプションページを非表示にする。
		root[-1].append(ElemOptionsGroup("ProductName"))  #  node-type=OptionsGroupをセットノードOptionsDialogGroupsに追加。
# 		root[-1].append(ElemOptionsGroup("LibreOffice Base"))
		
# 		root.append(Elem("node", {'oor:name': "Modules"}))  # セットノードModules。表示させるモジュールを限定する。
# 		root[-1].append(ElemModeule("com.sun.star.text.TextDocument", nodes))  #  node-type=ModuleをセットノードModulesに追加。ノード名はhttps://wiki.openoffice.org/wiki/Framework/Article/Options_Dialog_Configurationのいずれか。	
# 		
# 		root.append(Elem("node", {'oor:name': "Nodes"}))  # セットノードNodes。オプションページを定義。
# 		for node in nodes:
# 			root[-1].append(ElemNode(node, c))  #  node-type=NodeをセットノードNodesに追加。
			
		tree = ET.ElementTree(root)  # 根要素からxml.etree.ElementTree.ElementTreeオブジェクトにする。
		tree.write(f.name, "utf-8", True)  # xml_declarationを有効にしてutf-8でファイルに出力する。   
		print("{} has been created.".format(filename))	
if __name__ == "__main__":
	createOptionsDialogXcu(getConfig(False))  # バックアップをとるときはTrue