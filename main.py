import urwid
import os
import json
import subprocess
import sys

subprocess.STDOUT = sys.stdout
checkboxes = []
filenames = [name for name in os.listdir("lists/") if name.endswith(".json")]

def execute(*args):
    try:
        output = subprocess.check_output(args, shell=True)
        result = [0, output]
    except subprocess.CalledProcessError as e:
        result = [int(e.returncode), e.output]
    return result

for filename in filenames:
    json_contents = json.load(open(os.path.join("lists/", filename)))
    name = json_contents["name"]
    description = json_contents["description"]
    checkbox = urwid.CheckBox(name+" - "+description)
    checkbox.filename = filename
    checkboxes.append(checkbox)

def make_list(*args):
    raise urwid.ExitMainLoop()

body = [urwid.Text("Choose packages:"), urwid.Divider()]
for checkbox in checkboxes:
    body.append(checkbox)
exit_button = urwid.Button("Done")
urwid.connect_signal(exit_button, 'click', make_list)
body.append(urwid.Divider())
body.append(exit_button)

listbox = urwid.ListBox(urwid.SimpleListWalker(body))

overlay = urwid.Overlay(listbox, urwid.SolidFill('\N{BLUE}'), align='center', width=('relative', 70), valign="middle", height=('relative', 90), min_width=80, min_height=10)
loop = urwid.MainLoop(overlay).run()

filenames = [checkbox.filename for checkbox in checkboxes if checkbox.state == True]

packages = []
pre_install_triggers = []
post_install_triggers = []

for filename in filenames:
    json_contents = json.load(open(os.path.join("lists/", filename)))
    packages += json_contents["packages"]
    pre_install_triggers += json_contents["pre-install"]
    post_install_triggers += json_contents["post-install"]

script_name = 'install_packages.sh'

print pre_install_triggers
print post_install_triggers

f = open(script_name, 'w')
f.write("apt-get update&&apt-get install -y ")
f.write(" ".join(packages))
st = os.stat(script_name)
os.chmod(script_name, st.st_mode | 64)
f.close()
print execute("./"+script_name)
for trigger in pre_install_triggers:
    print execute(trigger)
for trigger in post_install_triggers:
    print execute(trigger)
