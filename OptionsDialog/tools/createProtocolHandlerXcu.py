#!/opt/libreoffice5.2/program/python
# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import os
import sys
from config import getConfig
import types
from helper import Elem
class MenuItem(Elem):
    '''
    oor:node-type="MenuItem"を作成するメソッドをもつElemの派生クラス。
    '''
    def createNodes(self, c, xdic):
        '''
        oor:node-type="MenuItem"のElementのリストを返す。
        
        :param DIC: PYTHON_UNO_Component,IMPLE_NAME,SERVICE_NAME,HANDLED_PROTOCOL
        :type DIC: dict
        :param xdic: Xml Attributes
        :type xdic: dict
        :returns: a list of nodes
        :rtype: list
        '''
        ORDER = "URL","Title","Target","Context","Submenu","ControlType","Width"  # ノードの順を指定。 "ImageIdentifier"ノードは使わないので無視する。
        lst_nd = list()  # ノードをいれるリスト。
        for key in ORDER:
            if key in xdic:
                val = xdic[key]
                if key == "Title":  # タイトルノードのとき
                    nd = Elem("prop", {"oor:name": key, "oor:type": "xs:string"})
                    for lang,txt in val.items():
                        nd.append(Elem("value", {"xml:lang": lang}, text=txt))
                    lst_nd.append(nd)
                elif key == "Submenu":  # サブメニューノードのとき
                    fn = val.pop()  # サブメニュー設定のための関数を取得。
                    if type(fn) is types.MethodType:
                        lst_nd.append(fn(c, val))
                else:  # それ以外のノードの時。
                    nd = Elem("prop", {"oor:name": key,"oor:type": "xs:string"})
                    nd.append(Elem("value", text=val)) 
                    lst_nd.append(nd) 
        return lst_nd 
    def createWindowStateNodes(self, c, xdic):  # ツールバーの設定。
        '''
        Properties for ToolBar
        
        :param DIC: PYTHON_UNO_Component,IMPLE_NAME,SERVICE_NAME,HANDLED_PROTOCOL
        :type DIC: dict
        :param xdic: Xml Attributes
        :type xdic: dict
        :returns: a list of nodes
        :rtype: list
        '''
        ORDER = "UIName","ContextSensitive","Visible","Docked" # ノードの順を指定。
        lst_nd = list()  # ノードをいれるリスト。
        for key in ORDER:
            if key in xdic:
                val = xdic[key]
                if key == "UIName":  # タイトルノードのとき
                    nd = Elem("prop", {"oor:name": key, "oor:type": "xs:string"})
                    for lang, txt in val.items():
                        nd.append(Elem("value", {"xml:lang": lang}, text=txt))
                    lst_nd.append(nd)
                else:  # それ以外のノードの時。
                    nd = Elem("prop", {"oor:name": key, "oor:type": "xs:boolean"})
                    nd.append(Elem("value", text=val)) 
                    lst_nd.append(nd) 
        return lst_nd         
class AddonMenu(MenuItem):  # ツール→アドオン、に表示されるメニュー項目を作成。
    '''
    Tools->Add-Ons->AddonMenu
    '''
    def __init__(self, c):
        super().__init__("node", {'oor:name': "AddonMenu"})  # 変更不可。
        self.append(Elem("node", {'oor:name': "{}.function".format(c["HANDLED_PROTOCOL"]), "oor:op": "replace"}))  # oor:nameの値はノードの任意の固有名。
        self[-1].extend(super().createNodes(c, {"Title": {"en-US": "Add-On example by AddonMenuNode"}, "Context": "com.sun.star.text.TextDocument", "Submenu": ["m1", "m2", self.subMenu]}))  # ここから表示されるメニューの設定。
    def subMenu(self, c, val):
        '''
        サブメニューの作成。 
        
        :param DIC: PYTHON_UNO_Component,IMPLE_NAME,SERVICE_NAME,HANDLED_PROTOCOL
        :type DIC: dict
        :param val: Submenu IDs
        :type val: list
        :returns:  a node for submenu
        :rtype: xml.etree.ElementTree.Element
        
        '''
        nd = Elem("node", {"oor:name": "Submenu"})  # 変更不可。
        i = 0
        nd.append(Elem("node", {"oor:name" :val[i], "oor:op": "replace"}))  # oor:nameの値はノードの任意の固有名。この順でソートされる。
        nd[i].extend(super().createNodes(c, {"URL": "{}:Function1".format(c["HANDLED_PROTOCOL"]), "Title": {"en-US": "Add-On Function 1"}, "Target": "_self"}))
        i += 1
        nd.append(Elem("node", {"oor:name": val[i], "oor:op": "replace"}))  # oor:nameの値はノードの任意の固有名。この順でソートされる。
        nd[i].extend(super().createNodes(c, {"URL": "{}:Function2".format(c["HANDLED_PROTOCOL"]), "Title": {"en-US": "Add-On Function 2"}, "Target": "_self"}))
        return nd
