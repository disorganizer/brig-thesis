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

def icon_pixbuf(name):
    theme = Gtk.IconTheme.get_default()
    info = Gtk.IconTheme.lookup_icon_for_scale(theme, name, 64, 1, 0)
    return Gtk.IconInfo.load_icon(info)



def on_button_press_event(_, event):
    """Callback handler only used for mouse clicks."""
    if event.button != 3:
        return

    menu = PopupMenu()
    menu.simple_add_checkbox('Pin file', None)
    menu.simple_add('Show History', None)
    menu.simple_add_separator()
    menu.simple_add('Import file', None)
    menu.simple_add('Export file', None)
    menu.simple_add('Remove', None)
    menu.simple_add('New Folder', None)
    menu.simple_add_separator()
    menu.simple_add('Open in file browser', None)
    menu.simple_popup(event)


class BrowserView(View):
    """The actual view instance."""
    def __init__(self, app):
        View.__init__(self, app)
        self.sub_title = 'View and pin some files'


        sidebar = Gtk.PlacesSidebar()
        browser = Gtk.IconView()
        browser.connect('button-press-event', on_button_press_event)

        model = Gtk.ListStore(str, GdkPixbuf.Pixbuf)
        model.append(['Schreibtisch', icon_pixbuf('folder')])
        model.append(['Bilder', icon_pixbuf('folder')])
        model.append(['Dokumente', icon_pixbuf('folder-download')])
        model.append(['Downloads', icon_pixbuf('folder')])
        model.append(['Musik', icon_pixbuf('folder')])
        model.append(['Videos', icon_pixbuf('folder')])
        model.append(['Public', icon_pixbuf('folder-publicshare')])
        model.append(['notes.txt', icon_pixbuf('emblem-documents')])

        browser.set_model(model)
        browser.set_markup_column(0)
        browser.set_pixbuf_column(1)

        paned = Gtk.Paned()
        paned.add1(sidebar)
        paned.add2(browser)

        paned.set_hexpand(True)
        paned.set_vexpand(True)

        self.add(paned)
