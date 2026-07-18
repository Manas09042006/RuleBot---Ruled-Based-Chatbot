import customtkinter as ctk
from tkinter import END
from datetime import datetime

from chatbot import ChatBot


THEMES = {
    "dark": {
        "bg": "#0B1220",
        "sidebar": "#0E1628",
        "sidebar_hover": "#1A2740",
        "header": "#121C30",
        "chat_bg": "#111A2C",
        "bubble_bot": "#1A2740",
        "accent": "#14B8A6",
        "accent_hover": "#2DD4BF",
        "accent_dim": "#0D9488",
        "text": "#E2E8F0",
        "text_muted": "#94A3B8",
        "text_soft": "#64748B",
        "border": "#1E2D45",
        "danger": "#F87171",
        "danger_hover": "#EF4444",
        "danger_bg": "#3F1D1D",
        "success": "#34D399",
        "input_bg": "#162033",
        "panel": "#152036",
        "nav_active": "#134E4A",
        "user_name": "#5EEAD4",
        "user_msg": "#CCFBF1",
        "send_text": "#042F2E",
        "chat_textbox_bg": "#111A2C",
    },
    "light": {
        "bg": "#E8EEF5",
        "sidebar": "#FFFFFF",
        "sidebar_hover": "#DCE7F2",
        "header": "#FFFFFF",
        "chat_bg": "#F7FAFC",
        "bubble_bot": "#E8F0F7",
        "accent": "#0D9488",
        "accent_hover": "#14B8A6",
        "accent_dim": "#0F766E",
        "text": "#0F172A",
        "text_muted": "#475569",
        "text_soft": "#64748B",
        "border": "#CBD5E1",
        "danger": "#DC2626",
        "danger_hover": "#EF4444",
        "danger_bg": "#FEE2E2",
        "success": "#059669",
        "input_bg": "#FFFFFF",
        "panel": "#FFFFFF",
        "nav_active": "#CCFBF1",
        "user_name": "#0F766E",
        "user_msg": "#134E4A",
        "send_text": "#FFFFFF",
        "chat_textbox_bg": "#F7FAFC",
    },
}

FAQS = [
    ("What is Python?", "what is python"),
    ("Python features", "python features"),
    ("What is OOP?", "what is oop"),
    ("Four pillars of OOP", "four pillars of oop"),
    ("What is Tkinter?", "what is tkinter"),
    ("What is Regex?", "what is regex"),
    ("What is a chatbot?", "what is chatbot"),
    ("What is AI?", "what is ai"),
    ("What is SQL?", "what is sql"),
    ("What is JavaScript?", "what is javascript"),
]


