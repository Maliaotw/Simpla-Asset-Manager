import win32com.client
def WMIDateStringToDate(dtmDate):
    strDateTime = ""
    if (dtmDate[4] == 0):
        strDateTime = dtmDate[5] + '/'
    else:
        strDateTime = dtmDate[4] + dtmDate[5] + '/'
    if (dtmDate[6] == 0):
        strDateTime = strDateTime + dtmDate[7] + '/'
    else:
        strDateTime = strDateTime + dtmDate[6] + dtmDate[7] + '/'
        strDateTime = strDateTime + dtmDate[0] + dtmDate[1] + dtmDate[2] + dtmDate[3] + " " + dtmDate[8] + dtmDate[9] + ":" + dtmDate[10] + dtmDate[11] +':' + dtmDate[12] + dtmDate[13]
    return strDateTime

strComputer = "."
objWMIService = win32com.client.Dispatch("WbemScripting.SWbemLocator")
objSWbemServices = objWMIService.ConnectServer(strComputer,"root\cimv2")
colItems = objSWbemServices.ExecQuery("SELECT * FROM Win32_DeviceMemoryAddress")
for objItem in colItems:
    if objItem.Caption != None:
        print ("Caption:" +  objItem.Caption)
    if objItem.CreationClassName != None:
        print ("CreationClassName:" +  objItem.CreationClassName)
    if objItem.CSCreationClassName != None:
        print ("CSCreationClassName:" +  objItem.CSCreationClassName)
    if objItem.CSName != None:
        print ("CSName:" +  objItem.CSName)
    if objItem.Description != None:
        print ("Description:" +  objItem.Description)
    if objItem.EndingAddress != None:
        print ("EndingAddress:" +  objItem.EndingAddress)
    if objItem.InstallDate != None:
        print ("InstallDate:" + WMIDateStringToDate(objItem.InstallDate))
    if objItem.MemoryType != None:
        print ("MemoryType:" +  objItem.MemoryType)
    if objItem.Name != None:
        print ("Name:" +  objItem.Name)
    if objItem.StartingAddress != None:
        print ("StartingAddress:" +  objItem.StartingAddress)
    if objItem.Status != None:
        print ("Status:" +  objItem.Status)