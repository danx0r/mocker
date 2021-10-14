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
        print ("SKIP |", r)
        skip = False
        continue
    if r[:9] == "#PSEUDO: ":
        if r[9:] == 'SKIP':
            skip = True
            continue
        else:
            skip = False
            cmd = r[9:]
            print ("DO   |", cmd)
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
            print ("DO   |", cmd)
            do(cmd)
        elif key == "ENV":
            i = cmd.find('=')
            var = cmd[:i]
            val = cmd[i+1:]
            val = os.path.expandvars(val)
            print (f"SET  | {var}={val}")
            os.environ[var]=val
        else:
            print ("SKIP |", r)
f.close()
