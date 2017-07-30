# OptionsDialog

Example of LibreOffice extension with an option page

This repository contains the PyDev package ov Eclipse.

## tools

In the tools folder there are scripts that generates files necessary for creating an oxt file.

CreateIDLs.py generates idl files, createRDB.py compiles idl files, createProtocolHandlerXcu.py generates ProtocolHandler.xcu defining the ProtocolHandlercomponent data node, but these are not used to create the oxt file.

### createOptionsDialogXcu.py and createXcs.py

After creating the function createXcs() in createOptionsDialogXcu.py and the function createOptionsDialogXcu() in createXcs.py, execute them to generate OptionsDialog.xcu and config.xcs.

### createXMLs.py

createXMLs.py generates OptionsDialog.components, manifest.xml, and description.xml file.

description.xml is generated from the information in config.ini.

### createOXT.py

createOXT.py locates the necessary files in the src folder, creates an oxt file, and outputs it to the oxt folder.

### deployOXT.py

deployOXT.py deploys the oxt file in LibreOffice extension manager.


