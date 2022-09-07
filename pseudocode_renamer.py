import idaapi
import PyQt5

def get_current_widget():
	tw = idaapi.get_current_viewer()
	w = idaapi.PluginForm.FormToPyQtWidget(tw)
	parent = w.parent()
	if parent is None:
		return None
	if not isinstance(parent, PyQt5.QtWidgets.QSplitter):
		return None
	return parent

BADNAMES = {"Structures", "Local Types", "Strings"}
def is_bad_name(name):
	if name.startswith("IDA View-"):
		return True
	if name in BADNAMES:
		return True
	return False

def set_pseudocode_widget_name_safely(w, new_name):
	current_name = w.windowTitle()
	if current_name == new_name:
		return False
	if is_bad_name(current_name):
		return False
	w.setWindowTitle(new_name)
	return True


class RenamingHook(idaapi.Hexrays_Hooks):
	def __init__(self):
		self.original_names = []
		super().__init__()

	def get_original_name(self, search_name):
		for (renamed_title_name, original_name) in self.original_names:
			if renamed_title_name == search_name:
				return original_name
		return None

	def get_original_name_idx(self, search_name):
		for idx, (renamed_title_name, _) in enumerate(self.original_names):
			if renamed_title_name == search_name:
				return idx
		return None

	def open_pseudocode(self, vu):
		w = get_current_widget()
		funcname = idaapi.get_name(vu.cfunc.entry_ea)
		orig_name = w.windowTitle()
		if not set_pseudocode_widget_name_safely(w, funcname):
			return 0

		self.original_names.append((funcname, orig_name))
		return 0

	def switch_pseudocode(self, vu):
		w = get_current_widget()
		current_title_name = w.windowTitle()

		for orig_idx, (renamed_title_name, original_name) in enumerate(self.original_names):
			if renamed_title_name == current_title_name:
				break
		else:
			original_name = current_title_name
			orig_idx = -1

		funcname = idaapi.get_name(vu.cfunc.entry_ea)
		if not set_pseudocode_widget_name_safely(w, funcname):
			return 0

		if orig_idx == -1:
			self.original_names.append((funcname, original_name))
		else:
			self.original_names[orig_idx] = (funcname, original_name)
		return 0

	def drop_names(self):
		tw = idaapi.get_current_viewer()
		w = idaapi.PluginForm.FormToPyQtWidget(tw)
		while w is not None:
			if isinstance(w, PyQt5.QtWidgets.QStackedWidget):
				break
			w = w.parent()

		for c in w.children():
			if not hasattr(c, "windowTitle"):
				continue 
			child_name = c.windowTitle()
			orig_name_idx = self.get_original_name_idx(child_name)
			if orig_name_idx is None:
				continue

			orig_name = self.original_names.pop(orig_name_idx)[1]

			for c1 in c.children():
				if not hasattr(c1, "windowTitle"):
					continue 
				if c1.windowTitle() == child_name:
					c1.setWindowTitle(orig_name)


class MyIDBHook(idaapi.IDB_Hooks):
	def __init__(self, rhook: RenamingHook):
		self.rhook = rhook
		super().__init__()

	def savebase(self):
		self.rhook.drop_names()

	def closebase(self):
		self.rhook.drop_names()


class PseudocodeRenamer(idaapi.plugin_t):
	flags = 0
	wanted_name = "pseudocode renamer"

	def init(self):
		if idaapi.init_hexrays_plugin():
			self.renamer_hook = RenamingHook()
			self.renamer_hook.hook()
			self.idb_hook = MyIDBHook(self.renamer_hook)
			self.idb_hook.hook()

		return idaapi.PLUGIN_KEEP

	def run(self, arg):
		return

	def term(self):
		return

def PLUGIN_ENTRY():
	return PseudocodeRenamer()