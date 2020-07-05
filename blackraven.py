import re
import sys
import signal
import subprocess
import os
import glob
import hashlib
from time import sleep

decoy_name = "decoy.bin"
kill = True


def generate_decoy(file_name, size):
    print("[+]Generating decoy")
    with open(file_name, "w") as decoy:
        decoy.write("A"*size)
    return os.path.abspath(file_name)


def deploy_decoy(decoy_path, path):
    for filename in glob.glob(path + '/**/*', recursive=True):
        if os.path.isdir(filename):
            target = os.path.join(
                filename, ".007-decoy-{}.{}".format("finance", "docx"))
            if not os.path.islink(target):
                os.symlink(decoy_path, target)


def configure_auditd_rule(decoy_path):
    # Check if rule present
    print("[+]Checking auditd rule")
    cmd = "auditctl -l"
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    res = p.stdout.read().decode()
    if decoy_path not in res:
        print("[+]Adding auditd rule to track decoy")
        cmd = "auditctl -a exit,always -F path={} -F perm=rwa".format(
            decoy_path)
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)


def monitor_file_auditd(decoy_name):
    print("[+]And so my watch begins!")
    decoy_triggered = list()
    while True:
        try:
            sleep(0.5)
            cmd = "aureport -f"
            p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
            result = p.stdout.read().decode().split(
                "===============================================")[-1].strip()
            if "<no events of interest were found>" in result:
                continue
            for event in result.split("\n"):
                if event not in decoy_triggered:
                    decoy_triggered.append(event)
                else:
                    continue

                event_id = event.split(" ")[-1]
                cmd = "ausearch -i -a {}".format(event_id)
                p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
                event_details = p.stdout.read().decode()
                event_data = event_details.split("\n")
                proctitle = re.search(
                    r"proctitle\=(?P<proctitle>.*)$", event_data[1]).group("proctitle")
                if sys.argv[0] in proctitle:
                    continue
                try:
                    m = re.search(
                        r"pid\=(?P<pid>[0-9]+)\s.*\sexe\=(?P<exe>\S+)\s", event_data[-2])
                    pid = m.group("pid")
                    exe = m.group("exe")
                except AttributeError:
                    continue
                print(
                    "[+]Detected potential ransmware process {} with pid:{}".format(exe, pid))
                if kill:
                    print("[+]Killing it!")
                    try:
                        os.kill(int(pid), signal.SIGKILL)
                    except ProcessLookupError:
                        print("[+]Already dead!")
        except KeyboardInterrupt:
            print("\n[+]My watch has ended!")
            break


if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("[+]You need to provide path!")
        exit()

    paths = sys.argv[1]

    decoy_path = generate_decoy(decoy_name, 1024*1024*1)

    for path in paths.split(","):
        deploy_decoy(decoy_path, path)

    configure_auditd_rule(decoy_path)
    monitor_file_auditd(decoy_name)
