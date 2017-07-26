#!/opt/libreoffice5.2/program/python
# -*- coding: utf-8 -*-
import os
import sys
import xml.etree.ElementTree as ET
from helper import Elem
from config import getConfig
import glob
def createDescriptionFile(c):  # description.xmlファイルの作成。
	langs = "en", "ja"
	description_file = "description.xml"
	c["backup"](description_file)
	cfg = c["ini"]["description.xml"]  # config.iniを読み込んだconfigparserのdescription.xmlセクションを取得。
	vals = {}
	for key, val in cfg.items():
		for lang in langs:
			end = "-{}".format(lang)
			if key.endswith(end):
				element = key.replace(end)	
				if element in vals:
					vals[element].append(val)
				else:
					vals[element] = [val]
			elif key.endswith("-version"):
				element = "dependencies"	
				if element in vals:
					vals[element].append((key, val))
				else:
					vals[element] = [(key, val)]	
			elif key in ("accept-by", "suppress-on-update", "suppress-if-required"):
				element = "registration"			
				if element in vals:
					vals[element].append((key, val))
				else:
					vals[element] = [(key, val)]	
			else:
				vals[key] = val			
	with open(description_file, "w", encoding="utf-8") as f:
		rt = Elem("description", {"xmlns": "http://openoffice.org/extensions/description/2006", "xmlns:xlink": "http://www.w3.org/1999/xlink", "xmlns:d": "http://openoffice.org/extensions/description/2006", "xmlns:l": "http://libreoffice.org/extensions/description/2011"})
		for element, val in vals.items():
			if element == "display-name":
					
					
					
					rt.append(Elem(element))
					if element == "display-name":
						[rt[-1].append(Elem("name", {"lang": lang}, text=val)) for val, lang in vals]
					elif element == "extension-description":
						[rt[-1].append(Elem("src", {"xlink:href": val, "lang": lang})) for val, lang in vals]
					elif element == "publisher":
						[rt[-1].append(Elem("name", {"lang": lang, "xlink:href": url}, text=val)) for val, url, lang in vals]
					
					
			
			
			if key.endswith(["-{}".format(lang) for lang in langs]):
				vals = []
				for lang in langs:
					val = cfg["{}-{}".format(element, lang)]
					if val:
						if element=="publisher":
							url = cfg["{}-url-{}".format(element, lang)]
							vals.append((val, url, lang))
						else:
							vals.append((val, lang))
				if vals:
					rt.append(Elem(element))
					if element == "display-name":
						[rt[-1].append(Elem("name", {"lang": lang}, text=val)) for val, lang in vals]
					elif element == "extension-description":
						[rt[-1].append(Elem("src", {"xlink:href": val, "lang": lang})) for val, lang in vals]
					elif element == "publisher":
						[rt[-1].append(Elem("name", {"lang": lang, "xlink:href": url}, text=val)) for val, url, lang in vals]
				
			
			if key == "identifier":
				if val == "%IMPLE_NAME%":  # IMPLE_NAMEのときはoptiondialoghandler.pyの実装サービス名をIMPLE_NAMEを使う。
					val = c["ExtentionID"]
				Elem(key, {"value": val})
				
				
# 			if key.startswith("publisher", "publisher-url", "license-text", "display-name", "extension-description"):
				
				
		
		
		
	
# 	keys = "identifier", "version", "platform", "LibreOffice-minimal-version", "LibreOffice-maximal-version", "accept-by", "suppress-on-update", "suppress-if-required", "icon"
# 	keys-lang = "publisher", "publisher-url", "license-text", "display-name", "extension-description"
# 	cfgs = {}
# 	for key in keys:
# 		try:
			
	
	
	
	if cfg["identifier"] == "%IMPLE_NAME%":  # IMPLE_NAMEのときはoptiondialoghandler.pyの実装サービス名をIMPLE_NAMEを使う。
		cfg["identifier"] = c["ExtentionID"]
	with open(description_file, "w", encoding="utf-8") as f:
		rt = Elem("description", {"xmlns": "http://openoffice.org/extensions/description/2006", "xmlns:xlink": "http://www.w3.org/1999/xlink", "xmlns:d": "http://openoffice.org/extensions/description/2006", "xmlns:l": "http://libreoffice.org/extensions/description/2011"})
		keys = "identifier", "version", "platform"
		[rt.append(Elem(key, {"value": cfg[key]})) for key in keys if cfg[key]]	
		for key, name in ("icon", "default"),:
			if cfg[key]:
				rt.append(Elem(key))
				rt[-1].append(Elem(name, {"xlink:href": cfg[key]}))						
		for element in "display-name", "extension-description", "publisher":
			vals = []
			for lang in langs:
				val = cfg["{}-{}".format(element, lang)]
				if val:
					if element=="publisher":
						url = cfg["{}-url-{}".format(element, lang)]
						vals.append((val, url, lang))
					else:
						vals.append((val, lang))
			if vals:
				rt.append(Elem(element))
				if element == "display-name":
					[rt[-1].append(Elem("name", {"lang": lang}, text=val)) for val, lang in vals]
				elif element == "extension-description":
					[rt[-1].append(Elem("src", {"xlink:href": val, "lang": lang})) for val, lang in vals]
				elif element == "publisher":
					[rt[-1].append(Elem("name", {"lang": lang, "xlink:href": url}, text=val)) for val, url, lang in vals]
		vals = []
		keys = "LibreOffice-minimal-version", "LibreOffice-maximal-version"
		[vals.append((key, cfg[key])) for key in keys if cfg[key]]
		if vals:
			rt.append(Elem("dependencies"))
			[rt[-1].append(Elem("l:{}".format(key), {"value": val, "d:name": "LIbreOffice {}".format(val)})) for key, val in vals]
		rt.append(Elem("registration"))
		if cfg["accept-by"]:
			ts = "accept-by", "suppress-on-update", "suppress-if-required"
			rt[-1].append(Elem("simple-license", {ts[0]: cfg[ts[0]], ts[1]: cfg[ts[1]], ts[2]: cfg[ts[2]]}))
		for lang in langs:
			val = cfg["license-text-{}".format(lang)]
			if val:
				rt[-1][-1].append(Elem("license-text", {"xlink:href": val, "lang": lang}))	
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
		unordb_file = ".uno.rdb".format(c["projectname"])  # rdbファイル名の取得。	
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