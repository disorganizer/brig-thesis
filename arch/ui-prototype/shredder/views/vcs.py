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

# Internal:
from shredder.util import View, IconButton, size_to_human_readable
from shredder.util import PopupMenu, NodeState


def create_entry(val_widget, summary, desc=None):
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
    return row


def checkout_button():
    btn = Gtk.Button()
    btn.add(Gtk.Arrow(Gtk.ArrowType.RIGHT, Gtk.ShadowType.NONE))
    btn.set_relief(Gtk.ReliefStyle.NONE)
    return btn


def checkpoint_button():
    box = Gtk.Box()
    box.get_style_context().add_class(Gtk.STYLE_CLASS_LINKED)

    box.pack_start(IconButton('document-save-symbolic', ''), True, False, 0)
    box.pack_start(IconButton('edit-undo-symbolic', ''), True, False, 0)

    box.set_hexpand(False)
    box.set_vexpand(False)
    box.set_valign(Gtk.Align.CENTER)
    box.set_margin_end(15)
    return box


class VCSView(View):
    """The actual view instance."""
    def __init__(self, app):
        View.__init__(self, app)
        self.sub_title = 'View and modify the history'

        commit_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        commit_box = Gtk.ListBox()
        commit_box.set_selection_mode(Gtk.SelectionMode.SINGLE)
        commit_box.set_size_request(350, -1)
        commit_box.set_hexpand(True)

        commits = [
            ('#4: <b>Uncommitted changes</b>', 'Created on 2016-10-23 by <span foreground="#008888">alice</span>'),
            ('#3: <b>Reorganized photo collection</b>', '2016 on 2016-10-23 by <span foreground="#008888">alice</span>'),
            ('#2: <b>Nuclear assault weapon docs</b>', 'Merged with <span foreground="#880088">bob/laptop</span> on 2016-10-22'),
            ('#1: <b>Autocommit</b>', 'Merged with <span foreground="#000088">bob/desktop</span> on 2016-10-21')
        ]

        for idx, (title, desc) in enumerate(commits):
            commit_box.insert(create_entry(checkout_button(), title, desc), -1)
            if idx != len(commits) - 1:
                sep = Gtk.Separator()
                commit_box.insert(sep, -1)

        checkpoint_box = Gtk.ListBox()
        checkpoint_box.set_selection_mode(Gtk.SelectionMode.NONE)
        checkpoint_box.set_hexpand(True)

        header_label = Gtk.Label()
        header_label.set_markup('<b>Commit #2</b> – Reorganized photo collection')
        header_label.get_style_context().add_class(Gtk.STYLE_CLASS_DIM_LABEL)

        checkpoint_box.insert(header_label, -1)
        checkpoint_box.insert(Gtk.Separator(), -1)

        checkpoints = [
            ('/photos/me.png',  '<span foreground="#006600"><b>Added</b></span> on 2016-10-23 14:29:01'),
            ('/photos/cat.png <small>(was /photos/kat.png)</small>', '<span foreground="#0000BB">Moved</span> on 2016-10-23 14:33:02'),
            ('/photos/dog.png', '<span foreground="#006600"><b>Added</b></span> on 2016-10-23 14:33:23'),
            ('/photos/owl.png', '<span foreground="#666600"><b>Modified</b></span> on 2016-10-23 14:34:59'),
            ('/notes.txt',      '<span foreground="#660000"><b>Removed</b></span> on ~9 minutes ago'),
            ('/movies/big.mkv', '<span foreground="#006600"><b>Added</b></span> ~5 minutes ago'),
        ]

        for idx, (summ, desc) in enumerate(checkpoints):
            checkpoint_box.insert(
                create_entry(
                    checkpoint_button(),
                    summ,
                    desc,
                ),
                -1
            )

            if idx != len(checkpoints) - 1:
                checkpoint_box.insert(Gtk.Separator(), -1)

        frame = Gtk.Frame()
        frame.add(checkpoint_box)

        scw = Gtk.ScrolledWindow()
        scw.set_border_width(12)
        scw.add(frame)

        stat_label = Gtk.Label('4 commits, 7 changes selected')

        add_commit_btn = IconButton('list-add-symbolic', 'Make commit')
        add_commit_btn.get_style_context().add_class(
            Gtk.STYLE_CLASS_SUGGESTED_ACTION
        )

        add_commit_btn.set_margin_top(5)
        add_commit_btn.set_margin_bottom(5)
        add_commit_btn.set_margin_start(5)
        add_commit_btn.set_margin_end(5)

        ctrl_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        ctrl_box.pack_start(add_commit_btn, False, False, 0)
        ctrl_box.pack_end(stat_label, True, False, 0)

        commit_container.pack_start(commit_box, True, True, 0)
        commit_container.pack_start(Gtk.Separator(), False, False, 0)
        commit_container.pack_start(ctrl_box, False, False, 0)

        paned = Gtk.Paned()
        paned.add1(commit_container)
        paned.add2(scw)
        paned.set_hexpand(True)
        paned.set_vexpand(True)
        self.add(paned)
