#!/opt/libreoffice5.2/program/python
# -*- coding: utf-8 -*-
from config import getConfig
import subprocess
import glob
import os
import shutil
import sys
from itertools import chain
def createOXT(c):
	oxtf = os.path.join(c["src_path"], "..", "oxt")  # oxtフォルダの絶対パスの取得。
	if not os.path.exists(oxtf):  # oxtフォルダがなければ作成する。
		os.mkdir(oxtf)
	oxt = os.path.join(oxtf, "{}.oxt".format(c["projectname"])) # 作成するoxtファイルの絶対パスを取得。
	c["backup"](oxt)  # すでにあるoxtファイルをbkに改名。
	os.chdir(c["src_path"])  # srcフォルダに移動。
	if not shutil.which("zip"):  # zipコマンドの有効を確認。
		print("The zip command must be valid for execution.")
		sys.exit()
	mani = [os.path.join("META-INF", "manifest.xml")]  # manifest.xmlを取得。
	rdbs = glob.glob("*.rdb")  # rdbファイルを取得。
	comps = glob.glob("*.components")  # .componentsファイルを取得。 
	pys = glob.glob("*.py")  # Python UNO Componentファイルを取得。 
	xcus = glob.glob("*.xc?")  # xcu, .xcsファイルを取得。
	icons = glob.glob(os.path.join("icons", "*.png"))  # iconファイルを取得。
	dialogs = glob.glob(os.path.join("dialogs", "**", "*.*"), recursive=True)  # ダイアログフォルダ内のファイルをすべて取得。
	descriptions = ["description.xml", *glob.glob("{}*".format(c["ini"]["description.xml"]["license-text-en"])), *glob.glob(os.path.join("descriptions", "*.txt"))]  # description.xml関連のファイルを取得。
	lst_files = []
	for lst in mani, rdbs, comps, pys, xcus, icons, dialogs, descriptions:  # oxtファイルにいれるファイルリストを取得。
		if lst:
			lst_files.extend(lst)
	args = ["zip", oxt]
	args.extend(lst_files)
	subprocess.run(args)  # 必須ファイルをoxtファイルに収納。
	if os.path.exists("pythonpath"):  # pythonpathフォルダがあるとき
		exts = "py","mo"  # oxtファイルに含めるファイルの拡張子のタプル。
		lst_files = []  # ファイルリストの初期化。
		for ext in exts:
			g = glob.glob(os.path.join("pythonpath", "**", "*.{}".format(ext)), recursive=True)  # 指定拡張子のファイルのパスを取得。
			if g: lst_files.extend(g)  # 指定拡張子のファイルがあるのならリストに追加。
		if not g:
			args = ["zip", "-u", oxt]
			args.extend(lst_files)
			subprocess.run(args)  # pythonpathフォルダをoxtファイルに収納。
if __name__ == "__main__":
	createOXT(getConfig())
	