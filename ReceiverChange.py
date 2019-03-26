#
# ReceiverChange.py
# Dirac script to change the receiver number and enviroment parameters in selected files
#
# To run this script, copy it to the Documents\Dirac\Plugins folder,
# start Dirac and select the script from the Script menu.
# Alternatively, run Dirac with the script name on the commandline.
#
#
# Copyright 2019 Jakub Orasinski, KudlatyWORKSHOP.com - www.kudlatyworkshop.com
#

# Import the required modules 
import sys
import clr
import System
import DiracLib

clr.AddReference('System.Windows.Forms')
clr.AddReference('System.Drawing')
clr.AddReference('Microsoft.VisualBasic')

from System.IO import Path
from System.Windows.Forms import (OpenFileDialog, DialogResult)
from Microsoft.VisualBasic import Interaction
from DiracLib.App.Settings import Settings

# prompt the user to select a number of files
def GetFileList():
    dlgFile = OpenFileDialog()
    dlgFile.Title = "Select files to change"
    dlgFile.Filter = "Wave files (*.wav)|*.wav"
    dlgFile.InitialDirectory = Settings.Instance().DataDir
    dlgFile.CheckFileExists = True
    dlgFile.CheckPathExists = True
    dlgFile.AddExtension = True
    dlgFile.AutoUpgradeEnabled = True
    dlgFile.DefaultExt = "wav"
    dlgFile.Multiselect = True
    dlgFile.RestoreDirectory = True
    dlgFile.SupportMultiDottedExtensions = True
    dlgFile.FileName = ""
    result = dlgFile.ShowDialog()
    if (result == DialogResult.OK):
        Settings.Instance().DataDir = Path.GetDirectoryName(dlgFile.FileName)
        return dlgFile.FileNames
    else:
        return

# prompt the user for a temperature
def GetTemp():
    result = Interaction.InputBox('Enter Temperature', 'SetTemp', '0')
    return result

# prompt the user for a humidity
def GetHum():
    result = Interaction.InputBox('Enter Humidity', 'SetHum', '0')
    return result

# prompt the user for a pressure
def GetPres():
    result = Interaction.InputBox('Enter Pressure', 'SetPres', '0')
    return result
    

# get the files
files = GetFileList()
if files is not None and len(files) > 0:
    

    # get the parameters
    temp = int(GetTemp())
    hum = int(GetHum())
    pres = int(GetPres())

    distance = 1
    if distance > 0:


        # show output window
        output.Show()
        output.WriteLine('Setting temperature to ' + str(temp) + '[*C]')
        output.WriteLine('Setting humidity to ' + str(hum) + '[%]')
        output.WriteLine('Setting pressure to ' + str(pres) + '[hPa]')
        
        # channel var
        ch = 0
      
        # iterate over all folders
        for file in files:
            ch = ch + 1
            # get file paths
            folder = Path.GetDirectoryName(file)
            name = Path.GetFileNameWithoutExtension(file)
            ext = Path.GetExtension(file)
            newname = folder + '\\' + 'edited_' + str(ch) + '_' + name + ext
            wave = waves.LoadWave(file)
            wave.AudioFile.Temperature = temp
            wave.AudioFile.Humidity = hum
            wave.AudioFile.Pressure = pres
            wave.AudioFile.ReceiverNo = ch
            wave.SaveAs(newname)
            output.WriteLine('Saving as: ' + newname + ' - ok')

            wave.Close()	# make sure to close the file, otherwise you'll run out of memory
        
        output.WriteLine('That\'s all')



