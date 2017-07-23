#!/home/pq/anaconda3/bin/python
# -*- coding: utf-8 -*-
import sys
import os
import glob
import subprocess
from config import getConfig
def createRDB(c):
    # 各々のパスの取得。
    uno_path = os.environ["UNO_PATH"]  # programフォルダへの絶対パスを取得。
    regmerge = os.path.join(uno_path, "regmerge")  # regmergeの絶対パスを取得。
    regview = os.path.join(uno_path, "regview")  # regviewの絶対パスを取得。
    sdk_path = os.path.join(os.path.dirname(uno_path), "sdk")  # SDKフォルダへの絶対パスを取得。
    idlc = os.path.join(sdk_path, "bin", "idlc")  # idlcの絶対パスを取得。
    sdkidl_path = os.path.join(sdk_path, "idl")  # SDKのidlフォルダへの絶対パスを取得。
    #すべての存在確認をする。ツールがそろっていなければ終了する。
    for p in [regmerge, regview, idlc, sdkidl_path]:
        if not os.path.exists(p):
            print("Erorr: {} does not exit.".format(p))
            sys.exit()    
    myidl_path = os.path.join(c["src_path"], "idl")  # PyDevプロジェクトのidlフォルダへの絶対パスを取得。
    if os.path.exists(myidl_path):  # idlフォルダがあるとき
        os.chdir(myidl_path)  # idlフォルダに移動
        for i in glob.iglob("*.urd"):  # すでにあるurdファイルを削除。
            os.remove(i)
        for i in glob.iglob("*.idl"):  # 各idlファイルについて
            args = [idlc, "-I.", "-I"+sdkidl_path, "-O..", i]
            subprocess.run(args)  # idlファイルをコンパイルして親フォルダに出力する。
        os.chdir(c["src_path"])  # srcフォルダに移動
        unordb_file = c["projectname"] + ".uno.rdb"  # RDBファイル名を取得。
        c["backup"](unordb_file)  # すでにあるrdbファイルのバックアップ。
        urds = glob.glob("*.urd")  # urdファイルのリストを取得。
        if urds:  # urdファイルがあるとき
            args = [regmerge, unordb_file, "/UCR"]
            args.extend(urds)
            subprocess.run(args)  # mergeKeyName /UCR(UNO core reflection)も追加してurdファイルをuno.rdbファイルにまとめる。
        if os.path.exists(unordb_file):  # rdbファイルができていれば、
#             args = [regview,unordb_file]
#             subprocess.run(args)  # rdbファイルの中身を出力。  
            print("{} creation succeeded.".format(unordb_file))   
            for i in glob.iglob("*.urd"):  # すでにあるurdファイルを削除。
                os.remove(i)        
        else:  # urdファイルが出力されていないとき
            print("urd files are not created.")
if __name__ == "__main__":
    createRDB(getConfig(False))
