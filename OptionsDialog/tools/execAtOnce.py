from createIDLs import createIDLs
from createRDB import createRDB
from createProtocolHandlerXcu import createProtocolHandlerXcu
from createOptionsDialogXcu import createOptionsDialogXcu
from createXMLs import createXMLs
from createXcs import createXcs
from createOXT import createOXT
from deployOXT import deployOXT
from config import getConfig
if __name__ == '__main__':
	# シェルコマンドのエラーでは止まらないのでログを最初から確認する必要あり。
	c = getConfig(False)
	
#	 print("\ncreateIDLs\n")
#	 createIDLs(c)   
   
#	 print("\ncreateRDB\n")
#	 createRDB(c)
 
#	 print("\ncreateProtocolHandlerXcu\n")
#	 createProtocolHandlerXcu(c)

# 	print("\ncreateOptionsDialogXcu\n")
# 	createOptionsDialogXcu(c)

# 	print("\ncreateXcs\n")
# 	createXcs(c)

# 	print("\ncreateXMLs\n")
# 	createXMLs(c)
	
	print("\ncreateOXT\n")
	createOXT(c)
	
	print("\ndeployOXT\n")
	deployOXT(c)
	
	print("By running TestPyUnoComponent.py, you can check the operation of the created oxt file.")