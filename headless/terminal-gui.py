#!/usr/bin/env python3
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Vte', '2.91')
from gi.repository import Gtk, Vte, GLib, Pango
import os
import sys

class TerminalApp(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Terminal GUI")
        self.set_default_size(800, 600)
        self.connect("destroy", Gtk.main_quit)
        
        # Create main vertical box
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        vbox.set_margin_top(10)
        vbox.set_margin_bottom(10)
        vbox.set_margin_start(10)
        vbox.set_margin_end(10)
        self.add(vbox)
        
        # Create command entry widget
        self.command_entry = Gtk.Entry()
        self.command_entry.set_placeholder_text("Enter shell command here...")
        self.command_entry.connect("activate", self.on_command_enter)
        vbox.pack_start(self.command_entry, False, False, 0)
        
        # Create run button
        run_button = Gtk.Button(label="Run Command")
        run_button.connect("clicked", self.on_command_enter)
        vbox.pack_start(run_button, False, False, 0)
        
        # Create terminal widget
        self.terminal = Vte.Terminal()
        self.terminal.set_font(Pango.FontDescription("Monospace 10"))
        self.terminal.set_scrollback_lines(10000)
        self.terminal.set_cursor_blink_mode(Vte.CursorBlinkMode.ON)
        
        # Spawn initial shell
        self.terminal.spawn_sync(
            Vte.PtyFlags.DEFAULT,
            os.environ['HOME'],
            ["/bin/bash"],
            [],
            GLib.SpawnFlags.DO_NOT_REAP_CHILD,
            None,
            None
        )
        
        # Add terminal to scrolled window for scrollbars
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scrolled_window.add(self.terminal)
        vbox.pack_start(scrolled_window, True, True, 0)
        
    def on_command_enter(self, widget):
        command = self.command_entry.get_text()
        if command:
            # Clear entry
            self.command_entry.set_text("")
            
            # Feed command to terminal with newline
            full_command = f"{command}\n"
            self.terminal.feed_child(full_command.encode())

def main():
    app = TerminalApp()
    app.show_all()
    Gtk.main()

if __name__ == "__main__":
    main()
