# Copyright 2016 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
'''Creates sample IAP Server'''


def GenerateConfig(context):
  """Generate configuration."""
  
  resources=[]
  resources.append({
    'name': 'iap-server-instance-template',
    'type': 'compute.v1.instanceTemplate',
    'properties': {
      'properties': {
        'zone': context.properties['zone'],
        'machineType': 'n1-standard-1',
        'disks': [{
          'deviceName': 'boot',
          'type': 'PERSISTENT',
          'boot': True,
          'autoDelete': True,
          'initializeParams': {
            'sourceImage': 'projects/debian-cloud/global/images/family/debian-8'
          }
        }],
        'networkInterfaces': [{
          'network': 'global/networks/default',

          # Access Config required to give the instance a public IP address
          'accessConfigs': [{
            'name': 'External NAT',
            'type': 'ONE_TO_ONE_NAT',
          }],
        }],
        'metadata': { 
          'items':[{
            'key': 'startup-script',
            'value': 'wget https://github.com/GoogleCloudPlatform/python-docs-samples/raw/master/iap/validate_jwt.py? -O /home/validate_jwt.py;'
                     'wget https://github.com/GoogleCloudPlatform/professional-services/raw/master/infrastructure/identity-aware-proxy/iap_validating_server.py? -O /home/iap_validating_server.py;'
                     'wget https://raw.githubusercontent.com/GoogleCloudPlatform/python-docs-samples/master/iap/requirements.txt;'
                     'apt-get update;'
                     'apt-get install python-pip build-essential libssl-dev libffi-dev python-dev -y;'
                     'easy_install --upgrade pip;'
                     'pip install virtualenv;'
                     'virtualenv /home/virtualenv;'
                     '/home/virtualenv/bin/pip install -r requirements.txt;'
                     '/home/virtualenv/bin/python /home/iap_validating_server.py;'
          }]
        }
      }
    }
  })
  resources.append({
    'name': 'iap-server-instance-group',
    'type': 'compute.v1.instanceGroupManager',
    'properties': {
      'instanceTemplate': '$(ref.iap-server-instance-template.selfLink)',
      'baseInstanceName': 'iap-server-vm',
      'targetSize': 1,
      'zone': context.properties['zone'],
    }
  })
  return {'resources':resources}