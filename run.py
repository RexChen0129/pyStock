import os
import subprocess
import sys

if __name__ == "__main__":
    # 自動執行 streamlit 指令啟動 app.py
    print("🚀 正在啟動股市分析網頁...")
    subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"])