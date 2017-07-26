#!/opt/libreoffice5.2/program/python
# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
from helper import Elem, ElemProp, ElemPropLoc
from config import getConfig
import os
class ElemLeaf(Elem):  # node-type=Leaf。オプションページのロードマップコントロールの小項目になる。
	def __init__(self, c, attrs):  # 辞書attrのkeyは"Name"	, "Label", "GroupId", "GroupIndex", "Id"。 valueはすべて文字列でいれる。
		if not "Id" in attrs:  # IdがなければNameを代用する。Idを拡張機能Idと同じにすると拡張機能マネージャーでオプションボタンが表示される。
			attrs["Id"] = attrs["Name"]		
		attrs["OptionsPage"] = "%origin%/dialogs/optionsdialog.xdl"  # オプションダイアログxdlファイル名。UnoControlDialogオブジェクトになる。
		attrs["EventHandlerService"] = c["ExtentionID"]  # オプションダイアログの呼び出しと共に呼び出す実装サービス名。
		super().__init__("node", {'oor:name': attrs.pop("Name"), "oor:op": "fuse"})
		for key, val in attrs.items():
			if key=="Label":
				self.append(ElemPropLoc(key, val))
			else:
				self.append(ElemProp(key, val))
class ElemNode(Elem):  # node-type=Node
	def __init__(self, c, attrs, *, leaves=None):  # 辞書attrのkeyはName, Label, OptionsPage, AllModules, GroupId, GroupIndex。 valueはすべて文字列でいれる。
		super().__init__("node", {'oor:name': attrs.pop("Name"), "oor:op": "fuse"})
		for key, val in attrs.items():
			if key=="Label":
				self.append(ElemPropLoc(key, val))
			else:
				self.append(ElemProp(key, val))		
		if leaves is not None:
			self.append(Elem("node", {'oor:name': "Leaves"}))  # セットノードLeaves
			for leaf in leaves:
				self[-1].append(leaf)  #  node-type=LeafをセットノードLeavesに追加。
class ElemOrderdNode(Elem):  # node-type=OrderdNode
	def __init__(self, name, index=None):  # nodeはノード名。
		super().__init__("node", {'oor:name': name, "oor:op": "fuse"})	
		if index is not None:
			self.append(ElemProp("Index", index))  # 位置の指定。省略可。
class ElemModeule(Elem):  # node-type=Module
	def __init__(self, name, nodes):  # moduleはオプションダイアログを表示させるモジュールを指定。有効にするためにはnode-type=NodeのAllModulesをfalseにする必要がある。
		super().__init__("node", {'oor:name': name, "oor:op": "fuse"})
		self.append(Elem("node", {'oor:name': "Nodes"}))  # セットノードNodes
		for node in nodes:
			self[-1].append(node)  #  node-type=OrderdNodeをセットノードNodesに追加。
class ElemSingleOption(Elem):  #  node-type=SingleOption
	def __init__(self, name):
		super().__init__("node", {'oor:name': name, "oor:op": "fuse"})
		self.append(ElemProp("Hide", "true"))
class ElemOptionsPage(Elem):  #  node-type=OptionsPage
	def __init__(self, name, *, hide=None, singleoptions=None):
		super().__init__("node", {'oor:name': name, "oor:op": "fuse"})
		if hide is not None:
			self.append(ElemProp("Hide", "true"))
		if singleoptions is not None:
			self.append(Elem("node", {'oor:name': "Options"}))  # セットノードOptions。
			for singleoption in singleoptions:
				self[-1].append(singleoption)  #  node-type=SingleOptionをセットノードOptionsに追加。
class ElemOptionsGroup(Elem):  #  node-type=OptionsGroup
	def __init__(self, name, *, hide=None, optionspages=None):
		super().__init__("node", {'oor:name': name, "oor:op": "fuse"})
		if hide is not None:
			self.append(ElemProp("Hide", "true"))
		if optionspages is not None:
			self.append(Elem("node", {'oor:name': "Pages"}))  # セットノードPages。
			for optionspage in optionspages:
				self[-1].append(optionspage)  #  node-type=OptionsPageをセットノードPagesに追加。							
