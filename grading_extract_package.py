from pprint import pprint
import tarfile
import os
from shutil import copyfile, move, rmtree
import shutil
sd = '1solutions'
fn = 'pset-03-103_Curtis_17.tar.gz'
parent_folder = fn[:fn.find('-', fn.find('-')+1)]
def extract_tarball(fname):
    if (fname.endswith("tar.gz")):
        tar = tarfile.open(fname, "r:gz")
        tar.extractall()
        tar.close()
    elif (fname.endswith("tar")):
        tar = tarfile.open(fname, "r:")
        tar.extractall()
        tar.close()
        
def isdir(fn):
    if not(os.path.isdir(fn)):
        os.mkdir(fn)
        print("Creating Directory: {}".format(fn))
    else:
        print("Directory Exists: {}".format(fn))

def unpack_110(b):
    isdir(b)
    owd = os.getcwd()
    target_packages = list(filter(lambda x: b in x and 'tar' in x, os.listdir()))
    #pprint(target_packages)
    for package in target_packages:
        copyfile(package, os.path.join(b, package))
    
    os.chdir(b)
    for package in list(filter(lambda x: 'tar' in x, os.listdir())):
        extract_tarball(package)
        print('Package Extracted: {}'.format(package))
        os.remove(package)
    
    #print(os.listdir())
    temp_dirs = list(filter(lambda x: b in x and os.path.isdir(x), os.listdir()))
    #print(temp_dirs)
    for ps_dir in temp_dirs:
        files = os.listdir(ps_dir)
        files = list(filter(lambda x: x not in os.listdir(), files))
        for file in files:
            #if file in os.listdir():
            #print(file, os.getcwd())
            if os.path.isdir(os.path.join(ps_dir, file)):
                #print(file)
                move(os.path.join(ps_dir, file), os.path.join(owd, b))
            else:
                move(os.path.join(ps_dir, file), os.path.join(owd, b))
        rmtree(ps_dir)
        print('Removing Directory: {}'.format(ps_dir))
    
    
    solution_files = list(filter(lambda x: 'solutions' in x and '.rkt' in x, os.listdir()))

    isdir(sd)
    for sf in solution_files:
        if sf not in os.listdir(sd):
            move(os.path.join(sf), os.path.join(sd, sf))
        else:
            os.remove(os.path.join(sf))
    print('Moved Solution Files')
    

    
    print('Done Handling All Files\n')
    os.chdir(owd)
    #print(owd)

def package_zip(d):
    fn = 'graded-{}-Curtis-17'.format(d.split('-')[1])
    if '{}.zip'.format(fn) in os.listdir():
        os.remove('{}.zip'.format(fn))
    if sd in os.listdir(d):
        rmtree(os.path.join(d, sd))
        print('Removed: {}'.format(os.path.join(d, sd)))
    #print(fn)
    shutil.make_archive(fn, 'zip', d)  
    print("Packaged: {}".format('{}.zip'.format(fn)))
    
    
owd = os.getcwd()
try:
    unpack_110('pset-03')
except:
    os.chdir(owd)
    raise

package_zip('pset-03')

