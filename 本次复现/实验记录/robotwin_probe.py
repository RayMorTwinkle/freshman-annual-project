import sys, subprocess
def run(*cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    print("COMMAND", cmd, "EXIT", r.returncode)
    print((r.stdout + r.stderr)[-6500:])
    return r.returncode
run("nvidia-smi", "--query-gpu=name,memory.total,driver_version", "--format=csv,noheader")
run("git","-C","/content/robotwin","rev-parse","HEAD")
run(sys.executable, "-m", "pip", "install", "--no-deps", "sapien==3.0.0b1")
if not run("uv","venv","--python","3.10","/content/robotwin-probe"):
    py = "/content/robotwin-probe/bin/python"
    if not run("uv","pip","install","--python",py,"numpy==1.26.4","sapien==3.0.0b1"):
        run(py,"-c", 'import sapien; print(sapien.__file__,flush=True); s=sapien.Scene(); c=s.add_camera("probe",64,64,1.0,0.1,10); s.update_render(); c.take_picture(); print(c.get_picture("Color").shape)')
