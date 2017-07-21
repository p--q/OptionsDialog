#!/opt/libreoffice5.2/program/python
# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET




def createOptionsXcu(c):
    #Creation of OptionsDialog.xcu
    os.chdir(c["src_path"])  # srcフォルダに移動。
    if c["HANDLED_PROTOCOL"] is not None:  # HANDLED_PROTOCOLの値があるとき
        filename =  "OptionsDialog.xcu"
        c["backup"](filename)  # すでにあるファイルをバックアップ
        with open(filename, "w", encoding="utf-8") as f:  # ProtocolHandler.xcuファイルの作成
            rt = Elem("oor:component-data", {"oor:name": "ProtocolHandler", "oor:package": "org.openoffice.Office", "xmlns:oor": "http://openoffice.org/2001/registry", "xmlns:xs": "http://www.w3.org/2001/XMLSchema", "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance"})  # 根の要素を作成。
            rt.append(Elem("node", {'oor:name': "HandlerSet"}))
            rt[-1].append(Elem("node", {'oor:name': c["IMPLE_NAME"], "oor:op": "replace"}))
            rt[-1][-1].append(Elem("prop",{'oor:name': "Protocols", "oor:type": "oor:string-list"}))
            rt[-1][-1][-1].append(Elem("value", text = "{}:*".format(c["HANDLED_PROTOCOL"])))
            tree = ET.ElementTree(rt)  # 根要素からxml.etree.ElementTree.ElementTreeオブジェクトにする。
            tree.write(f.name, "utf-8", True)  # xml_declarationを有効にしてutf-8でファイルに出力する。   
            print("{} has been created.".format(filename))    
        #Creation of Addons.xcu
        filename =  "Addons.xcu"
        c["backup"](filename)  # すでにあるファイルをバックアップ
        with open(filename, "w", encoding="utf-8") as f:  # Addons.xcuファイルの作成。   
            rt = Elem("oor:component-data", {"oor:name":"Addons", "oor:package": "org.openoffice.Office", "xmlns:oor": "http://openoffice.org/2001/registry", "xmlns:xs": "http://www.w3.org/2001/XMLSchema"})  # 根の要素を作成。
            rt.append(Elem("node", {'oor:name': "AddonUI"}))
            rt[-1].extend([AddonMenu(c), OfficeMenuBar(c), OfficeToolBar(c), Images(c), OfficeHelp(c)])  # 追加するノード。
            tree = ET.ElementTree(rt)  # 根要素からxml.etree.ElementTree.ElementTreeオブジェクトにする。
            tree.write(f.name, "utf-8", True)  # xml_declarationを有効にしてutf-8でファイルに出力する。   
            print("{} has been created.".format(filename))  
if __name__ == "__main__":
    createOptionsXcu(getConfig())