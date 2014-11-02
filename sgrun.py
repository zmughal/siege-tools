#!/usr/bin/env python2
import os
import sys
import subprocess
exes = []
cwd = "."
plugins = []
p = os.path.abspath(".")
foldername = ""

def run():
    args = sys.argv[1:]
    if not args:
        args = []

    r = 1
    
    try:
        if "-l" in args:
            print os.path.join(cwd,exes[0])
            return 0
        elif "-d" in args:
            print os.path.dirname(cwd)
            return 0
        else:
            r = subprocess.call(['./'+exes[0]] + args, cwd=(cwd))
    except:
        pass
    
    return r

def advanced():
    global exes

    # test plugin "package.json"
    try:
        import json
        with open("package.json") as f:
            j = json.load(f)
            exe = j["main"] + ".js"
            if os.path.isfile(exe):
                exes = [exe]
                return run()
    except:
        pass

    # too many exes? use the one that matches outer project folder name
    try:
        if len(exes) > 1 and foldername:
            for exe in exes:
                if os.path.basename(exe) == foldername:
                    exes = [foldername]
                    return run()
    except:
        pass
    
    return 1
    
class Break(Exception): pass

p = os.path.abspath(".")
try:
    while True:
        try:
            cwd = os.path.join(p, "bin")
            for f in os.listdir(cwd):
                fn = os.path.join(p, "bin/%s" % f)
                if not os.path.isdir(fn) and not "." in f and os.access(fn, os.X_OK):
                    exes += [f]
                    foldername = os.path.basename(os.getcwd())
            if exes:
                raise Break
        except OSError:
            pass

        try:
            cwd = p
            for f in os.listdir(p):
                fn = f
                if not os.path.isdir(fn) and not "." in f and os.access(fn, os.X_OK):
                    exes += [f]
                    fnp = os.path.basename(os.getcwd())
                    if fnp == "bin":
                        fnp = os.path.basename(os.path.abspath(os.path.join(os.getcwd(), "..")))
                    foldername = os.path.join(os.path.basename(fnp))
            if exes:
                raise Break
        except OSError:
            pass
        
        p = os.path.abspath(os.path.join(p, ".."))
        if p == "/":
            break
except Break:
    pass

# attempt to remove test executables that might be present in the current dir
if len(exes) > 1:
    exes_old = exes
    exes = [e for e in exes_old if "test" not in e.lower()]
    if len(exes) == 0:
        exes = exes_old # get the right error message

if len(exes) == 1:
    exit(run())
    #os.system(exes[0])
elif len(exes) > 1:
    r = advanced()
    if r != 0:
        print >> sys.stderr, "Too many executables"
else:
    r = advanced()
    if r != 0:
        print >> sys.stderr, "No executables"

