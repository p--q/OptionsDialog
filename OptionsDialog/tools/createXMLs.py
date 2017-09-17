#!/opt/libreoffice5.2/program/python
# -*- coding: utf-8 -*-
import os
import sys
import xml.etree.ElementTree as ET
from helper import Elem
from config import getConfig
import glob
def createVals(dic):  # 辞書をクロージャーにもつ。
	def addVal(element, key, val):  # キー: element、値に辞書を入れてその辞書のキーにkey、値にvalを入れる。
		if element in dic:
			dic[element][key] = val
		else:  # キーがみつからないときは値に辞書を作成。
			dic[element] = {key: val}
	return addVal
def createDescriptionFile(c):  # description.xmlファイルの作成。
	langs = "en", "ja"  # 言語のタプル
	description_file = "description.xml"
	c["backup"](description_file)
	cfg = c["ini"]["description.xml"]  # config.iniを読み込んだconfigparserのdescription.xmlセクションを取得。キーはすべて小文字になっている。
	vals = {}  # configparsarで取得した値を整理して取得する辞書。
	addVal = createVals(vals)
	for key, val in cfg.items():
		if val:  # 値があるときのみ
			flg = False
			for lang in langs: 
				end = "-{}".format(lang)
				if key.endswith(end):  # "publisher", "publisher-url", "license-text", "display-name", "extension-description"
					flg = True
					addVal(key.replace(end, ""), lang, val)
			if flg:
				continue
			if key.endswith("-version"):  # "libreoffice-minimal-version", "libreoffice-maximal-version"
				addVal("dependencies", key.replace("libreoffice", "LibreOffice"), val)  # 小文字を元に戻しておく。
			elif key in ("accept-by", "suppress-on-update", "suppress-if-required"):  # "accept-by", "suppress-on-update", "suppress-if-required"
				addVal("registration", key, val)
			else:  # "identifier", "version", "platform", "icon"
				vals[key] = val  # これらは辞書を入れ子にしない。		
	with open(description_file, "w", encoding="utf-8") as f:
		rt = Elem("description", {"xmlns": "http://openoffice.org/extensions/description/2006", "xmlns:xlink": "http://www.w3.org/1999/xlink", "xmlns:d": "http://openoffice.org/extensions/description/2006", "xmlns:l": "http://libreoffice.org/extensions/description/2011"})
		for element, dic in vals.items():
			if element in ("identifier", "version", "platform"):
				rt.append(Elem(element, {"value": dic}))
			elif element == "display-name":
				rt.append(Elem(element))
				[rt[-1].append(Elem("name", {"lang": lang}, text=txt)) for lang, txt in dic.items()]
			elif element == "extension-description":
				rt.append(Elem(element))
				[rt[-1].append(Elem("src", {"xlink:href": path, "lang": lang})) for lang, path in dic.items()]
			elif element == "publisher":
				rt.append(Elem(element))
				for lang, txt in dic.items():
					try:
						rt[-1].append(Elem("name", {"lang": lang, "xlink:href": vals["publisher-url"][lang]}, text=txt))
					except KeyError:
						print("publisher-url-{} is not defined.".format(lang))
						rt[-1].append(Elem("name", {"lang": lang}, text=txt))				
			elif element == "icon":		
				rt.append(Elem(element))
				rt[-1].append(Elem("default", {"xlink:href": dic}))		
			elif element == "dependencies":
				rt.append(Elem(element))
				[rt[-1].append(Elem("l:{}".format(key), {"value": val, "d:name": "LibreOffice {}".format(val)})) for key, val in dic.items()]			
			elif element == "registration":
				rt.append(Elem(element))
				rt[-1].append(Elem("simple-license", dic))	
				try:
					[rt[-1][-1].append(Elem("license-text", {"xlink:href": val, "lang": lang})) for lang, val in vals["license-text"].items()]
				except KeyError:
					print("license-text is not defined.")
		tree = ET.ElementTree(rt)  # 根要素からxml.etree.ElementTree.ElementTreeオブジェクトにする。
		tree.write(f.name, "utf-8", True)  # xml_declarationを有効にしてutf-8でファイルに出力する。   
		print("{} file has been created.".format(description_file))
