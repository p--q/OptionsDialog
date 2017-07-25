#!/opt/libreoffice5.2/program/python
# -*- coding: utf-8 -*-
import os
import sys
import subprocess
import glob
from config import getConfig
def deployOXT(c):
    print("Do not start LibreOffice until Extension Manager is displayed.")
    os.chdir(os.path.join(c["src_path"], "..", "oxt"))  # oxtフォルダの絶対パスの取得。))  # oxtフォルダに移動。
    oxt = glob.glob("*.oxt")  # oxtファイルのリストを取得。
    if oxt:
        oxt_path = oxt[0]
        uno_path = os.path.dirname(os.environ["UNO_PATH"])  # programフォルダへのパスを取得。
        unopkg = os.path.join(uno_path, "program", "unopkg") 
        args = [unopkg, "add", "-f", oxt_path, "--suppress-license"]  # ライセンス表示を抑制する。
        subprocess.run(args) 
        subprocess.run([unopkg, "gui"])
        print("If the error message is not, {} deployment to {} has been successful.".format(oxt_path, os.path.basename(uno_path)))
        print("Restarting the OS may be necessary depending on the error.")
    else:
        print("There is no oxt file.")
if __name__ == "__main__":
    deployOXT(getConfig(False)) 