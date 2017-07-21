#!
# -*- coding: utf_8 -*-
import unohelper
from com.sun.star.awt import XContainerWindowEventHandler
from com.sun.star.lang import XServiceInfo
from com.sun.star.awt import XActionListener
from com.sun.star.beans import PropertyValue
from com.sun.star.awt.PosSize import POSSIZE
import traceback
IMPLE_NAME = None
SERVICE_NAME = None
def create(ctx, *args, imple_name, service_name):
	global IMPLE_NAME
	global SERVICE_NAME
	if IMPLE_NAME is None:
		IMPLE_NAME = imple_name 
	if SERVICE_NAME is None:
		SERVICE_NAME = service_name
	return DilaogHandler(ctx, *args)
class DilaogHandler(unohelper.Base, XServiceInfo, XContainerWindowEventHandler):  # UNOコンポーネントにするクラス。
	METHODNAME = "external_event"  # 変更できない。
	def __init__(self, ctx, *args):
		self.ctx = ctx
		self.smgr = ctx.getServiceManager()
		self.readConfig, self.writeConfig = createConfigAccessor(ctx, self.smgr, "/org.openoffice.Office.Common/Drawinglayer")
		self.cfgnames = "MaximumPaperWidth", "MaximumPaperHeight"
	# XContainerWindowEventHandler
	def callHandlerMethod(self, dialog, eventname, methodname):  # ブーリアンを返す必要あり。dialogはUnoControlDialog。 eventnameは文字列initialize, ok, backのいずれか。methodnameは文字列external_event。
		if methodname==self.METHODNAME:  # Falseのときがありうる?
			try:
				if eventname=="initialize":  # オプションダイアログがアクティブになった時
# 					import pydevd; pydevd.settrace(stdoutToServer=True, stderrToServer=True)
					# 		name = dialog.getModel().Name
# 		if name != "mytools_Extensions_MaximumPaperSize":
# 			return
					
					maxwidth, maxheight = self.readConfig(*self.cfgnames)
					buttonlistener = ButtonListener(dialog)
					addControl = controlCreator(self.ctx, self.smgr, dialog)
					addControl("FixedLine", {"PositionX": 5, "PositionY": 13, "Width": 250, "Height": 10, "Label": "Maximum page size"})
					addControl("FixedText", {"PositionX": 11, "PositionY": 39, "Width": 49, "Height": 15, "Label": "Width", "NoLabel": True})
					addControl("NumericField", {"PositionX": 65, "PositionY": 39, "Width": 60, "Height": 15, "Spin": True, "ValueMin": 1, "Value": maxwidth, "DecimalAccuracy": 0})
					addControl("NumericField", {"PositionX": 65, "PositionY": 64, "Width": 60, "Height": 15, "Spin": True, "ValueMin": 1, "Value": maxheight, "DecimalAccuracy": 0})
					addControl("FixedText", {"PositionX": 11, "PositionY": 66, "Width": 49, "Height": 15, "Label": "Height", "NoLabel": True})
					addControl("FixedText", {"PositionX": 127, "PositionY": 42, "Width": 25, "Height": 15, "Label": "cm", "NoLabel": True})
					addControl("FixedText", {"PositionX": 127, "PositionY": 68, "Width": 25, "Height": 15, "Label": "cm", "NoLabel": True})
					addControl("Button", {"PositionX": 155, "PositionY": 39, "Width": 50, "Height": 15, "Label": "~Default"}, {"setActionCommand": "width", "addActionListener": buttonlistener})
					addControl("Button", {"PositionX": 155, "PositionY": 64, "Width": 50, "Height": 15, "Label": "~Default"}, {"setActionCommand": "height", "addActionListener": buttonlistener})
				elif eventname=="ok":  # OKボタンが押された時
					maxwidth = dialog.getControl("NumericField1").getModel().Value
					maxheight = dialog.getControl("NumericField2").getModel().Value
					self.writeConfig(self.cfgnames, (int(maxwidth), int(maxheight)))
				elif eventname=="back":  # 元に戻すボタンが押された時
					maxwidth, maxheight = self.readConfig(*self.cfgnames)
					dialog.getControl("NumericField1").getModel().Value= maxwidth
					dialog.getControl("NumericField2").getModel().Value= maxheight
			except:
				traceback.print_exc()
				return False
		return True
	def getSupportedMethodNames(self):
		return (self.METHODNAME,)	
	# XServiceInfo
	def getImplementationName(self):
		return IMPLE_NAME
	def supportsService(self, name):
		return name == SERVICE_NAME
	def getSupportedServiceNames(self):
		return (SERVICE_NAME,)	