class OfficeMenuBar(MenuItem):  # メインメニューに追加される項目を作成。
    '''
    OfficeMenuBar
    Main Menu Bar
    
    '''
    def __init__(self,DIC):
        super().__init__("node", {'oor:name': "OfficeMenuBar"})  # 変更不可。
        self.append(Elem("node", {'oor:name': c["HANDLED_PROTOCOL"], "oor:op": "replace"}))  # oor:nameの値はノードの任意の固有名。
        self[0].extend(super().createNodes(c, {"Title": {"en-US": "Add-On example by OfficeMenuBar"}, "Target": "_self", "Submenu": ["m1", "m2", "m3", self.subMenu]}))  # ここから表示されるメニューの設定。
    def subMenu(self, c, val):
        nd = Elem("node", {"oor:name": "Submenu"})  # 変更不可。
        i = 0
        nd.append(Elem("node", {"oor:name": val[i], "oor:op": "replace"}))  # oor:nameの値はノードの任意の固有名。この順でソートされる。
        nd[i].extend(super().createNodes(c, {"URL": "{}:Function1".format(c["HANDLED_PROTOCOL"]), "Title": {"en-US": "Add-On Function 1"}, "Target": "_self", "Context": "com.sun.star.text.TextDocument"}))
        i += 1
        nd.append(Elem("node", {"oor:name": val[i], "oor:op": "replace"}))  # oor:nameの値はノードの任意の固有名。この順でソートされる。
        nd[i].extend(super().createNodes(c, {"URL": "private:separator"}))
        i += 1
        nd.append(Elem("node", {"oor:name": val[i], "oor:op": "replace"}))  # oor:nameの値はノードの任意の固有名。この順でソートされる。
        nd[i].extend(super().createNodes(c, {"URL": "", "Title": {"en-US": "Add-On sub menu"}, "Target": "_self", "Submenu": ["m1", self.subMenu2]}))      
        return nd
    def subMenu2(self, c, val):
        nd = Elem("node", {"oor:name": "Submenu"})  # 変更不可。
        i = 0
        nd.append(Elem("node", {"oor:name":val[i], "oor:op":"replace"}))  # oor:nameの値はノードの任意の固有名。この順でソートされる。
        nd[i].extend(super().createNodes(c, {"URL":  "{}:Function2".format(c["HANDLED_PROTOCOL"]), "Title": {"en-US": "Add-On Function 2"}, "Target": "_self", "Context": "com.sun.star.sheet.SpreadsheetDocument"}))
        return nd
class OfficeToolBar(MenuItem):  # ツールバーを作成。
    '''
    OfficeToolBar
    View->Toolbars
    Select this tool bar.
    
    ツールバーの名前は未設定。
    
    '''
    def __init__(self, c):
        super().__init__("node", {'oor:name': "OfficeToolBar"})  # 変更不可。 
        self.append(Elem("node", {'oor:name': c["HANDLED_PROTOCOL"], "oor:op": "replace"}))  # oor:nameの値はノードの任意の固有名。
        self[0].append(Elem("node", {'oor:name': "m1", "oor:op": "replace"}))  # oor:nameの値はノードの任意の固有名。この順でソートされる。  
        self[0][0].extend(super().createNodes(c, {"URL": "{}:Function1".format(c["HANDLED_PROTOCOL"]), "Title": {"en-US": "Function 1"}, "Target": "_self", "Context": "com.sun.star.text.TextDocument"}))
        self[0].append(Elem("node", {'oor:name': "m2", "oor:op": "replace"}))  # oor:nameの値はノードの任意の固有名。この順でソートされる。 
        self[0][1].extend(super().createNodes(c, {"URL": "{}:Function2".format(c["HANDLED_PROTOCOL"]), "Title": {"en-US": "Function 2"}, "Target": "_self", "Context": "com.sun.star.text.TextDocument"}))
        self.createWindwStatexcu(c, "Writer")  # Writer用のツールバーのプロパティの設定。
    def createWindwStatexcu(self, c, ctxt):  # ツールバーのプロパティの設定。
        #Creation of WriterWindwState.xcu、Calcの場合はCalcWindwState.xcu
        filename =  "{}WindowState.xcu".format(ctxt)
        c["backup"](filename)  # すでにあるファイルをbkに改名
        with open(filename, "w", encoding="utf-8") as f:   
            rt = Elem("oor:component-data", {"oor:name": "{}WindowState".format(ctxt), "oor:package": "org.openoffice.Office.UI", "xmlns:oor": "http://openoffice.org/2001/registry", "xmlns:xs": "http://www.w3.org/2001/XMLSchema"})  # 根の要素を作成。
            rt.append(Elem("node", {'oor:name': "UIElements"}))
            rt[-1].append(Elem("node", {'oor:name': "States"}))
            rt[-1][-1].append(Elem("node", {'oor:name': "private:resource/toolbar/addon_{}".format(c["HANDLED_PROTOCOL"]), "oor:op": "replace"}))
            rt[-1][-1][-1].extend(super().createWindowStateNodes(c, {"UIName": {"en-US": "OfficeToolBar Title"}, "ContextSensitive": "false", "Visible": "true", "Docked": "false"}))  # ツールバーのプロパティを設定。
            tree = ET.ElementTree(rt)  # 根要素からxml.etree.ElementTree.ElementTreeオブジェクトにする。
            tree.write(f.name, "utf-8", True)  # xml_declarationを有効にしてutf-8でファイルに出力する。   
            print("{} has been created.".format(filename))  
