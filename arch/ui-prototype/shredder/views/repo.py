#!/usr/bin/env python
# encoding: utf-8

"""Location view.

Give the users a list of directories he might want to scan.
Also give him the choice of adding new directories.

Integrate with GtkRecentManager and detect mounted volumes.
Also show the directory size alongside.
"""


# Stdlib:
import os
import logging

# External:
from gi.repository import Gtk
from gi.repository import GdkPixbuf

from shredder.util import View, IconButton, size_to_human_readable


def create_entry(val_widget, summary, desc=None):
    box = Gtk.ListBox()
    box.set_selection_mode(Gtk.SelectionMode.NONE)
    box.set_size_request(350, -1)
    box.set_hexpand(True)

    desc_label = Gtk.Label(desc or '')
    summ_label = Gtk.Label(summary or '')

    desc_label.get_style_context().add_class(
        Gtk.STYLE_CLASS_DIM_LABEL
    )

    for label in desc_label, summ_label:
        label.set_use_markup(True)
        label.set_halign(Gtk.Align.FILL)
        label.set_hexpand(True)
        label.set_halign(Gtk.Align.START)

    val_widget.set_halign(Gtk.Align.END)

    sub_grid = Gtk.Grid()
    sub_grid.attach(summ_label, 0, 0, 1, 1)
    sub_grid.attach(desc_label, 0, 1, 1, 1)
    sub_grid.attach(val_widget, 1, 0, 1, 2)
    sub_grid.set_border_width(3)

    row = Gtk.ListBoxRow()
    row.add(sub_grid)
    row.set_can_focus(False)
    box.insert(row, -1)
    return box


def create_separator():
    sep = Gtk.Separator()
    sep.set_halign(Gtk.Align.FILL)
    sep.set_hexpand(True)
    return sep


def make_double_widget(a, b):
    box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
    box.pack_start(a, True, True, 0)
    box.pack_start(b, True, False, 0)

    return box



class RepoView(View):
    """The actual view instance."""
    def __init__(self, app):
        View.__init__(self, app)
        self.sub_title = 'Repository creating wizard'

        grid = Gtk.Grid()
        grid.set_hexpand(True)
        grid.set_vexpand(True)
        grid.set_valign(Gtk.Align.CENTER)
        grid.set_halign(Gtk.Align.FILL)
        grid.set_margin_start(30)
        grid.set_margin_end(30)

        header = Gtk.Label()
        header.set_markup('<b><big>We just need a tiny bit of info to get you connected…</big></b>')
        header.set_margin_bottom(30)
        header.get_style_context().add_class(Gtk.STYLE_CLASS_DIM_LABEL)

        footer = Gtk.Label()
        footer.set_markup(
            '<big><b>🔌</b></big> If you want to use a Yubikey, plug it in now.'
        )
        footer.set_margin_top(30)
        footer.get_style_context().add_class(Gtk.STYLE_CLASS_DIM_LABEL)

        user_entry = Gtk.Entry()
        user_entry.set_hexpand(True)
        user_entry.set_vexpand(False)
        user_entry.set_valign(Gtk.Align.CENTER)
        user_entry.set_halign(Gtk.Align.FILL)
        user_entry.set_margin_start(15)

        user_label = Gtk.Label()
        user_label.set_markup('<span foreground="#BB9900">⚠ This username seems to be taken.</span>')

        pass_entry = Gtk.Entry()
        pass_entry.set_hexpand(True)
        pass_entry.set_vexpand(False)
        pass_entry.set_valign(Gtk.Align.CENTER)
        pass_entry.set_halign(Gtk.Align.FILL)
        pass_entry.set_visibility(False)
        pass_entry.set_margin_start(15)

        level_bar = Gtk.LevelBar()
        level_bar.set_valign(Gtk.Align.START)
        level_bar.set_halign(Gtk.Align.CENTER)
        level_bar.set_vexpand(False)
        level_bar.set_size_request(150, 10)
        level_bar.set_value(0.9)

        pass_label = Gtk.Label()
        pass_label.set_markup('<span foreground="#00AA00">✔ Entropy 33/30</span>')

        pass_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        pass_box.pack_start(pass_label, True, False, 0)
        pass_box.pack_start(level_bar, True, False, 0)

        double_pass_entry = Gtk.Entry()
        double_pass_entry.set_hexpand(True)
        double_pass_entry.set_vexpand(False)
        double_pass_entry.set_valign(Gtk.Align.CENTER)
        double_pass_entry.set_halign(Gtk.Align.FILL)
        double_pass_entry.set_visibility(False)
        double_pass_entry.set_margin_start(15)

        double_pass_label = Gtk.Label()
        double_pass_label.set_markup('<span foreground="#AA0000">✗ Passwords do not match :-(</span>')

        file_chooser = Gtk.FileChooserButton()
        file_chooser.set_action(Gtk.FileChooserAction.SELECT_FOLDER)

        sub_grid = Gtk.Grid()
        sub_grid.attach(create_entry(make_double_widget(user_label, user_entry), 'Username', 'This is how you are known in the network.'), 1, 1, 1, 1)
        sub_grid.attach(create_separator(), 1, 2, 1, 1)
        sub_grid.attach(create_entry(make_double_widget(pass_box, pass_entry), 'Passphrase', 'Remember this, you will need it to access your files!'), 1, 3, 1, 1)
        sub_grid.attach(create_separator(), 1, 4, 1, 1)
        sub_grid.attach(create_entry(make_double_widget(double_pass_label, double_pass_entry), 'Repeat the Passphrase', 'Annoying, we know. But this is for your own safety.'), 1, 5, 1, 1)
        sub_grid.attach(create_separator(), 1, 6, 1, 1)
        sub_grid.attach(create_entry(file_chooser, 'Repository Path', 'Where shall we create the new repository?'), 1, 7, 1, 1)

        frame = Gtk.Frame()
        frame.add(sub_grid)

        grid.attach(header, 0, 0, 1, 1)
        grid.attach(frame, 0, 1, 1, 1)
        grid.attach(footer, 0, 2, 1, 1)

        self.set_border_width(50)
        self.add(grid)

    def on_view_enter(self):
        """Called when the view gets visible."""
        create_button = IconButton('emblem-ok-symbolic', 'Create repository')
        create_button.get_style_context().add_class(Gtk.STYLE_CLASS_SUGGESTED_ACTION)
        self.add_header_widget(create_button)

