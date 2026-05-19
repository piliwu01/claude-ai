Set objShell = CreateObject("WScript.Shell")
Set objFSO   = CreateObject("Scripting.FileSystemObject")

strDir  = objFSO.GetParentFolderName(WScript.ScriptFullName)
strPy   = strDir & "\omr_processor_gui.py"
strLog  = strDir & "\omr_log.txt"

' Check GUI script exists
If Not objFSO.FileExists(strPy) Then
    MsgBox "Cannot find omr_processor_gui.py" & vbCrLf & _
           "Put this .vbs in the same folder.", vbCritical, "OMR Tool"
    WScript.Quit
End If

' Find python.exe path via where command
Set objExec = objShell.Exec("cmd /c where python")
strPythonPath = ""
Do While Not objExec.StdOut.AtEndOfStream
    strLine = Trim(objExec.StdOut.ReadLine())
    If InStr(strLine, "python.exe") > 0 And strPythonPath = "" Then
        strPythonPath = strLine
    End If
Loop

If strPythonPath = "" Then
    MsgBox "Python not found." & vbCrLf & vbCrLf & _
           "Install from: https://www.python.org/downloads/" & vbCrLf & _
           "Check [Add Python to PATH] during install.", vbCritical, "OMR Tool"
    WScript.Quit
End If

' Build pythonw path (same folder as python.exe)
strPythonDir = objFSO.GetParentFolderName(strPythonPath)
strPythonW   = strPythonDir & "\pythonw.exe"

' Install required packages silently
objShell.Run "cmd /c pip install pandas openpyxl xlrd -q", 0, True

' Launch GUI - use pythonw if exists, else python
If objFSO.FileExists(strPythonW) Then
    objShell.Run """" & strPythonW & """ """ & strPy & """", 0, False
Else
    objShell.Run """" & strPythonPath & """ """ & strPy & """", 1, False
End If
