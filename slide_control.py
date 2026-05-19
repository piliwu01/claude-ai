import warnings
warnings.filterwarnings("ignore")

import json
import sys
import os

STATE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "slide_state.json")


def read_state():
    with open(STATE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def write_state(state):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False)


def main():
    if not os.path.exists(STATE_FILE):
        print("錯誤：找不到 slide_state.json，請先啟動霹靂簡報控制器。")
        sys.exit(1)

    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"
    state = read_state()
    current = state.get("current", 1)
    total = state.get("total", 1)

    if cmd == "next":
        if current < total:
            state["current"] = current + 1
            write_state(state)
            print(f"已翻至第 {state['current']} 頁（共 {total} 頁）")
        else:
            print(f"已是最後一頁（第 {total} 頁）")

    elif cmd == "prev":
        if current > 1:
            state["current"] = current - 1
            write_state(state)
            print(f"已翻至第 {state['current']} 頁（共 {total} 頁）")
        else:
            print("已是第一頁，無法再後退。")

    elif cmd.startswith("goto:"):
        try:
            page = int(cmd.split(":")[1])
        except ValueError:
            print("錯誤：頁碼須為整數，例如 goto:5")
            sys.exit(1)
        if 1 <= page <= total:
            state["current"] = page
            write_state(state)
            print(f"已跳至第 {page} 頁（共 {total} 頁）")
        else:
            print(f"頁碼超出範圍（共 {total} 頁），請輸入 1 到 {total}。")

    elif cmd == "status":
        print(f"目前第 {current} 頁，共 {total} 頁。")

    else:
        print("用法：python slide_control.py next | prev | goto:N | status")


if __name__ == "__main__":
    main()
