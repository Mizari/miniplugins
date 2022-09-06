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
def set_pseudocode_widget_name_safely(w, new_name):
	current_name = w.windowTitle()
	if current_name == new_name:
		return False
	if current_name.startswith("IDA View-"):
		return False
	if current_name in BADNAMES:
		return False
	w.setWindowTitle(new_name)
	return True


class RenamingHook(idaapi.Hexrays_Hooks):
	def open_pseudocode(self, vu):
		w = get_current_widget()
		funcname = idaapi.get_name(vu.cfunc.entry_ea)
		set_pseudocode_widget_name_safely(w, funcname)
		return 0

	def switch_pseudocode(self, vu):
		w = get_current_widget()
		funcname = idaapi.get_name(vu.cfunc.entry_ea)
		set_pseudocode_widget_name_safely(w, funcname)
		return 0



class PseudocodeRenamer(idaapi.plugin_t):
	flags = 0
	wanted_name = "pseudocode renamer"

	def init(self):
		if idaapi.init_hexrays_plugin():
			self.h = RenamingHook()
			self.h.hook()

		return idaapi.PLUGIN_KEEP

	def run(self, arg):
		return

	def term(self):
		return

def PLUGIN_ENTRY():
	return PseudocodeRenamer()