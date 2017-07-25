#!/opt/libreoffice5.2/program/python
# -*- coding: utf-8 -*-
import glob
import os
import sys
import time
from configparser import ConfigParser
def backUp(backupflg):  # 引数がTrueのときバックアップ。Falseのときはファイルを削除するのみ。 
	def backupFile(filename):  # 引数のファイルがあれば拡張子bkを付けてバックアップにする。
		if os.path.exists(filename):  #ファイルがすでに存在するとき。
			if backupflg:
				bk = "{}.bk{}".format(filename, time.strftime("%Y%m%d_%H%M%S")) # バックアップファイル名の取得。
				os.rename(filename, bk)  # 既存のファイルを拡張子bkをつけて改名。 
				print("The previous version of " + os.path.basename(filename) + " file has been renamed for backup.")  
			else:
				os.remove(filename)  # 既存のファイルを削除。
	return backupFile
def readVariable(py):  # 引数はコンポーネントファイル
	cp = {"filename": py}  # 戻り値の辞書。
	consts = "IMPLE_NAME", "SERVICE_NAME", "HANDLED_PROTOCOL"  # コンポーネントファイルから取得したい定数名
	with open(py, "r") as f:  # pythonpathフォルダにはまだパスが通らずインポートではエラーが出るのでテキストファイルとして読み込む。
		d = {}  # exec()の名前空間を受ける辞書。
		for line in f:  # ファイルの先頭の行から読みこむ
			if  line.startswith(consts):  # 行頭がconstsの要素のいずれかで始まっている時
				exec(line, d)  # dに定数の値を受け取る。
				for const in consts:  # どの定数なのか調べる
					if line.startswith(const):
						cp[const] = d[const]  # 定数を戻り値の辞書に取得。
						break
			elif line.startswith("def"):  # 行頭がdefで始まっている時
				break  # for文を出る。	
	return cp
def getConfig(backupflg=None):
	if backupflg is None:
		backupflg = True
	print("This script uses the name of the PyDev Project name as the name of the oxt file.")
	c = {
		"backup": backUp(backupflg),  # ファイルのバックアップ。backupflg=Falseでバックファイルを作成しない。
		"components": [],  # コンポーネントファイルから読み込んだデータ。コンポーネントファイルが1要素。
		"src_path": os.path.join(os.path.dirname(sys.path[0]), "src"),  # srcフォルダの絶対パスを取得。
		"projectname": os.path.basename(os.path.dirname(sys.path[0])),  # プロジェクトファイル名
		}
	os.chdir(c["src_path"])  # srcフォルダに移動。
	cfgp = ConfigParser()
	cfgp.read("config.ini")
	c["ini"] = cfgp  # config.iniファイルの内容を取得。
	for py in glob.iglob("*.py"):  # srcフォルダの直下にあるpyファイルのリストを取得。
		cp = readVariable(py)  # コンポーネントファイルの定数の辞書を取得。
		if cp:
		 	c["components"].append(cp)
		if py=="optionsdialoghandler.py":
		 	c["ExtentionID"] = cp["IMPLE_NAME"]  # optionsdialoghandler.pyの実装サービス名を拡張期のIDにする。
	return c
if __name__ == "__main__":
	c = getConfig(False)
	print(c)
  
	
	
	
