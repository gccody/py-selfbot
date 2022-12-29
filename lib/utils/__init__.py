import subprocess


def behind():
    cmd1 = ["git", "remote", "update"]
    cmd2 = ["git", "status", "-uno"]
    subprocess.run(cmd1)
    res = subprocess.run(cmd2, stdout=subprocess.PIPE)

    return "Your branch is behind" in res.stdout.decode('utf-8')
