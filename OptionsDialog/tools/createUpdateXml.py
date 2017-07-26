#!/opt/libreoffice5.2/program/python
# -*- coding: utf-8 -*-
from config import getConfig
import xml.etree.ElementTree as ET
from helper import Elem
def createUpdateXml(c):
    update_file = "{}.update.xml".format(c["projectname"])
    c["backup"](update_file) 
    with open(update_file, "w", encoding="utf-8") as f:
        rt = Elem("description", {"xmlns": "http://openoffice.org/extensions/update/2006", "xmlns:xlink": "http://www.w3.org/1999/xlink"})
        cfg = c["ini"]["description.xml"]  # config.iniを読み込んだconfigparserのdescription.xmlセクションを取得。
        rt.append(Elem("version", {"value": cfg["version"]}))
        rt.append(Elem("identifier", {"value": c["ExtentionID"]}))
        rt.append(Elem("update-download"))
        rt[-1].append(Elem("src", {"xlink:href": "https://github.com/p--q/OptionsDialog/blob/master/OptionsDialog/oxt/OptionsDialog.oxt"}))
        tree = ET.ElementTree(rt)  # 根要素からxml.etree.ElementTree.ElementTreeオブジェクトにする。
        tree.write(f.name, "utf-8", True)  # xml_declarationを有効にしてutf-8でファイルに出力する。   
    print("{} file has been created.".format(update_file))    
if __name__ == "__main__":
    createUpdateXml(getConfig(False))