class ButtonListener(unohelper.Base, XActionListener):
	DEFAULTMAXIMUM = 300
	def __init__(self, dialog):
		self.dialog = dialog
	def actionPerformed(self, actionevent):
		cmd = actionevent.ActionCommand
		if cmd == "width":
			self.dialog.getControl("NumericField1").Value = self.DEFAULTMAXIMUM
		elif cmd == "height":
			self.dialog.getControl("NumericField2").Value = self.DEFAULTMAXIMUM
	def disposing(self,eventobject):
		pass
def controlCreator(ctx, smgr, dialog):  # コントロールを追加する関数を返す。
	dialogmodel = dialog.getModel()  # ダイアログモデルを取得。
	def addControl(controltype, props, attrs=None):  # props: コントロールモデルのプロパティ、attr: コントロールの属性。
		if "PosSize" in props:  # ピクセル単位を使うとき
			control = smgr.createInstanceWithContext("com.sun.star.awt.UnoControl{}".format(controltype), ctx)  # コントロールを生成。
			control.setPosSize(props.pop("PositionX"), props.pop("PositionY"), props.pop("Width"), props.pop("Height"), props.pop("PosSize"))  # ピクセルで指定するために位置座標と大きさだけコントロールで設定。
			controlmodel = _createControlModel(controltype, props)  # コントロールモデルの生成。
			control.setModel(controlmodel)  # コントロールにコントロールモデルを設定。
			dialog.addControl(props["Name"], control)  # コントロールをコントロールコンテナに追加。			
		else:  # Map AppFont (ma)のときはダイアログモデルにモデルを追加しないと正しくピクセルに変換されない。		
			controlmodel = _createControlModel(controltype, props)  # コントロールモデルの生成。
			dialogmodel.insertByName(props["Name"], controlmodel)  # ダイアログモデルにモデルを追加するだけでコントロールも作成される。
		if attrs is not None:  # Dialogに追加したあとでないと各コントロールへの属性は追加できない。
			control = dialog.getControl(props["Name"])  # コントロールコンテナに追加された後のコントロールを取得。
			for key, val in attrs.items():  # メソッドの引数がないときはvalをNoneにしている。
				if val is None:
					getattr(control, key)()
				else:
					getattr(control, key)(val)	
	def _createControlModel(controltype, props):  # コントロールモデルの生成。
		if not "Name" in props:
			props["Name"] = _generateSequentialName(controltype)  # Nameがpropsになければ通し番号名を生成。
		controlmodel = dialogmodel.createInstance("com.sun.star.awt.UnoControl{}Model".format(controltype))  # コントロールモデルを生成。UnoControlDialogElementサービスのためにUnoControlDialogModelからの作成が必要。
		if props:
			values = props.values()  # プロパティの値がタプルの時にsetProperties()でエラーが出るのでその対応が必要。
			if any(map(isinstance, values, [tuple]*len(values))):
				[setattr(controlmodel, key, val) for key, val in props.items()]  # valはリストでもタプルでも対応可能。XMultiPropertySetのsetPropertyValues()では[]anyと判断されてタプルも使えない。
			else:
				controlmodel.setPropertyValues(tuple(props.keys()), tuple(values))						
		return controlmodel								
	def _generateSequentialName(controltype):  # 連番名の作成。
		i = 1
		flg = True
		while flg:
			name = "{}{}".format(controltype, i)
			flg = dialog.getControl(name)  # 同名のコントロールの有無を判断。
			i += 1
		return name  
	return addControl  # コントロールコンテナとそのコントロールコンテナにコントロールを追加する関数を返す。
def createConfigAccessor(ctx, smgr, rootpath):
	cp = smgr.createInstanceWithContext("com.sun.star.configuration.ConfigurationProvider", ctx)
	node = PropertyValue(Name="nodepath", Value=rootpath)
	root = cp.createInstanceWithArguments("com.sun.star.configuration.ConfigurationUpdateAccess", (node,))		
	def readConfig(*args):
		if len(args)==1:  # 引数の数が1つのとき
			return root.getHierarchicalPropertyValue(*args) 
		elif len(args)>1:  # 引数の数が2つ以上のとき
			return root.getHierarchicalPropertyValues(args)
	def writeConfig(names, values):
		try:
			if isinstance(names, tuple):  # 引数がタプルのとき
				root.setHierarchicalPropertyValues(names, values)
			else:
				root.setHierarchicalPropertyValue(names, values)
			root.commitChanges()
		except:
			traceback.print_exc()			
	return readConfig, writeConfig
