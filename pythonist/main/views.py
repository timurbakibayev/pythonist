from shlex import split as splitsh
from django.shortcuts import render, HttpResponse
import subprocess
import time
import os
import re

def index(request):
    context = {"reply":"", "code":""}

    if request.method == "POST":
        prog = request.POST.get("program")
        t = re.search(r"import\s*os", prog)
        if t:
            prog = prog.replace(t.group(),"print('hehe')")
        context["code"] = prog
        text_file = open("test.py", "w")
        text_file.write(prog)
        text_file.close()
        # os.system()
        cmd = 'echo "2\n3" | python test.py'
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True,stderr=subprocess.PIPE)
        time.sleep(1)
        pstatus = proc.poll()
        if pstatus is None:
            proc.kill()
            context["reply"] = "Killed :("
        else:
            try:
                context["reply"] = proc.stdout.read().decode() + proc.stderr.read().decode()
            except Exception as e:
                context["reply"] = "Something is wrong<br>"+str(e)


    return render(request,"index.html",context=context)
