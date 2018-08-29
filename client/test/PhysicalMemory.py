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
        strDateTime = strDateTime + dtmDate[0] + dtmDate[1] + dtmDate[2] + dtmDate[3] + " " + dtmDate[8] + dtmDate[
            9] + ":" + dtmDate[10] + dtmDate[11] + ':' + dtmDate[12] + dtmDate[13]
    return strDateTime


strComputer = "."
objWMIService = win32com.client.Dispatch("WbemScripting.SWbemLocator")
objSWbemServices = objWMIService.ConnectServer(strComputer, "root\cimv2")
colItems = objSWbemServices.ExecQuery("SELECT * FROM Win32_PhysicalMemory")
for objItem in colItems:

    if objItem.BankLabel != None:
        print("BankLabel:" + objItem.BankLabel)
    if objItem.Capacity != None:
        print("Capacity:" + objItem.Capacity)
    if objItem.Caption != None:
        print("Caption:" + objItem.Caption)
    if objItem.CreationClassName != None:
        print("CreationClassName:" + objItem.CreationClassName)
    if objItem.DataWidth != None:
        print ("DataWidth:%s" %  objItem.DataWidth)
    if objItem.Description != None:
        print("Description:" + objItem.Description)
    if objItem.DeviceLocator != None:
        print("DeviceLocator:" + objItem.DeviceLocator)
    if objItem.FormFactor != None:
        print("FormFactor:%s" % objItem.FormFactor)
    if objItem.HotSwappable != None:
        print("HotSwappable:" + objItem.HotSwappable)
    if objItem.InstallDate != None:
        print("InstallDate:" + WMIDateStringToDate(objItem.InstallDate))
    if objItem.InterleaveDataDepth != None:
        print("InterleaveDataDepth:" + objItem.InterleaveDataDepth)
    if objItem.InterleavePosition != None:
        print("InterleavePosition:" + objItem.InterleavePosition)
    if objItem.Manufacturer != None:
        print("Manufacturer:" + objItem.Manufacturer)
    if objItem.MemoryType != None:
        print("MemoryType:%s" % objItem.MemoryType)
    if objItem.Model != None:
        print("Model:" + objItem.Model)
    if objItem.Name != None:
        print("Name:" + objItem.Name)
    if objItem.OtherIdentifyingInfo != None:
        print("OtherIdentifyingInfo:" + objItem.OtherIdentifyingInfo)
    if objItem.PartNumber != None:
        print("PartNumber:" + objItem.PartNumber)
    if objItem.PositionInRow != None:
        print("PositionInRow:" + objItem.PositionInRow)
    if objItem.PoweredOn != None:
        print("PoweredOn:" + objItem.PoweredOn)
    if objItem.Removable != None:
        print("Removable:" + objItem.Removable)
    if objItem.Replaceable != None:
        print("Replaceable:" + objItem.Replaceable)
    if objItem.SerialNumber != None:
        print("SerialNumber:" + objItem.SerialNumber)
    if objItem.SKU != None:
        print("SKU:" + objItem.SKU)
    if objItem.Speed != None:
        print("Speed:%s" % objItem.Speed)
    if objItem.Status != None:
        print("Status:" + objItem.Status)
    if objItem.Tag != None:
        print("Tag:" + objItem.Tag)
    if objItem.TotalWidth != None:
        print("TotalWidth:%s" % objItem.TotalWidth)
    if objItem.TypeDetail != None:
        print("TypeDetail:%s" % objItem.TypeDetail)
    if objItem.Version != None:
        print("Version:" + objItem.Version)

    print("-"*10)
