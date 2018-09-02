@echo off

cd C:\Program Files\Microsoft Office\Office15
cscript ospp.vbs /sethst:91.149.135.83
cscript ospp.vbs /act
cscript ospp.vbs /dstatus
cscript ospp.vbs /remhst

pause