def createOptionsDialogXcu(c):  #Creation of OptionsDialog.xcu
	os.chdir(c["src_path"])  # srcフォルダに移動。
	filename =  "OptionsDialog.xcu"
	c["backup"](filename)  # すでにあるファイルをバックアップ
	with open(filename, "w", encoding="utf-8") as f:  # OptionsDialog.xcuファイルの作成
		root = Elem("oor:component-data", {"oor:name": "OptionsDialog", "oor:package": "org.openoffice.Office", "xmlns:oor": "http://openoffice.org/2001/registry", "xmlns:xs": "http://www.w3.org/2001/XMLSchema", "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance"})  # 根の要素を作成。
		
		#オプションページの作成。拡張機能IDのc["ExtentionID"]をNameに使った時はLeafを一つにしないと拡張機能マネージャーでフリーズする。
		root.append(Elem("node", {'oor:name': "Nodes"}))  # セットノードNodesを追加。
		leaf = ElemLeaf(c, {"Name": c["ExtentionID"], "Label": {"en-US": "Maximum Paper Size", "ja-JP": "最大用紙サイズ"}})  # node-type=Leaf。小項目の設定。Idを拡張機能Idと同じc["ExtentionID"]にする。
		name = "{}.Node1".format(c["ExtentionID"])  # ロードマップコントロールに表示させる大項目のID。ユニークの必要があると考えるので拡張機能IDにくっつける。
		node = ElemNode(c, {"Name": name, "Label": {"en-US": "Extensions Example", "ja-JP": "拡張機能の例"}, "AllModules": "false"}, leaves=(leaf,))  # node-type=Node。大項目の設定。
		root[-1].append(node)  #  node-type=NodeをセットノードNodesに追加。

		
		# オプションページを表示させるモジュールを限定する。
		root.append(Elem("node", {'oor:name': "Modules"}))  # セットノードModulesを追加。
		orderednode = ElemOrderdNode(name)  #  node-type=OrderdNode。node-type=NodeのNameで表示させる大項目を指定。
		node = ElemModeule("com.sun.star.text.TextDocument", (orderednode,))  # node-type=Module。表示させるモジュールを指定。第一引数はhttps://wiki.openoffice.org/wiki/Framework/Article/Options_Dialog_Configurationのいずれか。	 
		root[-1].append(node)  #  node-type=ModuleをセットノードModulesに追加。  
		
		# 一部のオプションページを非表示にする。
		root.append(Elem("node", {'oor:name': "OptionsDialogGroups"}))  # セットノードOptionsDialogGroupを追加。
		security = ElemOptionsPage("Security", hide=True)  #  node-type=OptionsPage。非表示にする小項目。セキュリティー。
		memory = ElemOptionsPage("Memory", hide=True)  #  node-type=OptionsPage。非表示にする小項目。メモリー。
		productname = ElemOptionsGroup("ProductName", optionspages=(security, memory))  #  node-type=OptionsGroup。非表示にする大項目。hide=Trueにしていないときは第2引数の小項目のみ非表示にする。
		root[-1].append(productname)  #  node-type=OptionsGroupをセットノードOptionsDialogGroupsに追加。
		internet = ElemOptionsGroup("Internet", hide=True)  #  node-type=OptionsGroup。非表示にする大項目。Internet。
		root[-1].append(internet)  #  node-type=OptionsGroupをセットノードOptionsDialogGroupsに追加。	
		
		tree = ET.ElementTree(root)  # 根要素からxml.etree.ElementTree.ElementTreeオブジェクトにする。
		tree.write(f.name, "utf-8", True)  # xml_declarationを有効にしてutf-8でファイルに出力する。   
	print("{} has been created.".format(filename))	
if __name__ == "__main__":
	createOptionsDialogXcu(getConfig(False))  # バックアップをとるときはTrue