class Images(MenuItem):  # アイコンを表示させるコマンドURLを設定。
    '''
    Specify command URL to display icon
    '''
    def __init__(self, c):
        super().__init__("node", {'oor:name': "Images"})  # 変更不可。  
        # 画像1
        name = "com.sun.star.comp.framework.addon.image1"  # oor:nameの値はノードの任意の固有名。
        url = "{}:Function1".format(c["HANDLED_PROTOCOL"])  # アイコンを表示させるコマンドURL
        dic_image = {
            "ImageSmallURL": "%origin%/icons/image1ImageSmall.png",
            "ImageBigURL": "%origin%/icons/image1ImageBig.png",
            }
        self.append(self.userDefinedImages(name, url, dic_image))
        # 画像2
        name = "com.sun.star.comp.framework.addon.image2"  # oor:nameの値はノードの任意の固有名。
        url = "org.openoffice.Office.addon.example:Help"  # アイコンを表示させるコマンドURL
        dic_image = {
            "ImageSmallURL":"%origin%/icons/image2ImageSmall.png",
            "ImageBigURL":"%origin%/icons/image2ImageBig.png",
            }        
        self.append(self.userDefinedImages(name, url, dic_image))
    def userDefinedImages(self, name, url, dic_image):  
        '''
        アイコンの設定。
        
        :param name: name of icon
        :type name: str
        :param url: uri of icon
        :type url: str
        :param dic_image:  a dictionary of the same image with different sizes
        :type dic_image: dict
        :returns: a node for an image
        :rtype: xml.etree.ElementTree.Element
        '''
        nd = Elem("node", {"oor:name": name, "oor:op": "replace"})  # oor:nameの値はノードの任意の固有名。
        nd.append(Elem("prop", {"oor:name": "URL"}))
        nd[-1].append(Elem("value", text=url))  # アイコンを表示させるコマンドURLを設定。
        nd.append(Elem("node", {"oor:name": "UserDefinedImages"}))
        ORDER = "ImageSmall", "ImageBig", "ImageSmallHC", "ImageBigHC"
        for key in ORDER:
            if key in dic_image:
                snd = Elem("prop", {"oor:name": key, "oor:type": "xs:hexBinary"})
                snd.append(Elem("value", text=dic_image[key]))
                nd[-1].append(snd)
        ORDER = "ImageSmallURL", "ImageBigURL"  # "ImageSmallHCURL","ImageBigHCURL" valueノードのテキストノードの空白があると画像が表示されない。HC画像が優先して表示されてしまうのでHC画像は使わない。
        for key in ORDER:
            if key in dic_image:
                snd = Elem("prop", {"oor:name": key, "oor:type": "xs:string"})
                snd.append(Elem("value", text=dic_image[key]))
                nd[-1].append(snd)        
        return nd
class OfficeHelp(MenuItem):  # ヘルプメニューの設定。 
    '''
    Help Menu
    '''
    def __init__(self, c):
        super().__init__("node", {'oor:name': "OfficeHelp"})  # 変更不可。  
        self.append(Elem("node", {'oor:name': "com.sun.star.comp.framework.addon", "oor:op": "replace"}))  # oor:nameの値はノードの任意の固有名。           
        self[0].extend(super().createNodes(c, {"URL": "{}:Help".format(c["HANDLED_PROTOCOL"]), "Title": {"x-no-translate": "", "de": "Über Add-On Beispiel", "en-US":" About Add-On Example"}, "Target": "_self"}))


def createProtocolHandlerXcu(c):
    #Creation of ProtocolHandler.xcu
    os.chdir(c["src_path"])  # srcフォルダに移動。
    if c["HANDLED_PROTOCOL"] is not None:  # HANDLED_PROTOCOLの値があるとき
        filename =  "ProtocolHandler.xcu"
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
    createProtocolHandlerXcu(getConfig(False))