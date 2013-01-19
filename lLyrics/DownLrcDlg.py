#!/usr/bin/python
# -*- coding: utf-8 -*-


from gi.repository import Gtk
from gi.repository import GObject


class DownLrcDlg(Gtk.Dialog):
    """
    Download lyrics dialog.
    """
    def __init__(self, parent, artist, title, server, lrc_list):
        Gtk.Dialog.__init__(self, "Download Lyrics Dialog", parent, 0,
                            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                             Gtk.STOCK_OK, Gtk.ResponseType.OK))
        box = self.get_content_area()

        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        l1 = Gtk.Label('Artist')
        l2 = Gtk.Label(artist)
        # l2.set_markup("<b>{0}</b>".format(artist))
        l3 = Gtk.Label('Title')
        l4 = Gtk.Label(title)
        # l4.set_markup("<b>{0}</b>".format(title))
        l5 = Gtk.Label('Server')
        l6 = Gtk.Label(server)
        # l6.set_markup("<b>{0}</b>".format(server))
        hbox.pack_start(l1, False, False, 0)
        hbox.pack_start(l2, False, False, 0)
        hbox.pack_start(l3, False, False, 0)
        hbox.pack_start(l4, False, False, 0)
        hbox.pack_start(l5, False, False, 0)
        hbox.pack_start(l6, False, False, 0)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        vbox.pack_start(hbox, True, True, 0)

        self.liststore = Gtk.ListStore(str, str, str, str)
        for i in lrc_list:
            self.liststore.append(i)

        treeview = Gtk.TreeView(model=self.liststore)

        rt1 = Gtk.CellRendererText()
        ct1 = Gtk.TreeViewColumn("Artist", rt1, text=0)
        treeview.append_column(ct1)

        rt2 = Gtk.CellRendererText()
        ct2 = Gtk.TreeViewColumn("Title", rt2, text=1)
        treeview.append_column(ct2)

        rt3 = Gtk.CellRendererText()
        ct3 = Gtk.TreeViewColumn("Album", rt3, text=2)
        treeview.append_column(ct3)

        vbox.pack_start(treeview, True, True, 0)
        box.add(vbox)

        self.selection = treeview.get_selection()
        self.selection.set_mode(Gtk.SelectionMode.SINGLE)
        self.selection.connect("changed", self.on_select_changed)
        # self.time_id = GObject.timeout_add(10000, self.time_over)

        self.show_all()

    def time_over(self):
        model, treeiter = self.selection.get_selected()
        value = self.liststore.get_value(treeiter, 3)
        print value
        GObject.source_remove(self.time_id)
        self.time_id = None
        self.response(Gtk.ResponseType.OK)
        self.hide()

    def on_select_changed(self, widget):
        model, treeiter = self.selection.get_selected()
        if treeiter is not None:
            print str(treeiter)
            print "You selected", model[treeiter][0]

    def get_lrc_url(self):
        model, treeiter = self.selection.get_selected()
        value = self.liststore.get_value(treeiter, 3)
        return value
