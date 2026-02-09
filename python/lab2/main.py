import sys
import os

class Editor:
    def __init__(self, path):
        self.path = path
        self.content = []
        self.history = []
        self.copy_buffer = ""
        self.is_changed = False

        if os.path.exists(path):
            with open(path, 'r', encoding="utf-8") as file:
                self.content = [line.rstrip('\n') for line in file.readlines()]

    def _save_history(self):
        self.history.append(list(self.content))
        self.is_changed = True

    def insert(self, text, row=None, col=None):
        self._save_history()
        if row is None:
            self.content.append(text)
            return

        idx_row = row - 1
        while len(self.content) <= idx_row:
            self.content.append("")

        line = self.content[idx_row]
        if col is None:
            self.content[idx_row] = line + text
        else:
            idx_col = col - 1
            self.content[idx_row] = line[:idx_col] + text + line[idx_col:]

    def delete_all(self):
        self._save_history()
        self.content = []

    def del_row(self, row):
        idx_row = row - 1
        if 0 <= idx_row < len(self.content):
            self._save_history()
            self.content.pop(idx_row)
        else:
            print(f"Ошибка: Строки {row} не существует.")

    def del_col(self, col):
        self._save_history()
        idx_col = col - 1
        for i in range(len(self.content)):
            line = self.content[i]
            if 0 <= idx_col < len(line):
                self.content[i] = line[:idx_col] + line[idx_col+1:]

    def swap(self, r1, r2):
        idx1, idx2 = r1 - 1, r2 - 1
        if 0 <= idx1 < len(self.content) and 0 <= idx2 < len(self.content):
            self._save_history()
            self.content[idx1], self.content[idx2] = self.content[idx2], self.content[idx1]
        else:
            print("Ошибка: Указанные строки вне диапазона.")

    def undo(self, count=1):
        for _ in range(count):
            if self.history:
                self.content = self.history.pop()
            else:
                break

    def copy(self, row, start=None, end=None):
        idx_row = row - 1
        if 0 <= idx_row < len(self.content):
            line = self.content[idx_row]
            s = (start - 1) if start is not None else 0
            e = end if end is not None else len(line)
            self.copy_buffer = line[s:e]
        else:
            print("Ошибка: Строка не найдена.")

    def paste(self, row):
        self._save_history()
        idx_row = row - 1
        while len(self.content) <= idx_row:
            self.content.append("")
        self.content[idx_row] += self.copy_buffer

    def show(self):
        for i, line in enumerate(self.content):
            print(f"{i+1}: {line}")

    def save(self):
        with open(self.path, 'w', encoding="utf-8") as file:
            file.write('\n'.join(self.content))
        self.is_changed = False

def manual_parse(user_input):
    res = []
    current = []
    in_quotes = False
    for char in user_input:
        if char == '"':
            in_quotes = not in_quotes
        elif char == ' ' and not in_quotes:
            if current:
                res.append("".join(current))
                current = []
        else:
            current.append(char)
    if current:
        res.append("".join(current))
    return res

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Укажите путь к файлу.")
        sys.exit()

    editor = Editor(sys.argv[1])

    while True:
        try:
            raw = input(">>> ").strip()
            if not raw: continue
            
            parts = manual_parse(raw)
            cmd = parts[0].lower()
            args = parts[1:]

            if cmd == "exit":
                if editor.is_changed:
                    if input("Сохранить (y/n)? ").lower() == 'y': editor.save()
                break
            elif cmd == "show":
                editor.show()
            elif cmd == "save":
                editor.save()
            elif cmd == "insert":
                txt = args[0]
                r = int(args[1]) if len(args) > 1 else None
                c = int(args[2]) if len(args) > 2 else None
                editor.insert(txt, r, c)
            elif cmd == "del":
                editor.delete_all()
            elif cmd == "delrow":
                if not args: print("Ошибка: укажите номер.")
                else: editor.del_row(int(args[0]))
            elif cmd == "delcol":
                if not args: print("Ошибка: укажите номер.")
                else: editor.del_col(int(args[0]))
            elif cmd == "swap":
                editor.swap(int(args[0]), int(args[1]))
            elif cmd == "undo":
                count = int(args[0]) if args else 1
                editor.undo(count)
            elif cmd == "copy":
                r = int(args[0])
                s = int(args[1]) if len(args) > 1 else None
                e = int(args[2]) if len(args) > 2 else None
                editor.copy(r, s, e)
            elif cmd == "paste":
                editor.paste(int(args[0]))
        except Exception as e:
            print(f"Ошибка ввода: {e}")
