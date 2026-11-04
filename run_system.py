"""
Single-command launcher for Construction Safety System.
Starts both the FastAPI Backend and Vite React Frontend concurrently.
"""

import os
import sys
import time
import subprocess
import signal
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
BACKEND_DIR = ROOT_DIR / "backend"
FRONTEND_DIR = ROOT_DIR / "frontend"

def find_frontend_command():
    vite_js = FRONTEND_DIR / "node_modules" / "vite" / "bin" / "vite.js"
    if vite_js.exists():
        # Most reliable on Windows across Git Bash / CMD / PowerShell
        return ["node", str(vite_js)]
    
    # Fallback to direct npm path if available
    fixed_npm = r"C:\Program Files\nodejs\npm.cmd"
    if os.path.exists(fixed_npm):
        return [fixed_npm, "run", "dev"]
    
    return ["npm", "run", "dev"]

def main():
    print("=" * 65)
    print("  EDGE CONSTRUCTION SAFETY SYSTEM - UNIFIED LAUNCHER")
    print("  SIT Tumakuru Mini-Project (2026-27)")
    print("=" * 65)

    python_executable = sys.executable

    # Start FastAPI Backend
    print("\n[1/2] Starting FastAPI Edge Backend on http://localhost:8000...")
    backend_proc = subprocess.Popen(
        [python_executable, "main.py"],
        cwd=str(BACKEND_DIR),
        shell=(sys.platform == "win32")
    )

    # Start React Frontend using resilient direct node runner
    frontend_cmd = find_frontend_command()
    print(f"[2/2] Starting React Vite Frontend on http://localhost:5173...")
    frontend_proc = subprocess.Popen(
        frontend_cmd,
        cwd=str(FRONTEND_DIR),
        shell=(sys.platform == "win32" and frontend_cmd[0].endswith(".cmd"))
    )

    print("\n" + "=" * 65)
    print("  SYSTEM RUNNING SUCCESSFULLY!")
    print("  - Web Dashboard:     http://localhost:5173")
    print("  - Backend API:       http://localhost:8000")
    print("  - API Documentation: http://localhost:8000/docs")
    print("  Press Ctrl+C in this terminal to shut down both servers cleanly.")
    print("=" * 65 + "\n")

    def shutdown(signum=None, frame=None):
        print("\nStopping all system processes...")
        try:
            if sys.platform == "win32":
                subprocess.call(["taskkill", "/F", "/T", "/PID", str(backend_proc.pid)], stderr=subprocess.DEVNULL)
                subprocess.call(["taskkill", "/F", "/T", "/PID", str(frontend_proc.pid)], stderr=subprocess.DEVNULL)
            else:
                backend_proc.terminate()
                frontend_proc.terminate()
        except:
            pass
        print("Shutdown complete.")
        sys.exit(0)

    signal.signal(signal.SIGINT, shutdown)
    if hasattr(signal, "SIGTERM"):
        signal.signal(signal.SIGTERM, shutdown)

    try:
        while True:
            time.sleep(1)
            if backend_proc.poll() is not None:
                print("Backend process exited unexpectedly.")
                break
            if frontend_proc.poll() is not None:
                print("Frontend process exited unexpectedly.")
                break
    except KeyboardInterrupt:
        shutdown()

if __name__ == "__main__":
    main()
