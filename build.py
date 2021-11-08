import sys, os

def do(cmd):
    if len(sys.argv) > 1 and sys.argv[1] == '--dry':
        return
    os.system(cmd)

fn = "Dockerfile"
f =  open(fn)
skip = False
for r in f.readlines():
    r = r.strip()
    if skip:
        print ("MOCKER SKIP |", r)
        skip = False
        continue
    if r[:9] == "#MOCKER: ":
        if r[9:] == 'SKIP':
            skip = True
            continue
        else:
            skip = False
            cmd = r[9:]
            print ("MOCKER DO   |", cmd)
            if cmd [:3] == 'cd ':
                os.chdir(cmd[3:])
            else:
                do(cmd)
    skip = False
    if r and r[0] != '#':
        key = r.split()[0]
        cmd = r[len(key):].strip()
        if cmd[:3] == 'apt':
           cmd = f"sudo bash -c '{cmd}'"
        if key == 'RUN':
            print ("MOCKER DO   |", cmd)
            do(cmd)
        elif key == "ENV":
            i = cmd.find('=')
            var = cmd[:i]
            val = cmd[i+1:]
            val = os.path.expandvars(val)
            print (f"MOCKER SET  | {var}={val}")
            os.environ[var]=val
        elif key == 'WORKDIR':
            print("MOCKER cd   |", cmd)
            os.chdir(cmd)
        else:
            print ("MOCKER SKIP |", r)
f.close()

