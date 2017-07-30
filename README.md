# OptionsDialog Extension for LibreOffice

Example of LibreOffice extension with an option page

This repository contains the PyDev package of Eclipse.

## Compatibility

This oxt file is Linux and Windows compatible.

## Features

Create controls on the options dialog at runtime

Use Python gettext module for internationalization of the options dialog

Display the option button on LibreOffice Extension Manager

Save values in own component nodes

Restrict display of the options page to Writer only

Hide some options pages

## tools

In the tools folder there are scripts that generates files necessary for composing an oxt file.

These scripts work with Ubuntu 14.04.

They will probably work on Linux.

I do not know at all whether they work on Windows.

createIDLs.py generates idl files, createRDB.py compiles idl files, createProtocolHandlerXcu.py generates ProtocolHandler.xcu defining the ProtocolHandlercomponent data node, but these are not used to create the oxt file.

### createOptionsDialogXcu.py and createXcs.py

After creating the function createXcs() in createOptionsDialogXcu.py and the function createOptionsDialogXcu() in createXcs.py, execute them to generate OptionsDialog.xcu and config.xcs.

### createXMLs.py

createXMLs.py generates OptionsDialog.components, manifest.xml, and description.xml file.

description.xml is generated from the information in config.ini.

### createOXT.py

createOXT.py locates the necessary files in the src folder, creates an oxt file, and outputs it to the oxt folder.

### deployOXT.py

deployOXT.py deploys the oxt file in LibreOffice extension manager.