class ChatGUI:

    def __init__(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        self.bot = ChatBot()
        self.chat_history = []
        self.sessions = []
        self.active_nav = None
        self._overlay = None
        self._overlay_builder = None
        self._overlay_title = ""
        self._overlay_subtitle = ""
        self._typing = False
        self.theme_choice = "Dark"
        self.font_size = 14
        self.colors = dict(THEMES["dark"])
        self._theme_updating = False

        self.window = ctk.CTk()
        self.window.title("RuleBot — Intelligent Rule-Based Assistant")
        self.window.geometry("1180x740")
        self.window.minsize(980, 620)
        self.window.configure(fg_color=self.colors["bg"])

        self.window.grid_columnconfigure(0, weight=0)
        self.window.grid_columnconfigure(1, weight=1)
        self.window.grid_rowconfigure(1, weight=1)

        self.create_sidebar()
        self.create_header()
        self.create_main_area()
        self.create_chat_area()
        self.create_bottom_bar()
        self.create_status_bar()
        self._greet()

    # ------------------------------------------------------------------ UI
    def create_sidebar(self):
        c = self.colors
        self.sidebar = ctk.CTkFrame(
            self.window,
            width=248,
            fg_color=c["sidebar"],
            corner_radius=0,
            border_width=0,
        )
        self.sidebar.grid(row=0, column=0, rowspan=4, sticky="ns")
        self.sidebar.grid_propagate(False)

        brand = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        brand.pack(fill="x", padx=20, pady=(28, 8))

        self.brand_title = ctk.CTkLabel(
            brand,
            text="RuleBot",
            font=ctk.CTkFont(family="Segoe UI Semibold", size=26, weight="bold"),
            text_color=c["accent"],
            anchor="w",
        )
        self.brand_title.pack(anchor="w")

        self.brand_sub = ctk.CTkLabel(
            brand,
            text="Rule-Based Assistant",
            font=ctk.CTkFont(family="Segoe UI", size=12),
            text_color=c["text_soft"],
            anchor="w",
        )
        self.brand_sub.pack(anchor="w", pady=(2, 0))

        self.sidebar_divider = ctk.CTkFrame(
            self.sidebar, height=2, fg_color=c["accent_dim"], corner_radius=1
        )
        self.sidebar_divider.pack(fill="x", padx=20, pady=(16, 20))

        nav_items = [
            ("new", "New Chat", self.on_new_chat),
            ("history", "History", self.on_history),
            ("faqs", "FAQs", self.on_faqs),
            ("settings", "Settings", self.on_settings),
            ("about", "About", self.on_about),
        ]

        self.nav_buttons = {}
        for key, label, cmd in nav_items:
            btn = ctk.CTkButton(
                self.sidebar,
                text=f"  {label}",
                width=208,
                height=44,
                corner_radius=12,
                font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
                fg_color="transparent",
                hover_color=c["sidebar_hover"],
                text_color=c["text"],
                anchor="w",
                command=cmd,
            )
            btn.pack(padx=20, pady=5)
            self.nav_buttons[key] = btn
            self._bind_nav_hover(btn, key)

        ctk.CTkFrame(self.sidebar, fg_color="transparent").pack(expand=True)

        foot = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        foot.pack(fill="x", padx=20, pady=(0, 24))

        self.sidebar_foot = ctk.CTkLabel(
            foot,
            text="v1.0  ·  Offline Mode",
            font=ctk.CTkFont(family="Segoe UI", size=11),
            text_color=c["text_soft"],
        )
        self.sidebar_foot.pack(anchor="w")

    def _bind_nav_hover(self, btn, key):
        def on_enter(_e):
            if self.active_nav != key:
                btn.configure(fg_color=self.colors["sidebar_hover"])

        def on_leave(_e):
            if self.active_nav != key:
                btn.configure(fg_color="transparent")
            else:
                btn.configure(fg_color=self.colors["nav_active"])

        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)

    def _set_active_nav(self, key):
        self.active_nav = key
        c = self.colors
        for k, btn in self.nav_buttons.items():
            if k == key:
                btn.configure(fg_color=c["nav_active"], text_color=c["accent"])
            else:
                btn.configure(fg_color="transparent", text_color=c["text"])

    def create_header(self):
        c = self.colors
        self.header = ctk.CTkFrame(
            self.window,
            fg_color=c["header"],
            height=72,
            corner_radius=0,
            border_width=0,
        )
        self.header.grid(row=0, column=1, sticky="ew")
        self.header.grid_propagate(False)
        self.header.grid_columnconfigure(0, weight=1)

        left = ctk.CTkFrame(self.header, fg_color="transparent")
        left.grid(row=0, column=0, sticky="w", padx=28, pady=14)

        self.header_title = ctk.CTkLabel(
            left,
            text="Conversation",
            font=ctk.CTkFont(family="Segoe UI Semibold", size=20, weight="bold"),
            text_color=c["text"],
        )
        self.header_title.pack(anchor="w")

        self.header_sub = ctk.CTkLabel(
            left,
            text="Ask about Python, OOP, AI, databases & more",
            font=ctk.CTkFont(family="Segoe UI", size=12),
            text_color=c["text_soft"],
        )
        self.header_sub.pack(anchor="w")

        self.status_pill = ctk.CTkFrame(
            self.header,
            fg_color=c["bubble_bot"],
            corner_radius=20,
            height=36,
        )
        self.status_pill.grid(row=0, column=1, padx=24, pady=18)

        self.online_dot = ctk.CTkLabel(
            self.status_pill,
            text="●  Online",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            text_color=c["success"],
            width=100,
        )
        self.online_dot.pack(padx=14, pady=6)

    def create_main_area(self):
        self.main = ctk.CTkFrame(
            self.window, fg_color=self.colors["bg"], corner_radius=0
        )
        self.main.grid(row=1, column=1, sticky="nsew")
        self.main.grid_rowconfigure(0, weight=1)
        self.main.grid_columnconfigure(0, weight=1)

    def create_chat_area(self):
        c = self.colors
        self.chat_wrap = ctk.CTkFrame(
            self.main,
            fg_color=c["chat_bg"],
            corner_radius=18,
            border_width=1,
            border_color=c["border"],
        )
        self.chat_wrap.grid(row=0, column=0, sticky="nsew", padx=22, pady=(12, 8))
        self.chat_wrap.grid_rowconfigure(0, weight=1)
        self.chat_wrap.grid_columnconfigure(0, weight=1)

        self.chat_area = ctk.CTkTextbox(
            self.chat_wrap,
            fg_color=c["chat_textbox_bg"],
            corner_radius=16,
            font=ctk.CTkFont(family="Segoe UI", size=14),
            text_color=c["text"],
            wrap="word",
            border_width=0,
            activate_scrollbars=True,
        )
        self.chat_area.grid(row=0, column=0, sticky="nsew", padx=8, pady=8)
        self.chat_area.configure(state="disabled")
        self._configure_chat_tags()

    def _configure_chat_tags(self):
        c = self.colors
        size = self.font_size
        tb = self.chat_area._textbox
        tb.configure(bg=c["chat_textbox_bg"], fg=c["text"], insertbackground=c["text"])
        tb.tag_configure(
            "bot_name", foreground=c["accent"], font=("Segoe UI Semibold", 12)
        )
        tb.tag_configure(
            "user_name", foreground=c["user_name"], font=("Segoe UI Semibold", 12)
        )
        tb.tag_configure(
            "time", foreground=c["text_soft"], font=("Segoe UI", 10)
        )
        tb.tag_configure(
            "bot_msg",
            foreground=c["text"],
            font=("Segoe UI", size),
            lmargin1=12,
            lmargin2=12,
            rmargin=40,
            spacing1=4,
            spacing3=10,
        )
        tb.tag_configure(
            "user_msg",
            foreground=c["user_msg"],
            font=("Segoe UI", size),
            lmargin1=40,
            lmargin2=40,
            rmargin=12,
            spacing1=4,
            spacing3=10,
        )
        tb.tag_configure(
            "sys",
            foreground=c["text_muted"],
            font=("Segoe UI", 12, "italic"),
            justify="center",
            spacing1=8,
            spacing3=8,
        )

    def create_bottom_bar(self):
        c = self.colors
        self.bottom = ctk.CTkFrame(
            self.window, fg_color=c["header"], height=88, corner_radius=0
        )
        self.bottom.grid(row=2, column=1, sticky="ew")
        self.bottom.grid_columnconfigure(0, weight=1)

        self.entry = ctk.CTkEntry(
            self.bottom,
            height=50,
            corner_radius=25,
            placeholder_text="Type your message…  (Enter to send)",
            font=ctk.CTkFont(family="Segoe UI", size=15),
            fg_color=c["input_bg"],
            border_color=c["border"],
            border_width=1,
            text_color=c["text"],
            placeholder_text_color=c["text_soft"],
        )
        self.entry.grid(row=0, column=0, padx=(22, 10), pady=18, sticky="ew")
        self.entry.bind("<Return>", self.send_message)
        self.entry.bind("<FocusIn>", self._entry_focus_in)
        self.entry.bind("<FocusOut>", self._entry_focus_out)

        self.send_button = ctk.CTkButton(
            self.bottom,
            text="Send",
            width=96,
            height=50,
            corner_radius=25,
            font=ctk.CTkFont(family="Segoe UI Semibold", size=15, weight="bold"),
            fg_color=c["accent"],
            hover_color=c["accent_hover"],
            text_color=c["send_text"],
            command=self.send_message,
        )
        self.send_button.grid(row=0, column=1, padx=(0, 22))

    def create_status_bar(self):
        c = self.colors
        self.footer = ctk.CTkLabel(
            self.window,
            text="Ready  ·  Press Enter to send",
            anchor="w",
            height=26,
            font=ctk.CTkFont(family="Segoe UI", size=11),
            text_color=c["text_soft"],
            fg_color=c["bg"],
        )
        self.footer.grid(row=3, column=1, sticky="ew", padx=24, pady=(0, 8))

    # --------------------------------------------------------- theme logic
    def _resolve_palette_key(self, choice):
        if choice == "Dark":
            return "dark"
        if choice == "Light":
            return "light"
        # System — follow OS after CustomTkinter resolves it
        resolved = ctk.get_appearance_mode().lower()
        return "light" if resolved == "light" else "dark"

    def _apply_theme(self, choice, reopen_settings=False):
        if self._theme_updating:
            return
        self._theme_updating = True

        self.theme_choice = choice
        mode = {"Dark": "dark", "Light": "light", "System": "system"}[choice]
        ctk.set_appearance_mode(mode)

        key = self._resolve_palette_key(choice)
        self.colors = dict(THEMES[key])
        c = self.colors

        self.window.configure(fg_color=c["bg"])
        self.sidebar.configure(fg_color=c["sidebar"])
        self.brand_title.configure(text_color=c["accent"])
        self.brand_sub.configure(text_color=c["text_soft"])
        self.sidebar_divider.configure(fg_color=c["accent_dim"])
        self.sidebar_foot.configure(text_color=c["text_soft"])

        for k, btn in self.nav_buttons.items():
            btn.configure(
                hover_color=c["sidebar_hover"],
                text_color=c["accent"] if self.active_nav == k else c["text"],
                fg_color=c["nav_active"] if self.active_nav == k else "transparent",
            )

        self.header.configure(fg_color=c["header"])
        self.header_title.configure(text_color=c["text"])
        self.header_sub.configure(text_color=c["text_soft"])
        self.status_pill.configure(fg_color=c["bubble_bot"])
        if self._typing:
            self.online_dot.configure(text_color=c["accent"])
        else:
            self.online_dot.configure(text_color=c["success"])

        self.main.configure(fg_color=c["bg"])
        self.chat_wrap.configure(fg_color=c["chat_bg"], border_color=c["border"])
        self.chat_area.configure(
            fg_color=c["chat_textbox_bg"],
            text_color=c["text"],
            font=ctk.CTkFont(family="Segoe UI", size=self.font_size),
        )
        self._configure_chat_tags()

        self.bottom.configure(fg_color=c["header"])
        self.entry.configure(
            fg_color=c["input_bg"],
            border_color=c["border"],
            text_color=c["text"],
            placeholder_text_color=c["text_soft"],
        )
        self.send_button.configure(
            fg_color=c["accent"],
            hover_color=c["accent_hover"],
            text_color=c["send_text"],
        )
        self.footer.configure(text_color=c["text_soft"], fg_color=c["bg"])

        # Rebuild open overlay so its children pick up new colors
        try:
            if self._overlay is not None and self._overlay_builder is not None:
                title = self._overlay_title
                subtitle = self._overlay_subtitle
                builder = self._overlay_builder
                self._overlay.destroy()
                self._overlay = None
                self._show_overlay(title, subtitle, builder)
            elif reopen_settings:
                self.on_settings()

            self.footer.configure(text=f"Theme set to {choice}")
        finally:
            self._theme_updating = False

    # ----------------------------------------------------------- chat logic
    def _greet(self):
        self.display_message(
            "Bot",
            "Hello! I'm RuleBot — your rule-based assistant.\n"
            "Ask me about Python, OOP, AI, databases, web tech, and more.\n"
            "Tip: open FAQs in the sidebar for quick starters.",
        )

    def display_message(self, sender, message, save=True):
        current = datetime.now().strftime("%I:%M %p")
        self.chat_area.configure(state="normal")

        if sender == "Bot":
            self.chat_area.insert("end", "RuleBot  ", "bot_name")
            self.chat_area.insert("end", f"{current}\n", "time")
            self.chat_area.insert("end", message + "\n\n", "bot_msg")
        elif sender == "You":
            self.chat_area.insert("end", "You  ", "user_name")
            self.chat_area.insert("end", f"{current}\n", "time")
            self.chat_area.insert("end", message + "\n\n", "user_msg")
        else:
            self.chat_area.insert("end", message + "\n", "sys")

        self.chat_area.configure(state="disabled")
        self.chat_area.see("end")

        if save and sender in ("Bot", "You"):
            self.chat_history.append(
                {"sender": sender, "message": message, "time": current}
            )

    def send_message(self, event=None):
        if self._typing:
            return

        message = self.entry.get().strip()
        if not message:
            return

        self.display_message("You", message)
        self.entry.delete(0, END)
        self._set_typing(True)
        self.window.after(650, lambda: self.reply(message))

    def reply(self, message):
        response = self.bot.get_response(message)
        self.display_message("Bot", response)
        self._set_typing(False)

    def _set_typing(self, on):
        self._typing = on
        c = self.colors
        if on:
            self.footer.configure(text="RuleBot is typing…")
            self.online_dot.configure(text="●  Typing…", text_color=c["accent"])
            self.send_button.configure(state="disabled")
        else:
            self.footer.configure(text="Online  ·  Press Enter to send")
            self.online_dot.configure(text="●  Online", text_color=c["success"])
            self.send_button.configure(state="normal")

    def _entry_focus_in(self, _e):
        self.entry.configure(border_color=self.colors["accent"])

    def _entry_focus_out(self, _e):
        self.entry.configure(border_color=self.colors["border"])

    # ------------------------------------------------------ sidebar actions
    def on_new_chat(self):
        self._set_active_nav("new")
        self._close_overlay()

        if self.chat_history:
            self.sessions.insert(
                0,
                {
                    "title": self._session_title(),
                    "messages": list(self.chat_history),
                    "saved_at": datetime.now().strftime("%d %b %Y, %I:%M %p"),
                },
            )
            self.sessions = self.sessions[:20]

        self.chat_history.clear()
        self.chat_area.configure(state="normal")
        self.chat_area.delete("1.0", END)
        self.chat_area.configure(state="disabled")

        self.display_message("System", "── New conversation started ──", save=False)
        self._greet()
        self.footer.configure(text="New chat started")

        def _reset_nav():
            self.active_nav = None
            for btn in self.nav_buttons.values():
                btn.configure(
                    fg_color="transparent", text_color=self.colors["text"]
                )
            self.footer.configure(text="Online  ·  Press Enter to send")

        self.window.after(1600, _reset_nav)

    def _session_title(self):
        for item in self.chat_history:
            if item["sender"] == "You":
                t = item["message"]
                return (t[:42] + "…") if len(t) > 42 else t
        return "Untitled chat"

    def on_history(self):
        self._set_active_nav("history")
        self._show_overlay(
            title="Chat History",
            subtitle="Previous conversations from this session",
            build_body=self._build_history_body,
        )

    def _build_history_body(self, parent):
        c = self.colors
        if not self.sessions:
            ctk.CTkLabel(
                parent,
                text="No saved chats yet.\nStart a conversation, then click New Chat to archive it here.",
                font=ctk.CTkFont(family="Segoe UI", size=13),
                text_color=c["text_muted"],
                justify="left",
            ).pack(anchor="w", padx=8, pady=12)
            return

        for i, session in enumerate(self.sessions):
            card = ctk.CTkFrame(
                parent,
                fg_color=c["bubble_bot"],
                corner_radius=12,
                border_width=1,
                border_color=c["border"],
            )
            card.pack(fill="x", padx=4, pady=6)

            ctk.CTkLabel(
                card,
                text=session["title"],
                font=ctk.CTkFont(family="Segoe UI Semibold", size=13, weight="bold"),
                text_color=c["text"],
                anchor="w",
            ).pack(fill="x", padx=14, pady=(12, 2))

            ctk.CTkLabel(
                card,
                text=f"{session['saved_at']}  ·  {len(session['messages'])} messages",
                font=ctk.CTkFont(family="Segoe UI", size=11),
                text_color=c["text_soft"],
                anchor="w",
            ).pack(fill="x", padx=14, pady=(0, 8))

            row = ctk.CTkFrame(card, fg_color="transparent")
            row.pack(fill="x", padx=10, pady=(0, 12))

            ctk.CTkButton(
                row,
                text="Load",
                width=80,
                height=32,
                corner_radius=10,
                fg_color=c["accent"],
                hover_color=c["accent_hover"],
                text_color=c["send_text"],
                font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
                command=lambda idx=i: self._load_session(idx),
            ).pack(side="left", padx=4)

            ctk.CTkButton(
                row,
                text="Delete",
                width=80,
                height=32,
                corner_radius=10,
                fg_color="transparent",
                hover_color=c["danger_bg"],
                text_color=c["danger"],
                border_width=1,
                border_color=c["danger"],
                font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
                command=lambda idx=i: self._delete_session(idx),
            ).pack(side="left", padx=4)

    def _load_session(self, index):
        if not (0 <= index < len(self.sessions)):
            return

        session = self.sessions.pop(index)
        self._close_overlay()

        if self.chat_history:
            self.sessions.insert(
                0,
                {
                    "title": self._session_title(),
                    "messages": list(self.chat_history),
                    "saved_at": datetime.now().strftime("%d %b %Y, %I:%M %p"),
                },
            )

        self.chat_history = list(session["messages"])
        self.chat_area.configure(state="normal")
        self.chat_area.delete("1.0", END)
        self.chat_area.configure(state="disabled")

        self.display_message(
            "System", f"── Loaded: {session['title']} ──", save=False
        )
        for msg in self.chat_history:
            current = msg.get("time", "")
            self.chat_area.configure(state="normal")
            if msg["sender"] == "Bot":
                self.chat_area.insert("end", "RuleBot  ", "bot_name")
                self.chat_area.insert("end", f"{current}\n", "time")
                self.chat_area.insert("end", msg["message"] + "\n\n", "bot_msg")
            else:
                self.chat_area.insert("end", "You  ", "user_name")
                self.chat_area.insert("end", f"{current}\n", "time")
                self.chat_area.insert("end", msg["message"] + "\n\n", "user_msg")
            self.chat_area.configure(state="disabled")
        self.chat_area.see("end")
        self.footer.configure(text="Conversation restored from history")

    def _delete_session(self, index):
        if 0 <= index < len(self.sessions):
            del self.sessions[index]
        self.on_history()

    def on_faqs(self):
        self._set_active_nav("faqs")
        self._show_overlay(
            title="Frequently Asked",
            subtitle="Click a question to ask RuleBot instantly",
            build_body=self._build_faqs_body,
        )

    def _build_faqs_body(self, parent):
        c = self.colors
        for label, query in FAQS:
            ctk.CTkButton(
                parent,
                text=label,
                height=42,
                corner_radius=12,
                fg_color=c["bubble_bot"],
                hover_color=c["nav_active"],
                text_color=c["text"],
                font=ctk.CTkFont(family="Segoe UI", size=13),
                anchor="w",
                border_width=1,
                border_color=c["border"],
                command=lambda q=query: self._ask_faq(q),
            ).pack(fill="x", padx=4, pady=5)

    def _ask_faq(self, query):
        self._close_overlay()
        self.active_nav = None
        for btn in self.nav_buttons.values():
            btn.configure(fg_color="transparent", text_color=self.colors["text"])

        self.entry.delete(0, END)
        self.entry.insert(0, query)
        self.send_message()

    def on_settings(self):
        self._set_active_nav("settings")
        self._show_overlay(
            title="Settings",
            subtitle="Appearance & chat preferences",
            build_body=self._build_settings_body,
        )

    def _build_settings_body(self, parent):
        c = self.colors
        ctk.CTkLabel(
            parent,
            text="Appearance mode",
            font=ctk.CTkFont(family="Segoe UI Semibold", size=13, weight="bold"),
            text_color=c["text"],
            anchor="w",
        ).pack(fill="x", padx=8, pady=(8, 6))

        theme = ctk.CTkSegmentedButton(
            parent,
            values=["Dark", "Light", "System"],
            command=self._change_theme,
            selected_color=c["accent"],
            selected_hover_color=c["accent_hover"],
            unselected_color=c["bubble_bot"],
            unselected_hover_color=c["sidebar_hover"],
            text_color=c["send_text"],
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            height=36,
        )
        theme.pack(fill="x", padx=8, pady=(0, 16))
        theme.set(self.theme_choice)

        ctk.CTkLabel(
            parent,
            text="Chat text size",
            font=ctk.CTkFont(family="Segoe UI Semibold", size=13, weight="bold"),
            text_color=c["text"],
            anchor="w",
        ).pack(fill="x", padx=8, pady=(4, 6))

        size_map = {12: "Small", 14: "Medium", 16: "Large"}
        size = ctk.CTkSegmentedButton(
            parent,
            values=["Small", "Medium", "Large"],
            command=self._change_font_size,
            selected_color=c["accent"],
            selected_hover_color=c["accent_hover"],
            unselected_color=c["bubble_bot"],
            unselected_hover_color=c["sidebar_hover"],
            text_color=c["send_text"],
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            height=36,
        )
        size.pack(fill="x", padx=8, pady=(0, 16))
        size.set(size_map.get(self.font_size, "Medium"))

        ctk.CTkButton(
            parent,
            text="Clear current chat",
            height=40,
            corner_radius=12,
            fg_color="transparent",
            hover_color=c["danger_bg"],
            text_color=c["danger"],
            border_width=1,
            border_color=c["danger"],
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            command=self._clear_current_chat,
        ).pack(fill="x", padx=8, pady=(8, 4))

    def _change_theme(self, value):
        if self._theme_updating:
            return
        self._apply_theme(value)

    def _change_font_size(self, value):
        sizes = {"Small": 12, "Medium": 14, "Large": 16}
        self.font_size = sizes.get(value, 14)
        self.chat_area.configure(
            font=ctk.CTkFont(family="Segoe UI", size=self.font_size)
        )
        self._configure_chat_tags()
        self.footer.configure(text=f"Font size: {value}")

    def _clear_current_chat(self):
        self._close_overlay()
        self.chat_history.clear()
        self.chat_area.configure(state="normal")
        self.chat_area.delete("1.0", END)
        self.chat_area.configure(state="disabled")
        self.display_message("System", "── Chat cleared ──", save=False)
        self._greet()

    def on_about(self):
        self._set_active_nav("about")
        self._show_overlay(
            title="About RuleBot",
            subtitle="Project information",
            build_body=self._build_about_body,
        )

    def _build_about_body(self, parent):
        c = self.colors
        about = (
            "RuleBot is a rule-based chatbot built with Python.\n\n"
            "Stack\n"
            "• Python + CustomTkinter for the interface\n"
            "• Regular expressions for pattern matching\n"
            "• Object-oriented design for the bot engine\n\n"
            "How it works\n"
            "Messages are matched against predefined rules. "
            "There is no machine learning — every answer comes from "
            "carefully written patterns in responses.py.\n\n"
            "Try asking about Python, OOP, Tkinter, Regex, AI, SQL, "
            "HTML, CSS, or JavaScript."
        )
        ctk.CTkLabel(
            parent,
            text=about,
            font=ctk.CTkFont(family="Segoe UI", size=13),
            text_color=c["text_muted"],
            justify="left",
            wraplength=420,
            anchor="w",
        ).pack(anchor="w", padx=8, pady=8)

        ctk.CTkButton(
            parent,
            text="Got it",
            height=40,
            corner_radius=12,
            fg_color=c["accent"],
            hover_color=c["accent_hover"],
            text_color=c["send_text"],
            font=ctk.CTkFont(family="Segoe UI Semibold", size=13, weight="bold"),
            command=self._close_overlay,
        ).pack(fill="x", padx=8, pady=(16, 4))

    # ------------------------------------------------------------- overlay
    def _show_overlay(self, title, subtitle, build_body):
        self._close_overlay(clear_nav=False)
        self._overlay_title = title
        self._overlay_subtitle = subtitle
        self._overlay_builder = build_body

        c = self.colors
        self._overlay = ctk.CTkFrame(
            self.main,
            fg_color=c["panel"],
            corner_radius=18,
            border_width=1,
            border_color=c["border"],
        )
        self._overlay.place(
            relx=0.5, rely=0.5, anchor="center", relwidth=0.72, relheight=0.86
        )

        head = ctk.CTkFrame(self._overlay, fg_color="transparent")
        head.pack(fill="x", padx=20, pady=(18, 6))
        head.grid_columnconfigure(0, weight=1)

        titles = ctk.CTkFrame(head, fg_color="transparent")
        titles.grid(row=0, column=0, sticky="w")

        ctk.CTkLabel(
            titles,
            text=title,
            font=ctk.CTkFont(family="Segoe UI Semibold", size=20, weight="bold"),
            text_color=c["text"],
            anchor="w",
        ).pack(anchor="w")

        ctk.CTkLabel(
            titles,
            text=subtitle,
            font=ctk.CTkFont(family="Segoe UI", size=12),
            text_color=c["text_soft"],
            anchor="w",
        ).pack(anchor="w")

        ctk.CTkButton(
            head,
            text="✕",
            width=36,
            height=36,
            corner_radius=10,
            fg_color=c["bubble_bot"],
            hover_color=c["danger_hover"],
            text_color=c["text"],
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            command=self._close_overlay,
        ).grid(row=0, column=1, sticky="e")

        scroll = ctk.CTkScrollableFrame(
            self._overlay,
            fg_color="transparent",
            corner_radius=0,
        )
        scroll.pack(fill="both", expand=True, padx=14, pady=(8, 18))
        build_body(scroll)

    def _close_overlay(self, clear_nav=True):
        if self._overlay is not None:
            self._overlay.destroy()
            self._overlay = None
            self._overlay_builder = None

        if clear_nav and self.active_nav and self.active_nav != "new":
            for btn in self.nav_buttons.values():
                btn.configure(
                    fg_color="transparent", text_color=self.colors["text"]
                )
            self.active_nav = None

    def run(self):
        self.window.mainloop()
