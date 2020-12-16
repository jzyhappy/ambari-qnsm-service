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

from resource_management.libraries.functions.default import default
from resource_management import *

config = Script.get_config()

# cluster info
#mgm_host = config['clusterHostInfo']['mgm_hosts'][0]

# cluster conf
dpdk_env_cfg_template = config['configurations']['qnsm-config']['content']
s3_address_cfg_template = config['configurations']['s3-config']['content']

# qnsm
pid_file = "/var/run/qnsm.pid"

# path
config_path = "/var/lib/qnsm"
