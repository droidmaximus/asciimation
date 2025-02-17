import PyInstaller.__main__

PyInstaller.__main__.run([
    '--name=asciimation',   # Name of the executable
    '--onefile',        # Bundle everything into a single file
    '--console',        # Opens in a console window (omit for GUI apps)
    'main.py',          # Your main script file
])
