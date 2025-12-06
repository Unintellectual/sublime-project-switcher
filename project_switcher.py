import sublime, sublime_plugin, os
from pathlib import Path

# Edit these to point at your project roots
PROJECT_ROOTS = ["~/programming/local", "~/programming/thirdparty"]
MAX_ENTRIES = 2000

def find_projects(roots):
    out = []
    for r in roots:
        root = os.path.expanduser(r)
        if not os.path.isdir(root):
            continue
        try:
            for name in os.listdir(root):
                p = os.path.join(root, name)
                if os.path.isdir(p):
                    out.append(p)
                    if len(out) >= MAX_ENTRIES:
                        return out
        except Exception:
            continue
    return sorted(out, key=lambda s: s.lower())

class ProjectSwitcherCommand(sublime_plugin.WindowCommand):
    def run(self):
        self.items = find_projects(PROJECT_ROOTS)
        if not self.items:
            sublime.message_dialog("No folders found in PROJECT_ROOTS.")
            return
        display = [p.replace(os.path.expanduser("~"), "~") for p in self.items]
        self.window.show_quick_panel(display, self.on_done, sublime.KEEP_OPEN_ON_FOCUS_LOST)

    def on_done(self, idx):
        if idx == -1:
            return
        path = self.items[idx]
        # replace folders in current window (no .sublime-project file needed)
        self.window.set_project_data({"folders": [{"path": path}]})
        # refresh sidebar if hidden
        if not self.window.is_sidebar_visible():
            self.window.run_command("toggle_side_bar")
            self.window.run_command("toggle_side_bar")
