#!/opt/libreoffice5.2/program/python
# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
class Elem(ET.Element):  
    '''
    キーワード引数textでテキストノードを付加するxml.etree.ElementTree.Element派生クラス。
    '''
    def __init__(self, tag, attrib={},**kwargs):  
        if "text" in kwargs:  # textキーワードがあるとき
            txt = kwargs["text"]
            del kwargs["text"]  
            super().__init__(tag,attrib,**kwargs)
            self._text(txt)
        else:
            super().__init__(tag,attrib,**kwargs)
    def _text(self,txt):
        self.text = txt