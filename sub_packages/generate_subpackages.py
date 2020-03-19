import requests, os, shutil, importlib.util, fileinput
from io import BytesIO
from zipfile import ZipFile
from pprint import pprint
from setuptools import sandbox
from environs import Env
from tempfile import mkstemp
from shutil import move
from os import fdopen, remove
from doc_converter.spec import SPEC as doc_converter_spec
from ooxml_automation.spec import SPEC as ooxml_automation_spec
from story.spec import SPEC as story_spec

DELETE_TMP_FILES = True

env = Env()
env.read_env()

CODEGEN_ENDPOINT="https://openapi-generator.presalytics.io/api/gen/clients/python"
CODEGEN_DL_STUB="https://openapi-generator.presalytics.io/api/gen/download/"
CODEGEN_DIR=os.path.dirname(os.path.realpath(__file__))
TMP_PATH = os.path.join(CODEGEN_DIR, "tmp")
LIC_PATH = os.path.join(CODEGEN_DIR, "LICENSE")


CLIENT_SPECS = []
CLIENT_SPECS.append(doc_converter_spec)
CLIENT_SPECS.append(ooxml_automation_spec)
CLIENT_SPECS.append(story_spec)
GIT_SSH_COMMAND = 'ssh -i ~/.ssh/id_rsa'
os.environ['GIT_SSH_COMMAND'] = GIT_SSH_COMMAND

os.system("git config credential.helper presalytics-bot")

HEADER = {
    'Content-type': 'application/json',
    'Accept': 'application/json'
}


# from git import Repo

# PATH_OF_GIT_REPO = r'path\to\your\project\folder\.git'  # make sure .git folder is properly configured
# COMMIT_MESSAGE = 'comment from python script'



def increment_version(old_version, update_type):

    _major, _minor, _patch = old_version.split(".")
    if update_type == "major":
        _major = int(_major) + 1
        _minor = 0
        _patch = 0
    elif update_type == "minor":
        _minor = int(_minor) + 1
        _patch = 0
    else:
        _patch = int(_patch) + 1
    new_version = "{0}.{1}.{2}".format(_major, _minor, _patch)
    return new_version

def replace_ver(file_path, update_type):
    #Create temp file
    fh, abs_path = mkstemp()
    with fdopen(fh,'w') as new_file:
        with open(file_path) as old_file:
            for line in old_file:
                if line[:10] == "VERSION = ":
                    ver = line.replace("VERSION = ", '').replace('"','').replace('\n','')
                    new_ver = increment_version(ver, update_type)
                    new_file.write('VERSION = "{0}"\n'.format(new_ver))
                else:
                    new_file.write(line)

    #Remove original file
    remove(file_path)
    #Move new file
    move(abs_path, file_path)
    return new_ver


def update_imports(tmp_dir_path, package_name):
    new_import_path = "presalytics.client.{}".format(package_name)
    find1 = "from {}".format(package_name)
    replace1 = "from {}".format(new_import_path)
    find2 = "import {}".format(package_name)
    replace2 = "import {}".format(new_import_path)
    find3 = "klass = getattr({}.models, klass)".format(package_name)
    replace3 = "klass = getattr({}.models, klass)".format(new_import_path)
    find4 = 'logging.getLogger(\"{}'.format(package_name)
    replace4 = 'logging.getLogger(\"{}'.format(new_import_path)

    for dname, dirs, files in os.walk(tmp_dir_path):
        for fname in files:
            fpath = os.path.join(dname, fname)
            with open(fpath) as f:
                s = f.read()
            s = s.replace(find1, replace1)
            s = s.replace(find2, replace2)
            s = s.replace(find3, replace3)
            s = s.replace(find4, replace4)
            with open(fpath, "w") as f:
                f.write(s)

for spec in CLIENT_SPECS:
    try:
        if spec["update"] is True:
            #new_ver = replace_ver(spec["setuppy_path"], spec["update_type"])
            payload = {
                'openAPIUrl': spec['endpoint'],
                'options' : {
                    'packageName': spec['package_name'],
                    'projectName': 'Presalytics API'
                    # 'packageVersion': new_ver
                }
            }

            print("Sending {} api spec to code generator".format(spec['package_name']))
            response = requests.post(CODEGEN_ENDPOINT, json=payload, headers=HEADER)
            print("Response from openapi generator:")
            pprint(response)
            uid = response.json()['code']
            link = CODEGEN_DL_STUB + uid

            print("Downloading generated code for {} ".format(spec['package_name']))
            file_response = requests.get(link)

            zipfile = ZipFile(BytesIO(file_response.content))
            zipfile.extractall(TMP_PATH)
            update_imports(TMP_PATH, spec["package_name"])
            source_dir = os.path.join(os.path.dirname(__file__), "tmp", "python-client", spec["package_name"])
            root = os.path.dirname(os.path.dirname(__file__))
            target_dir = os.path.join(root, "presalytics", "client", spec["package_name"])
            try:
                shutil.rmtree(target_dir)
            except Exception:
                pass
            shutil.copytree(source_dir, target_dir)
            print("Subpackage {0} successfull updated in {1}".format(spec["package_name"], target_dir))
    except Exception:
        print("Sub package generation unsuccessful.  Please debug and retry")
    finally:
        if DELETE_TMP_FILES:
            try:
                shutil.rmtree(TMP_PATH)
            except Exception:
                pass

    # repo = git.get_repo("presalytics/" + spec['package_name'])

#Clean temp files
