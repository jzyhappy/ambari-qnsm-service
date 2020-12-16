# ambari-qnsm-service
ambari-qnsm-service是将QNSM放在ambari上进行管理
QNSM(IQIYI Network Security Monitor) 是一个旁路部署的全流量，实时，高性能网络安全监控引擎，基于DPDK开发，集成了DDOS检测和IDPS模块。
QNSM参考https://github.com/iqiyi/qnsm

# 安装
## 下载
```powershell
VERSION=`hdp-select status hadoop-client | sed 's/hadoop-client - \([0-9]\.[0-9]\).*/\1/'`
sudo git clone https://github.com/jzyhappy/ambari-qnsm-service.git  /var/lib/ambari-server/resources/stacks/HDP/$VERSION/services/FLINK 
```
## 重新启动Ambari
```powershell
ambari-server restart
```

# 注意
安装qnsm本程序没有，因为我们是在源QNSM上记性了修改，并放到自己搭建的yum源上，所以目前ambari-qnsm-service只有启动，停止，重启，监控QNSM，没有安装，如需安装请自行修改
./package/scripts/qnsm.py 中install部分，可参考https://github.com/iqiyi/qnsm 和本人项目下其他ambari-*-service项目
