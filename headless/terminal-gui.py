#!/usr/bin/env python3
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Vte', '2.91')
from gi.repository import Gtk, Vte, GLib, Pango, Gdk
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
        
        # ===== TERMINAL CUSTOMIZATION =====
        
        # Set font (you can change size and font family)
        self.terminal.set_font(Pango.FontDescription("Monospace 12"))
        
        # Set scrollback lines (increase for more history)
        self.terminal.set_scrollback_lines(10000)
        
        # Set cursor blink mode (ON, OFF, or SYSTEM)
        self.terminal.set_cursor_blink_mode(Vte.CursorBlinkMode.ON)
        
        # ===== COLOR CUSTOMIZATION =====
        
        # Method 1: Set foreground and background colors
        # Create Gdk.RGBA colors (values from 0 to 1.0)
        bg_color = Gdk.RGBA()
        fg_color = Gdk.RGBA()
        
        # Black background (red, green, blue, alpha)
        bg_color.parse("#1E1E1E")  # Dark gray background
        
        # White text
        fg_color.parse("#F0F0F0")  # Light gray text
        
        # Apply the colors
        self.terminal.set_color_background(bg_color)
        self.terminal.set_color_foreground(fg_color)
        
        # Set cursor color
        cursor_color = Gdk.RGBA()
        cursor_color.parse("#00FF00")  # Green cursor
        self.terminal.set_color_cursor(cursor_color)
        
        # Method 2: Set the entire color palette (16 colors)
        # This sets the standard terminal colors (0-15)
        palette = []
        
        # Define your color scheme (these are Solarized Dark colors as an example)
        color_schemes = {
            "solarized_dark": [
                "#073642",  # black
                "#DC322F",  # red
                "#859900",  # green
                "#B58900",  # yellow
                "#268BD2",  # blue
                "#D33682",  # magenta
                "#2AA198",  # cyan
                "#EEE8D5",  # white
                "#002B36",  # bright black
                "#CB4B16",  # bright red
                "#586E75",  # bright green
                "#657B83",  # bright yellow
                "#839496",  # bright blue
                "#6C71C4",  # bright magenta
                "#93A1A1",  # bright cyan
                "#FDF6E3",  # bright white
            ],
            "monokai": [
                "#272822",  # black
                "#F92672",  # red
                "#A6E22E",  # green
                "#F4BF75",  # yellow
                "#66D9EF",  # blue
                "#AE81FF",  # magenta
                "#A1EFE4",  # cyan
                "#F8F8F2",  # white
                "#75715E",  # bright black
                "#F92672",  # bright red
                "#A6E22E",  # bright green
                "#F4BF75",  # bright yellow
                "#66D9EF",  # bright blue
                "#AE81FF",  # bright magenta
                "#A1EFE4",  # bright cyan
                "#F9F8F5",  # bright white
            ]
        }
        
        # Choose your color scheme
        active_scheme = "monokai"  # Change to "solarized_dark" or your own custom scheme
        
        # Parse the colors for the palette
        for color_str in color_schemes[active_scheme]:
            color = Gdk.RGBA()
            color.parse(color_str)
            palette.append(color)
        
        # Apply the palette
        self.terminal.set_colors(fg_color, bg_color, palette)
        
        # ===== COPY/PASTE FUNCTIONALITY =====
        
        # Enable selection
        self.terminal.set_allow_hyperlink(True)
        
        # Make hyperlinks clickable
        self.terminal.set_allow_hyperlink(True)
        
        # Create right-click menu for copy/paste
        self.create_context_menu()
        
        # Connect to right-click event
        self.terminal.connect("button-press-event", self.on_button_press)
        
        # Connect to key press for keyboard shortcuts
        self.terminal.connect("key-press-event", self.on_key_press)
        
        # ===== SPAWN SHELL =====
        
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
        
    def create_context_menu(self):
        """Create a right-click context menu for copy/paste."""
        self.menu = Gtk.Menu()
        
        # Copy menu item
        copy_item = Gtk.MenuItem(label="Copy")
        copy_item.connect("activate", self.on_copy_activate)
        self.menu.append(copy_item)
        
        # Paste menu item
        paste_item = Gtk.MenuItem(label="Paste")
        paste_item.connect("activate", self.on_paste_activate)
        self.menu.append(paste_item)
        
        # Select All menu item
        select_all_item = Gtk.MenuItem(label="Select All")
        select_all_item.connect("activate", self.on_select_all_activate)
        self.menu.append(select_all_item)
        
        self.menu.show_all()
    
    def on_button_press(self, widget, event):
        """Handle mouse button press events."""
        # Right-click event
        if event.button == 3:  # Right mouse button
            # Show context menu
            self.menu.popup_at_pointer(event)
            return True
        return False
    
    def on_key_press(self, widget, event):
        """Handle keyboard shortcuts."""
        # Check for Ctrl+Shift+C (copy) and Ctrl+Shift+V (paste)
        ctrl = (event.state & Gdk.ModifierType.CONTROL_MASK)
        shift = (event.state & Gdk.ModifierType.SHIFT_MASK)
        
        if ctrl and shift:
            if event.keyval == Gdk.KEY_c:
                self.copy_selection()
                return True
            elif event.keyval == Gdk.KEY_v:
                self.paste_clipboard()
                return True
        return False
    
    def on_copy_activate(self, widget):
        """Copy selected text."""
        self.copy_selection()
    
    def on_paste_activate(self, widget):
        """Paste from clipboard."""
        self.paste_clipboard()
    
    def on_select_all_activate(self, widget):
        """Select all text."""
        self.terminal.select_all()
    
    def copy_selection(self):
        """Copy selected text to clipboard."""
        self.terminal.copy_clipboard_format(Vte.Format.TEXT)
    
    def paste_clipboard(self):
        """Paste from clipboard."""
        self.terminal.paste_clipboard()
        
    def on_command_enter(self, widget):
        """Handle command entry."""
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
