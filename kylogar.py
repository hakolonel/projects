import keyboard
def write(event):
    button = event.name
    print(button,end="",flush=True)

keyboard.unhook_all
keyboard.on_release(callback=write)
keyboard.wait()