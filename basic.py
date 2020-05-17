import os
import subprocess
import time

# Configuration messages
not_root = "Merci d'éxécuter ce script en tant que root"
already_running = "Le serveur est déjà en marche impossible de le démarrer"
impossibletostop = "Impossible d'arrêter le serveur."
forcestop = "Arrêt d'urgence du serveur"
launched = "est en marche."
stop = "Tentative d'arrêt"
# Configuration test ne pas toucher
user = "tranie"
minram = "2G"
maxram = "4G"
service = "paper.jar"
startupcommand = "java -Xms{} -Xmx{} -jar {} nogui"
screen_name = "test"
path = "/home/test/"


# Configuration fin


def gen_command(screen_name, path, service=service, minram=minram, maxram=maxram, startupcommand=startupcommand):
    startupcommand = startupcommand.format(minram, maxram, service)
    return f"cd {path} && screen -c /dev/null -dmS {screen_name} {startupcommand}"


def amiroot():
    whoami = subprocess.Popen("whoami", stdout=subprocess.PIPE).communicate()[0]
    if str(whoami)[2:-3] == user:
        return True
    else:
        return False


def is_running():
    return True


def mc_run(screen_name=screen_name, command="test"):
    os.system(f"screen -p 0 -S {screen_name} -X eval 'stuff \"{command}\"\015'")


def mc_save():
    if is_running():
        mc_run("save-off")
        mc_run("save-all")
        time.sleep(10)
        mc_run("save-on")
    else:
        print("Server not running")


def mc_kill():
    pass


def mc_alert():
    pass


def mc_start(screen_name=screen_name, path=path, service=service, minram=minram, maxram=maxram,
             startupcommand=startupcommand):
    if amiroot() and is_running() == False:
        os.system(gen_command(screen_name, path, service, minram, maxram, startupcommand))
    elif not amiroot():
        return not_root
    else:
        return already_running


def mc_stop(screen_name=screen_name):
    count = 0
    while is_running():
        try:
            mc_alert();
            mc_save();
            mc_run("stop")
        except:
            pass
        if count >= 10:
            print(f"{impossibletostop} {forcestop}")
            mc_kill()
            break
        elif count == 0:
            print(f" {screen_name} {launched} {stop}")
        count += 1


def mc_restart():
    pass


mc_stop()
