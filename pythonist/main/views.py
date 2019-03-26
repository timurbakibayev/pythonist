from shlex import split as splitsh
from django.shortcuts import render, HttpResponse
import subprocess
import time
import os
import re

possible_errors = [
    {"error": "is not defined", "comment": "Вы использовали переменную, для которой не задали никаких значений. Например, вы могли написать print(a+b), но не объявили a или b."},
    {"error": "unsupported operand type(s)", "comment": "Вы пытаетесь сложить несовместимые типы данных. Например, одна из переменных строковая, а другая - числовая. Необходимо привести обе переменные к одному типу."},
]

possible_results = [
    {"result": "23", "comment": "Вы сложили два числа как строки. Необходимо преобразовать их в числа. Для этого воспользуйтесь фукнцией int(). Например, a = int(a)."},
    {"result": "5", "comment": "Вы всё сделали правильно! Поздравляю!"},
]

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
            context["reply"] = "Ваша программа зависла. Мы не стали ждать и прервали её. Простите."
        else:
            try:
                comments = ""
                errors = proc.stderr.read().decode()
                result = proc.stdout.read().decode()

                for p_e in possible_errors:
                    if p_e["error"] in errors:
                        comments = p_e["comment"]

                for p_e in possible_results:
                    if p_e["result"].strip() == result.strip():
                        comments = p_e["comment"]

                if "input(" not in prog:
                    comments = "Для начала рекомендуем считать эти два числа с помощью фукнции input. Например, a=input()."

                if len(errors.strip()) + len(comments) == 0:
                    comments = "Вроде бы программа отработала без ошибок. Но результат неверный."

                context["reply"] = result + errors + "\n\n" + comments
            except Exception as e:
                context["reply"] = "Ошибка вышла, вот о чем молчит наука: "+str(e)


    return render(request,"index.html",context=context)
