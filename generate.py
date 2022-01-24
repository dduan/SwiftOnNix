import os
import subprocess
import sys
import os.path
import shutil
import json
import re
from string import Template

call = subprocess.check_call

# Start clean
if os.path.isdir('./tmp'):
    shutil.rmtree('./tmp')
os.mkdir('./tmp')

# first argumnet is the full Swift version
full_version = sys.argv[1]

os.chdir("./tmp")

swift_src = f"swift-{full_version}-RELEASE"
swift_src_archive = f"{swift_src}.tar.gz"

# Download apple/swift by its version
call(["wget", f"https://github.com/apple/swift/archive/refs/tags/{swift_src_archive}"])

# Unpack
call(["tar", "xzvf", swift_src_archive])

# This is the source of the information
checkout_json_path = os.path.join(f"swift-{swift_src}", 'utils', 'update_checkout', 'update-checkout-config.json')
checkout_info = json.loads(open(checkout_json_path).read())

# in the JSON, keys only use major.minor versions.
rough_version = '.'.join(full_version.split('.')[:-1])

# find all the variables we defined in the template
template = open('../default.template.nix').read()
version_variables = re.findall(r'\$([a-z-]+)_version', template)
sha_variables = re.findall(r'\$([a-z-]+)_sha', template)

repos = checkout_info["repos"]
versions = checkout_info['branch-schemes'][f"release/{rough_version}"]["repos"]

fill_ins = {}

for project in version_variables:
    fill_ins[f"{project}_version"] = versions[project]

for project in sha_variables:
    project_repo = repos[project]["remote"]["id"]
    tarball_url = f"https://github.com/{project_repo}/archive/{versions[project]}.tar.gz"
    output = subprocess.check_output(['nix-prefetch-url', '--unpack', tarball_url])
    fill_ins[f"{project}_sha"] = output.decode('utf-8').rstrip()



result = template
fill_ins['swift_version'] = full_version
for key in fill_ins:
    result = result.replace(f"${key}", fill_ins[key])

output = open(sys.argv[2], 'w')
output.write(result)
