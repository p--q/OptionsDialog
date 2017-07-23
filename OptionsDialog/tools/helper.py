#!/opt/libreoffice5.2/program/python
# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
class Elem(ET.Element):  
    '''
    キーワード引数textでテキストノードを付加するxml.etree.ElementTree.Element派生クラス。
    '''
    def __init__(self, tag, attrib={},  **kwargs):  # textキーワードは文字列のみしか受け取らない。  
        if "text" in kwargs:  # textキーワードがあるとき
            txt = kwargs["text"]
            del kwargs["text"]  
            super().__init__(tag, attrib, **kwargs)
            self._text(txt)
        else:
            super().__init__(tag, attrib, **kwargs)
    def _text(self, txt):
        self.text = txt
class ElemProp(Elem):  # 値を持つpropノード
	def __init__(self, name, txt):
		super().__init__("prop", {'oor:name': name}) 
		self.append(Elem("value", text=txt))
class ElemPropLoc(Elem):  # 多言語化された値を持つpropノード。
	def __init__(self, name, langs):
		super().__init__("prop", {'oor:name': name})
		for lang, value in langs.items():
			self.append(Elem("value", {"xml:lang": lang}, text=value))