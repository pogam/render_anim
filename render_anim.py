import numpy
import glob
import subprocess
import os
import shutil
import argparse
import getpass

def ensure_dir(f):
    d = os.path.dirname(f)
    if not os.path.exists(d):
        os.makedirs(d) 

parser = argparse.ArgumentParser(description='this is the driver of the GeorefIrCam Algo.')
parser.add_argument('-i','--input', help='Input directory with images',required=True)
parser.add_argument('-ext','--extension', help='images format',required=True)
parser.add_argument('-o','--output', help='Name of the output video',required=True)
parser.add_argument('-fr','--frameRate', help='frame rate of the input images',required=False)

args = parser.parse_args()

pwd = os.getcwd()

if args.extension is None:
    extension = 'png'
else:
    extension = args.extension

if args.frameRate is None:
    frameRate = 10
else:
    frameRate = args.frameRate

files = sorted(glob.glob(args.input+'/*.'+extension))
outVideo = args.output

#tmpdir
tmpdir = '/tmp/{:s}/renderAnim/'.format(getpass.getuser())


#clean tmp
if os.path.isdir(tmpdir):
    shutil.rmtree(tmpdir)
ensure_dir(tmpdir)

#convert file name to get number right
for ifile, file_ in enumerate(files): 
    shutil.copyfile(file_,tmpdir+'{:06d}.{:s}'.format(ifile,extension))

#double the last image to make sure it shows when the frame rate is low
shutil.copyfile(file_,tmpdir+'{:06d}.{:s}'.format(ifile+1,extension))

#call avconv
os.chdir(tmpdir)
subprocess.call(['ffmpeg', '-r','{:d}'.format(int(frameRate)), '-f', 'image2', 
    '-i', '%06d'+'.'+extension,'-r','20','-vb','20M', outVideo])

#move video file back
if os.path.isfile(pwd+'/'+outVideo):
    os.remove(pwd+'/'+outVideo)
shutil.move(tmpdir+outVideo,pwd)
os.chdir(pwd)

#clean
shutil.rmtree(tmpdir)