def createComponentNode(cp):  # Python UNO Component Fileの登録。
	nd = Elem("component", {"loader": "com.sun.star.loader.Python", "uri": cp["filename"]})
	nd.append(Elem("implementation", {"name": cp["IMPLE_NAME"]}))
	nd[-1].append(Elem("service", {"name": cp["SERVICE_NAME"]}))
	print("{} is registered in the .components file.".format( cp["filename"]))
	return nd
def createComponentsFile(component_file, c):  # .componentファイルの作成。
	c["backup"](component_file)
	with open(component_file, "w", encoding="utf-8") as f:
		rt = Elem("components", {"xmlns": "http://openoffice.org/2010/uno-components"})
		for cp in c["components"]:
			rt.append(createComponentNode(cp))
		tree = ET.ElementTree(rt)  # 根要素からxml.etree.ElementTree.ElementTreeオブジェクトにする。
		tree.write(f.name, "utf-8", True)  # xml_declarationを有効にしてutf-8でファイルに出力する。   
		print("{} file has been created.".format(component_file))
def addXcuNode(f):
	return Elem("manifest:file-entry", {"manifest:full-path":f, "manifest:media-type":"application/vnd.sun.star.configuration-data"})
def addXcsNode(f):
	return Elem("manifest:file-entry", {"manifest:full-path":f, "manifest:media-type":"application/vnd.sun.star.configuration-schema"})
def createManifestFile(component_file, c):  # manifext.xmlファイルの作成
	mani = os.path.join(c["src_path"], "META-INF", "manifest.xml")  # manifest.xmlの絶対パスを取得。
	if not os.path.exists("META-INF"):  # META-INFフォルダがなければ作成する。
		os.mkdir("META-INF")
	else:
		c["backup"](mani)
	with open(mani, "w", encoding="utf-8") as f:
		rt = Elem("manifest:manifest", {"xmlns:manifest":"http://openoffice.org/2001/manifest"})
		xcss = glob.glob("*.xcs")  # xcsファイルのリストを取得。
		for xcs in xcss:
			rt.append(addXcsNode(xcs))
		xcus = glob.glob("*.xcu")  # xcuファイルのリストを取得。
		addonsxcu = "Addons.xcu"
		if addonsxcu in xcus:  # Addons.xcuファイルがあるときは先頭のノードにする。
			rt.append(addXcuNode(addonsxcu))
			xcus.remove(addonsxcu)  # 追加したAddons.xcuファイルをリストから削除。
		for xcu in xcus:  # 他のxcuファイルを追加。
			rt.append(addXcuNode(xcu))
		unordb_file = "{}.uno.rdb".format(c["projectname"])  # rdbファイル名の取得。	
		if os.path.exists(unordb_file):
			rt.append(Elem("manifest:file-entry", {"manifest:full-path": unordb_file, "manifest:media-type": "application/vnd.sun.star.uno-typelibrary;type=RDB"}))
		if os.path.exists(component_file):
			rt.append(Elem("manifest:file-entry", {"manifest:full-path": component_file, "manifest:media-type": "application/vnd.sun.star.uno-components"}))
		tree = ET.ElementTree(rt)  # 根要素からxml.etree.ElementTree.ElementTreeオブジェクトにする。
		tree.write(f.name, "utf-8", True)  # xml_declarationを有効にしてutf-8でファイルに出力する。   
		print("manifest.xml file has been created.")		
def createXMLs(c):
	component_file = "{}.components".format(c["projectname"])  # .componentsファイル名の作成。
	os.chdir(c["src_path"])  # srcフォルダに移動。  
	createComponentsFile(component_file, c)  # .componentファイルの作成。
	createManifestFile(component_file, c)  # manifext.xmlファイルの作成
	createDescriptionFile(c)  # description.xmlファイルの作成。
if __name__ == "__main__":
	createXMLs(getConfig(False))