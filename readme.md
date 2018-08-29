
# 需求

基本功能

1. 能支持Windows/Linux/OSX
2. 採集網卡、硬體、主板等硬體信息
3. 以主板SN號作為唯一電腦，與資料庫比對，沒有就新增電腦編號，存在就更新。
    1. 獲取SN號
    2. request api post data
        1. if SN in list return hostname, else add this SN.
    3. reponse Hostname
4. 結合Zabbix API
5. 結合堡壘機

開發環境

Python 3.6

Module

platform


