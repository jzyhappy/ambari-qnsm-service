"""
Licensed to the Apache Software Foundation (ASF) under one
or more contributor license agreements.  See the NOTICE file
distributed with this work for additional information
regarding copyright ownership.  The ASF licenses this file
to you under the Apache License, Version 2.0 (the
"License"); you may not use this file except in compliance
with the License.  You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

"""

from resource_management import *
from resource_management.core.exceptions import ComponentIsNotRunning
from resource_management.core.logger import Logger
import subprocess
import datetime

class Management(Script):

    def install(self, env):
        Logger.info("install qnsm")
        import params
        env.set_params(params)
        #remove_mysql_lib_cmd = "rpm -e --nodeps mysql-libs-5.7.27-el7-x86_64 >/dev/null 2>&1"
        #Execute(remove_mysql_lib_cmd,
        #        user='root'
        #        )
        #install_server_cmd = "yum -y install mysql-cluster-gpl-7.6.13-linux-glibc2.12-x86_64"
        #Execute(install_server_cmd,
        #        user='root'
        #        )
		
		 # create config dir
        Directory(params.config_path,
                  owner='root',
                  group='root'
                  )
        # create cluster config
        Logger.info('create dpdk_env.cfg in /var/lib/qnsm')
        File(format("{config_path}/dpdk_env.cfg"),
             owner = 'root',
             group = 'root',
             mode = 0644,
             content=InlineTemplate(params.dpdk_env_cfg_template)
             )
		File(format("{config_path}/s3_address.cfg"),
             owner = 'root',
             group = 'root',
             mode = 0644,
             content=InlineTemplate(params.s3_address_cfg_template)
             )
        # create pid file
        pid_cmd = "pgrep -o -f ^./qnsm-inspect* > {0}".format(params.pid_file)
        Execute(pid_cmd,
                logoutput=True)


    def configure(self, env):
        Logger.info("config qnsm node")
        import params
        env.set_params(params)
        File(format("{config_path}/dpdk_env.cfg"),
             owner = 'root',
             group = 'root',
             mode = 0644,
             content=InlineTemplate(params.dpdk_env_cfg_template)
             )
		File(format("{config_path}/s3_address.cfg"),
             owner = 'root',
             group = 'root',
             mode = 0644,
             content=InlineTemplate(params.s3_address_cfg_template)
             )


    def start(self, env):
        Logger.info("start qnsm")
        import params
        env.set_params(params)
        self.configure(env)
	Execute('cd /home/qnsm/qnsm_20200318 && ./start.py p1p2 >/home/qnsm/debug 2>&1 &', user="root", logoutput=True)
        #Execute('cd /home/qnsm/qnsm_20200318 && export RTE_SDK="/home/qnsm/qnsm_20200318" && export RTE_TARGET="/home/qnsm/qnsm_20200318/x86_64-native-linuxapp-gcc" && python ./setup_dpdk_env.py ./dpdk_env.cfg >/home/qnsm/debug 2>&1')
  	#Execute('export LD_LIBRARY_PATH=/home/qnsm/qnsm_20200318/qnsm_lib/:$LD_LIBRARY_PATH && cd /home/qnsm/qnsm_20200318 && ./qnsm-inspect -f ./qnsm_inspect.cfg.100 -c . -p 1 >/home/qnsm/debug 2>&1')
	#>/var/log/qnsm.log 2>&1
        pid_cmd = "pgrep -o -f ^/home/qnsm/qnsm_20200318/qnsm-inspect* > {0}".format(params.pid_file)
        Execute(pid_cmd, user="root", logoutput=True)


    def stop(self, env):
        Logger.info("stop qnsm")
        import params
        env.set_params(params)
	#pid = "cat {0}".format(params.pid_file)
	stop_cmd = "cat {0} | xargs kill -9".format(params.pid_file)
        Execute(stop_cmd, logoutput = True)
        File(params.pid_file, action = 'delete')


    def status(self, env):
        import os
        import params
        env.set_params(params)
        #check_process_status(params.pid_file)
        if os.path.isfile(params.pid_file):
            self.monitor(env)
	check_process_status(params.pid_file)

    def monitor(self, env):
        import params
        env.set_params(params)
        res = subprocess.Popen("ps -ef | grep qnsm-inspect",stdout=subprocess.PIPE,shell=True)
        qnsm=res.stdout.readlines()
        counts=len(qnsm)
        if counts<4:
            dt=datetime.datetime.now()
            fp=open('/home/qnsm/debug','a')
            fp.write('qnsm-inspect stop at %s\n' % dt.strftime('%Y-%m-%d %H:%M:%S'))
            fp.close()
            Execute('cd /home/qnsm/qnsm_20200318 && ./start.py p1p2 >/home/qnsm/debug 2>&1 &', logoutput=True)
            pid_cmd = "pgrep -o -f ^/home/qnsm/qnsm_20200318/qnsm-inspect* > {0}".format(params.pid_file)
            Execute(pid_cmd, logoutput=True)


    def uninstall(self, env):
        Logger.info("uninstall mgm node")

if __name__ == "__main__":
    Management().execute()
