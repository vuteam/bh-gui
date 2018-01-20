# -*- coding: UTF-8 -*-
from enigma import eListboxPythonMultiContent, gFont, RT_HALIGN_CENTER, RT_VALIGN_CENTER, getPrevAsciiCode
from Screen import Screen
from Components.Language import language
from Components.ActionMap import NumberActionMap
from Components.Sources.StaticText import StaticText
from Components.Input import Input
from Components.Label import Label
from Components.Pixmap import Pixmap
from Components.MenuList import MenuList
from Components.MultiContent import MultiContentEntryText, MultiContentEntryPixmapAlphaTest
from Tools.Directories import resolveFilename, SCOPE_CURRENT_SKIN
from Tools.LoadPixmap import LoadPixmap
from Tools.NumericalTextInput import NumericalTextInput
import skin

class VirtualKeyBoardList(MenuList):
	def __init__(self, list, enableWrapAround=False):
		MenuList.__init__(self, list, enableWrapAround, eListboxPythonMultiContent)
		self.l.setFont(0, gFont("Regular", 28))
		self.l.setItemHeight(45)

KEY_IMAGES =  {
		"BACKSPACE": "skin_default/vkey_backspace.png",
		"CLEAR": "skin_default/vkey_clr.png",
		"EXIT": "skin_default/vkey_esc.png",
		"OK": "skin_default/vkey_ok.png",
		"SHIFT": "skin_default/vkey_shift.png",
		"SPACE": "skin_default/vkey_space.png",
		}
KEY_IMAGES_SHIFT = {
		"BACKSPACE": "skin_default/vkey_backspace.png",
		"CLEAR": "skin_default/vkey_clr.png",
		"EXIT": "skin_default/vkey_esc.png",
		"OK": "skin_default/vkey_ok.png",
		"SHIFT": "skin_default/vkey_shift_sel.png",
		"SPACE": "skin_default/vkey_space.png",
		}
def VirtualKeyBoardEntryComponent(keys, selectedKey, shiftMode=False):
	key_bg = LoadPixmap(cached=True, path=resolveFilename(SCOPE_CURRENT_SKIN, "skin_default/vkey_bg.png"))
	key_bg_width = key_bg.size().width()
	if shiftMode:
		key_images = KEY_IMAGES_SHIFT
	else:
		key_images = KEY_IMAGES
	res = [ (keys) ]
	x = 0
	count = 0
	for count, key in enumerate(keys):
		width = None
		png = key_images.get(key, None)
		if png:
			pixmap = LoadPixmap(cached=True, path=resolveFilename(SCOPE_CURRENT_SKIN, png))
			width = pixmap.size().width()
			res.append(MultiContentEntryPixmapAlphaTest(pos=(x, 0), size=(width, 45), png=pixmap))
		else:
			width = key_bg_width
			res.extend((
				MultiContentEntryPixmapAlphaTest(pos=(x, 0), size=(width, 45), png=key_bg),
				MultiContentEntryText(pos=(x, 0), size=(width, 45), font=0, text=key.encode("utf-8"), flags=RT_HALIGN_CENTER | RT_VALIGN_CENTER)
			))
		if selectedKey == count:
			key_sel = LoadPixmap(cached=True, path=resolveFilename(SCOPE_CURRENT_SKIN, "skin_default/vkey_sel.png"))
			width = key_sel.size().width()
			res.append(MultiContentEntryPixmapAlphaTest(pos=(x, 0), size=(width, 45), png=key_sel))
		if width is not None:
			x += width
		else:
			x += 45
	return res


class VirtualKeyBoard(Screen):

	def __init__(self, session, title="", **kwargs):
		Screen.__init__(self, session)
		self.setTitle(_("Virtual keyboard"))
		self.keys_list = []
		self.shiftkeys_list = []
		self.lang = language.getLanguage()
		self.nextLang = None
		self.shiftMode = False
		self.selectedKey = 0
		self.smsChar = None
		self.sms = NumericalTextInput(self.smsOK)		
		self["country"] = StaticText("")
		self["header"] = Label(title)
		self["text"] = Input(currPos=len(kwargs.get("text", "").decode("utf-8",'ignore')), allMarked=False, **kwargs)
		self["list"] = VirtualKeyBoardList([])
		
		self["actions"] = NumberActionMap(["OkCancelActions", "WizardActions", "ColorActions", "KeyboardInputActions", "InputBoxActions", "InputAsciiActions"],
			{
				"gotAsciiCode": self.keyGotAscii,
				"ok": self.okClicked,
				"cancel": self.exit,
				"left": self.left,
				"right": self.right,
				"up": self.up,
				"down": self.down,
				"red": self.exit,
				"green": self.ok,
				"yellow": self.switchLang,
				"blue": self.shiftClicked,
				"deleteBackward": self.backClicked,
				"deleteForward": self.forwardClicked,
				"back": self.exit,
				"pageUp": self.cursorRight,
				"pageDown": self.cursorLeft,
				"1": self.keyNumberGlobal,
				"2": self.keyNumberGlobal,
				"3": self.keyNumberGlobal,
				"4": self.keyNumberGlobal,
				"5": self.keyNumberGlobal,
				"6": self.keyNumberGlobal,
				"7": self.keyNumberGlobal,
				"8": self.keyNumberGlobal,
				"9": self.keyNumberGlobal,
				"0": self.keyNumberGlobal,
			}, -2)
		self.setLang()
		self.onExecBegin.append(self.setKeyboardModeAscii)
		self.onLayoutFinish.append(self.buildVirtualKeyBoard)
		self.onClose.append(self.__onClose)

	def __onClose(self):
		self.sms.timer.stop()
	
	def switchLang(self):
		self.lang = self.nextLang
		self.setLang()
		self.buildVirtualKeyBoard()

	def setLang(self):
		if self.lang == 'ar_AE':
			self.keys_list = [
				[u"EXIT", u"1", u"2", u"3", u"4", u"5", u"6", u"7", u"8", u"9", u"0", u"BACKSPACE"],
				[u"ض", u"ص", u"ث", u"ق", u"ف", u"غ", u"ع", u"ه", u"خ", u"ح", u"ج", u"د"],
				[u"ش", u"س", u"ي", u"ب", u"ل", u"ا", u"ت", u"ن", u"م", u"ك", u"ط", u"#"],
				[u"ئ", u"ء", u"ؤ", u"ر", u"لا", u"ى", u"ة", u"و", u"ز", "ظ", u"ذ", u"CLEAR"],
				[u"SHIFT", u"SPACE", u"+", u"-", u"*", u"/", u".", u",", u"@", u"%", u"&", u"OK"]]
			self.shiftkeys_list = [
				[u"EXIT", u"!", u'"', u"§", u"$", u"^", u"<", u">", u"(", u")", u"=", u"BACKSPACE"],
				[u"َ", u"ً", u"ُ", u"ٌ", u"لإ", u"إ", u"‘", u"÷", u"×", u"؛", u"<", u">"],
				[u"ِ", u"ٍ", u"]", u"[", u"لأ", u"أ", u"ـ", u"،", u"/", u":", u"~", u"'"],
				[u"ْ", u"}", u"{", u"لآ", u"آ", u"’", u",", u".", u"؟", u":", u"_", u"CLEAR"],
				[u"SHIFT", u"SPACE", u"?", u"\\", u"=", u"ّ", u"~", u"OK"]]
			self.nextLang = 'cs_CZ'
		elif self.lang == 'cs_CZ':
			self.keys_list = [
				[u"EXIT", u"1", u"2", u"3", u"4", u"5", u"6", u"7", u"8", u"9", u"0", u"BACKSPACE"],
				[u"q", u"w", u"e", u"r", u"t", u"z", u"u", u"i", u"o", u"p", u"ú", u"+"],
				[u"a", u"s", u"d", u"f", u"g", u"h", u"j", u"k", u"l", u"ů", u"@", u"#"],
				[u"<", u"y", u"x", u"c", u"v", u"b", u"n", u"m", u",", ".", u"-", u"ALL"],
				[u"SHIFT", u"SPACE", u"ě", u"š", u"č", u"ř", u"ž", u"ý", u"á", u"í", u"é", u"OK"]]
			self.shiftkeys_list = [
				[u"EXIT", u"!", u'"', u"§", u"$", u"%", u"&", u"/", u"(", u")", u"=", u"BACKSPACE"],
				[u"Q", u"W", u"E", u"R", u"T", u"Z", u"U", u"I", u"O", u"P", u"ť", u"*"],
				[u"A", u"S", u"D", u"F", u"G", u"H", u"J", u"K", u"L", u"ň", u"ď", u"'"],
				[u">", u"Y", u"X", u"C", u"V", u"B", u"N", u"M", u";", u":", u"_", u"CLEAR"],
				[u"SHIFT", u"SPACE", u"?", u"\\", u"Č", u"Ř", u"Š", u"Ž", u"Ú", u"Á", u"É", u"OK"]]
			self.nextLang = 'de_DE'
		elif self.lang == 'de_DE':
			self.keys_list = [
				[u"EXIT", u"1", u"2", u"3", u"4", u"5", u"6", u"7", u"8", u"9", u"0", u"BACKSPACE"],
				[u"q", u"w", u"e", u"r", u"t", u"z", u"u", u"i", u"o", u"p", u"ü", u"+"],
				[u"a", u"s", u"d", u"f", u"g", u"h", u"j", u"k", u"l", u"ö", u"ä", u"#"],
				[u"<", u"y", u"x", u"c", u"v", u"b", u"n", u"m", u",", ".", u"-", u"ALL"],
				[u"SHIFT", u"SPACE", u"@", u"ß", u"OK", u"LEFT", u"RIGHT"]]
			self.shiftkeys_list = [
				[u"EXIT", u"!", u'"', u"§", u"$", u"%", u"&", u"/", u"(", u")", u"=", u"BACKSPACE"],
				[u"Q", u"W", u"E", u"R", u"T", u"Z", u"U", u"I", u"O", u"P", u"Ü", u"*"],
				[u"A", u"S", u"D", u"F", u"G", u"H", u"J", u"K", u"L", u"Ö", u"Ä", u"'"],
				[u">", u"Y", u"X", u"C", u"V", u"B", u"N", u"M", u";", u":", u"_", u"CLEAR"],
				[u"SHIFT", u"SPACE", u"?", u"\\", u"OK", u"LEFT", u"RIGHT"]]
			self.nextLang = 'el_GR'
		elif self.lang == 'el_GR':
			self.keys_list = [
				[u"EXIT", u"1", u"2", u"3", u"4", u"5", u"6", u"7", u"8", u"9", u"0", u"BACKSPACE"],
				[u"=", u"ς", u"ε", u"ρ", u"τ", u"υ", u"θ", u"ι", u"ο", u"π", u"[", u"]"],
				[u"α", u"σ", u"δ", u"φ", u"γ", u"η", u"ξ", u"κ", u"λ", u";", u"'", u"-"],
				[u"\\", u"ζ", u"χ", u"ψ", u"ω", u"β", u"ν", u"μ", u",", ".", u"/", u"ALL"],
				[u"SHIFT", u"SPACE", u"ά", u"έ", u"ή", u"ί", u"ό", u"ύ", u"ώ", u"ϊ", u"ϋ", u"OK"]]
			self.shiftkeys_list = [
				[u"EXIT", u"!", u"@", u"#", u"$", u"%", u"^", u"&", u"*", u"(", u")", u"BACKSPACE"],
				[u"+", u"€", u"Ε", u"Ρ", u"Τ", u"Υ", u"Θ", u"Ι", u"Ο", u"Π", u"{", u"}"],
				[u"Α", u"Σ", u"Δ", u"Φ", u"Γ", u"Η", u"Ξ", u"Κ", u"Λ", u":", u'"', u"_"],
				[u"|", u"Ζ", u"Χ", u"Ψ", u"Ω", u"Β", u"Ν", u"Μ", u"<", u">", u"?", u"CLEAR"],
				[u"SHIFT", u"SPACE", u"Ά", u"Έ", u"Ή", u"Ί", u"Ό", u"Ύ", u"Ώ", u"Ϊ", u"Ϋ", u"OK"]]
			self.nextLang = 'es_ES'
		elif self.lang == 'es_ES':
			#still missing keys (u"ùÙ")
			self.keys_list = [
				[u"EXIT", u"1", u"2", u"3", u"4", u"5", u"6", u"7", u"8", u"9", u"0", u"BACKSPACE"],
				[u"q", u"w", u"e", u"r", u"t", u"z", u"u", u"i", u"o", u"p", u"ú", u"+"],
				[u"a", u"s", u"d", u"f", u"g", u"h", u"j", u"k", u"l", u"ó", u"á", u"#"],
				[u"<", u"y", u"x", u"c", u"v", u"b", u"n", u"m", u",", ".", u"-", u"ALL"],
				[u"SHIFT", u"SPACE", u"@", u"Ł", u"ŕ", u"é", u"č", u"í", u"ě", u"ń", u"ň", u"OK"]]
			self.shiftkeys_list = [
				[u"EXIT", u"!", u'"', u"§", u"$", u"%", u"&", u"/", u"(", u")", u"=", u"BACKSPACE"],
				[u"Q", u"W", u"E", u"R", u"T", u"Z", u"U", u"I", u"O", u"P", u"Ú", u"*"],
				[u"A", u"S", u"D", u"F", u"G", u"H", u"J", u"K", u"L", u"Ó", u"Á", u"'"],
				[u">", u"Y", u"X", u"C", u"V", u"B", u"N", u"M", u";", u":", u"_", u"CLEAR"],
				[u"SHIFT", u"SPACE", u"?", u"\\", u"Ŕ", u"É", u"Č", u"Í", u"Ě", u"Ń", u"Ň", u"OK"]]
			self.nextLang = 'fa_IR'
		elif self.lang == 'fa_IR':
			self.keys_list = [
				[u"EXIT", u"\u06F1", u"\u06F2", u"\u06F3", u"\u06F4", u"\u06F5", u"\u06F6", u"\u06F7", u"\u06F8", u"\u06F9", u"\u06F0", u"BACKSPACE"],
				[u"\u0636", u"\u0635", u"\u062B", u"\u0642", u"\u0641", u"\u063A", u"\u0639", u"\u0647", u"\u062E", u"\u062D", u"-", u"\u062C"],
				[u"\u0634", u"\u0633", u"\u06CC", u"\u0628", u"\u0644", u"\u0627", u"\u062A", u"\u0646", u"\u0645", u"\u06A9", u"\u06AF", u"\u067E"],
				[u"<", u"\u0638", u"\u0637", u"\u0632", u"\u0631", u"\u0630", u"\u062F", u"\u0626", u"\u0648", ".", u"/", u"ALL"],
				[u"SHIFT", u"SPACE", u"OK", u"LEFT", u"RIGHT", u"*"]]
			self.shiftkeys_list = [
				[u"EXIT", u"!", u"@", u"#", u"$", u"%", u"^", u"&", u"(", u")", u"=", u"BACKSPACE"],
				[u"\u0636", u"\u0635", u"\u062B", u"\u0642", u"\u060C", u"\u061B", u"\u0639", u"\u0647", u"\u062E", u"\u062D", u"+", u"\u0686"],
				[u"\u0634", u"\u0633", u"\u06CC", u"\u0628", u"\u06C0", u"\u0622", u"\u062A", u"\u0646", u"\u0645", u"?", u'"', u"|"],
				[u">", u"\u0629", u"\u064A", u"\u0698", u"\u0624", u"\u0625", u"\u0623", u"\u0621", u";", u":", u"\u061F", u"CLEAR"],
				[u"SHIFT", u"SPACE", u"OK", u"LEFT", u"RIGHT", u"~"]]
			self.nextLang = 'fi_FI'
		elif self.lang == 'fi_FI':
			self.keys_list = [
				[u"EXIT", u"1", u"2", u"3", u"4", u"5", u"6", u"7", u"8", u"9", u"0", u"BACKSPACE"],
				[u"q", u"w", u"e", u"r", u"t", u"z", u"u", u"i", u"o", u"p", u"é", u"+"],
				[u"a", u"s", u"d", u"f", u"g", u"h", u"j", u"k", u"l", u"ö", u"ä", u"#"],
				[u"<", u"y", u"x", u"c", u"v", u"b", u"n", u"m", u",", ".", u"-", u"ALL"],
				[u"SHIFT", u"SPACE", u"@", u"ß", u"ĺ", u"OK", u"LEFT", u"RIGHT"]]
			self.shiftkeys_list = [
				[u"EXIT", u"!", u'"', u"§", u"$", u"%", u"&", u"/", u"(", u")", u"=", u"BACKSPACE"],
				[u"Q", u"W", u"E", u"R", u"T", u"Z", u"U", u"I", u"O", u"P", u"É", u"*"],
				[u"A", u"S", u"D", u"F", u"G", u"H", u"J", u"K", u"L", u"Ö", u"Ä", u"'"],
				[u">", u"Y", u"X", u"C", u"V", u"B", u"N", u"M", u";", u":", u"_", u"CLEAR"],
				[u"SHIFT", u"SPACE", u"?", u"\\", u"Ĺ", u"OK", u"LEFT", u"RIGHT"]]
			self.nextLang = 'fr_FR'
		elif self.lang == 'fr_FR':
			self.keys_list = [
				[u"EXIT", u"1", u"2", u"3", u"4", u"5", u"6", u"7", u"8", u"9", u"0", u"BACKSPACE"],
				[u"a", u"z", u"e", u"r", u"t", u"y", u"u", u"i", u"o", u"p", u"é", u"è"],
				[u"q", u"s", u"d", u"f", u"g", u"h", u"j", u"k", u"l", u"m", u"ê", u"ë"],
				[u"<", u"w", u"x", u"c", u"v", u"b", u"n", u",", u";", u":", u"=", u"ALL"],
				[u"SHIFT", u"SPACE", u"ù", u"â", u"ï", u"ô", u"ç", u"#", u"-", u"OK", u"LEFT", u"RIGHT"]]
			self.shiftkeys_list = [
				[u"EXIT", u"&", u'@', u'"', u"€", u"§", u"!", u"ç", u"(", u")", u"_", u"BACKSPACE"],
				[u"A", u"Z", u"E", u"R", u"T", u"Y", u"U", u"I", u"O", u"P", u"É", u"È"],
				[u"Q", u"S", u"D", u"F", u"G", u"H", u"J", u"K", u"L", u"M", u"Ê", u"Ë"],
				[u">", u"W", u"X", u"C", u"V", u"B", u"N", u"?", u".", u"+", u"~", u"CLEAR"],
				[u"SHIFT", u"SPACE", u"Ù", u"Â", u"Ï", u"Ô", u"°", u"/",u"\\", u"OK", u"LEFT", u"RIGHT"]]
			self.nextLang = 'lv_LV'
		elif self.lang == 'lv_LV':
			self.keys_list = [
				[u"EXIT", u"1", u"2", u"3", u"4", u"5", u"6", u"7", u"8", u"9", u"0", u"BACKSPACE"],
				[u"q", u"w", u"e", u"r", u"t", u"y", u"u", u"i", u"o", u"p", u"-", u"š"],
				[u"a", u"s", u"d", u"f", u"g", u"h", u"j", u"k", u"l", u";", u"'", u"ū"],
				[u"<", u"z", u"x", u"c", u"v", u"b", u"n", u"m", u",", u".", u"ž", u"ALL"],
				[u"SHIFT", u"SPACE", u"ā", u"č", u"ē", u"ģ", u"ī", u"ķ", u"ļ", u"ņ", u"LEFT", u"RIGHT"]]
			self.shiftkeys_list = [
				[u"EXIT", u"!", u"@", u"$", u"*", u"(", u")", u"_", u"=", u"/", u"\\", u"BACKSPACE"],
				[u"Q", u"W", u"E", u"R", u"T", u"Y", u"U", u"I", u"O", u"P", u"+", u"Š"],
				[u"A", u"S", u"D", u"F", u"G", u"H", u"J", u"K", u"L", u":", u'"', u"Ū"],
				[u">", u"Z", u"X", u"C", u"V", u"B", u"N", u"M", u"#", u"?", u"Ž", u"CLEAR"],
				[u"SHIFT", u"SPACE", u"Ā", u"Č", u"Ē", u"Ģ", u"Ī", u"Ķ", u"Ļ", u"Ņ", u"LEFT", u"RIGHT"]]
			self.nextLang = 'pl_PL'
		elif self.lang == 'pl_PL':
			self.keys_list = [
				[u"EXIT", u"1", u"2", u"3", u"4", u"5", u"6", u"7", u"8", u"9", u"0", u"BACKSPACE"],
				[u"q", u"w", u"e", u"r", u"t", u"y", u"u", u"i", u"o", u"p", u"-", u"["],
				[u"a", u"s", u"d", u"f", u"g", u"h", u"j", u"k", u"l", u";", u"'", u"\\"],
				[u"<", u"z", u"x", u"c", u"v", u"b", u"n", u"m", u",", ".", u"/", u"ALL"],
				[u"SHIFT", u"SPACE", u"ą", u"ć", u"ę", u"ł", u"ń", u"ó", u"ś", u"ź", u"ż", u"OK"]]
			self.shiftkeys_list = [
				[u"EXIT", u"!", u"@", u"#", u"$", u"%", u"^", u"&", u"(", u")", u"=", u"BACKSPACE"],
				[u"Q", u"W", u"E", u"R", u"T", u"Y", u"U", u"I", u"O", u"P", u"*", u"]"],
				[u"A", u"S", u"D", u"F", u"G", u"H", u"J", u"K", u"L", u"?", u'"', u"|"],
				[u">", u"Z", u"X", u"C", u"V", u"B", u"N", u"M", u";", u":", u"_", u"CLEAR"],
				[u"SHIFT", u"SPACE", u"Ą", u"Ć", u"Ę", u"Ł", u"Ń", u"Ó", u"Ś", u"Ź", u"Ż", u"OK"]]
			self.nextLang = 'ru_RU'
		elif self.lang == 'ru_RU':
			self.keys_list = [
				[u"EXIT", u"1", u"2", u"3", u"4", u"5", u"6", u"7", u"8", u"9", u"0", u"BACKSPACE"],
				[u"а", u"б", u"в", u"г", u"д", u"е", u"ё", u"ж", u"з", u"и", u"й", u"+"],
				[u"к", u"л", u"м", u"н", u"о", u"п", u"р", u"с", u"т", u"у", u"ф", u"#"],
				[u"<", u"х", u"ц", u"ч", u"ш", u"щ", u"ъ", u"ы", u",", u".", u"-", u"ALL"],
				[u"SHIFT", u"SPACE", u"@", u"ь", u"э", u"ю", u"я", u"OK", u"LEFT", u"RIGHT"]]
			self.shiftkeys_list = [
				[u"EXIT", u"!", u'"', u"§", u"$", u"%", u"&", u"/", u"(", u")", u"=", u"BACKSPACE"],
				[u"А", u"Б", u"В", u"Г", u"Д", u"Е", u"Ё", u"Ж", u"З", u"И", u"Й", u"*"],
				[u"К", u"Л", u"М", u"Н", u"О", u"П", u"Р", u"С", u"Т", u"У", u"Ф", u"'"],
				[u">", u"Х", u"Ц", u"Ч", u"Ш", u"Щ", u"Ъ", u"Ы", u";", u":", u"_", u"CLEAR"],
				[u"SHIFT", u"SPACE", u"?", u"\\", u"Ь", u"Э", u"Ю", u"Я", u"OK", u"LEFT", u"RIGHT"]]
			self.nextLang = 'sk_SK'
		elif self.lang =='sk_SK':
			self.keys_list = [
				[u"EXIT", u"1", u"2", u"3", u"4", u"5", u"6", u"7", u"8", u"9", u"0", u"BACKSPACE"],
				[u"q", u"w", u"e", u"r", u"t", u"z", u"u", u"i", u"o", u"p", u"ú", u"+"],
				[u"a", u"s", u"d", u"f", u"g", u"h", u"j", u"k", u"l", u"ľ", u"@", u"#"],
				[u"<", u"y", u"x", u"c", u"v", u"b", u"n", u"m", u",", ".", u"-", u"ALL"],
				[u"SHIFT", u"SPACE", u"š", u"č", u"ž", u"ý", u"á", u"í", u"é", u"OK", u"LEFT", u"RIGHT"]]
			self.shiftkeys_list = [
				[u"EXIT", u"!", u'"', u"§", u"$", u"%", u"&", u"/", u"(", u")", u"=", u"BACKSPACE"],
				[u"Q", u"W", u"E", u"R", u"T", u"Z", u"U", u"I", u"O", u"P", u"ť", u"*"],
				[u"A", u"S", u"D", u"F", u"G", u"H", u"J", u"K", u"L", u"ň", u"ď", u"'"],
				[u"Á", u"É", u"Ď", u"Í", u"Ý", u"Ó", u"Ú", u"Ž", u"Š", u"Č", u"Ť", u"Ň"],
				[u">", u"Y", u"X", u"C", u"V", u"B", u"N", u"M", u";", u":", u"_", u"CLEAR"],
				[u"SHIFT", u"SPACE", u"?", u"\\", u"ä", u"ö", u"ü", u"ô", u"ŕ", u"ĺ", u"OK"]]
			self.nextLang = 'sv_SE'
		elif self.lang == 'sv_SE':
			self.keys_list = [
				[u"EXIT", u"1", u"2", u"3", u"4", u"5", u"6", u"7", u"8", u"9", u"0", u"BACKSPACE"],
				[u"q", u"w", u"e", u"r", u"t", u"z", u"u", u"i", u"o", u"p", u"é", u"+"],
				[u"a", u"s", u"d", u"f", u"g", u"h", u"j", u"k", u"l", u"ö", u"ä", u"#"],
				[u"<", u"y", u"x", u"c", u"v", u"b", u"n", u"m", u",", ".", u"-", u"ALL"],
				[u"SHIFT", u"SPACE", u"@", u"ß", u"ĺ", u"OK", u"LEFT", u"RIGHT"]]
			self.shiftkeys_list = [
				[u"EXIT", u"!", u'"', u"§", u"$", u"%", u"&", u"/", u"(", u")", u"=", u"BACKSPACE"],
				[u"Q", u"W", u"E", u"R", u"T", u"Z", u"U", u"I", u"O", u"P", u"É", u"*"],
				[u"A", u"S", u"D", u"F", u"G", u"H", u"J", u"K", u"L", u"Ö", u"Ä", u"'"],
				[u">", u"Y", u"X", u"C", u"V", u"B", u"N", u"M", u";", u":", u"_", u"CLEAR"],
				[u"SHIFT", u"SPACE", u"?", u"\\", u"Ĺ", u"OK", u"LEFT", u"RIGHT"]]
			self.nextLang = 'th_TH'
		elif self.lang == 'th_TH':
			self.keys_list = [[u"EXIT", "\xe0\xb9\x85", "\xe0\xb8\xa0", "\xe0\xb8\x96", "\xe0\xb8\xb8", "\xe0\xb8\xb6", "\xe0\xb8\x84", "\xe0\xb8\x95", "\xe0\xb8\x88", "\xe0\xb8\x82", "\xe0\xb8\x8a", u"BACKSPACE"],
				["\xe0\xb9\x86", "\xe0\xb9\x84", "\xe0\xb8\xb3", "\xe0\xb8\x9e", "\xe0\xb8\xb0", "\xe0\xb8\xb1", "\xe0\xb8\xb5", "\xe0\xb8\xa3", "\xe0\xb8\x99", "\xe0\xb8\xa2", "\xe0\xb8\x9a", "\xe0\xb8\xa5"],
				["\xe0\xb8\x9f", "\xe0\xb8\xab", "\xe0\xb8\x81", "\xe0\xb8\x94", "\xe0\xb9\x80", "\xe0\xb9\x89", "\xe0\xb9\x88", "\xe0\xb8\xb2", "\xe0\xb8\xaa", "\xe0\xb8\xa7", "\xe0\xb8\x87", "\xe0\xb8\x83"],
				["\xe0\xb8\x9c", "\xe0\xb8\x9b", "\xe0\xb9\x81", "\xe0\xb8\xad", "\xe0\xb8\xb4", "\xe0\xb8\xb7", "\xe0\xb8\x97", "\xe0\xb8\xa1", "\xe0\xb9\x83", "\xe0\xb8\x9d", "", u"ALL"],
				[u"SHIFT", u"SPACE", u"OK", u"LEFT", u"RIGHT"]]
			self.shiftkeys_list = [[u"EXIT", "\xe0\xb9\x91", "\xe0\xb9\x92", "\xe0\xb9\x93", "\xe0\xb9\x94", "\xe0\xb8\xb9", "\xe0\xb9\x95", "\xe0\xb9\x96", "\xe0\xb9\x97", "\xe0\xb9\x98", "\xe0\xb9\x99", u"BACKSPACE"],
				["\xe0\xb9\x90", "", "\xe0\xb8\x8e", "\xe0\xb8\x91", "\xe0\xb8\x98", "\xe0\xb9\x8d", "\xe0\xb9\x8a", "\xe0\xb8\x93", "\xe0\xb8\xaf", "\xe0\xb8\x8d", "\xe0\xb8\x90", "\xe0\xb8\x85"],
				["\xe0\xb8\xa4", "\xe0\xb8\x86", "\xe0\xb8\x8f", "\xe0\xb9\x82", "\xe0\xb8\x8c", "\xe0\xb9\x87", "\xe0\xb9\x8b", "\xe0\xb8\xa9", "\xe0\xb8\xa8", "\xe0\xb8\x8b", "", "\xe0\xb8\xbf"],
				["", "", "\xe0\xb8\x89", "\xe0\xb8\xae", "\xe0\xb8\xba", "\xe0\xb9\x8c", "", "\xe0\xb8\x92", "\xe0\xb8\xac", "\xe0\xb8\xa6", "", u"CLEAR"],
				[u"SHIFT", u"SPACE", u"OK", u"LEFT", u"RIGHT"]]
			self.nextLang = 'en_EN'
		else:
			self.keys_list = [
				[u"EXIT", u"1", u"2", u"3", u"4", u"5", u"6", u"7", u"8", u"9", u"0", u"BACKSPACE"],
				[u"q", u"w", u"e", u"r", u"t", u"y", u"u", u"i", u"o", u"p", u"-", u"["],
				[u"a", u"s", u"d", u"f", u"g", u"h", u"j", u"k", u"l", u";", u"'", u"\\"],
				[u"<", u"z", u"x", u"c", u"v", u"b", u"n", u"m", u",", ".", u"/", u"ALL"],
				[u"SHIFT", u"SPACE", u"OK", u"LEFT", u"RIGHT", u"*"]]
			self.shiftkeys_list = [
				[u"EXIT", u"!", u"@", u"#", u"$", u"%", u"^", u"&", u"(", u")", u"=", u"BACKSPACE"],
				[u"Q", u"W", u"E", u"R", u"T", u"Y", u"U", u"I", u"O", u"P", u"+", u"]"],
				[u"A", u"S", u"D", u"F", u"G", u"H", u"J", u"K", u"L", u"?", u'"', u"|"],
				[u">", u"Z", u"X", u"C", u"V", u"B", u"N", u"M", u";", u":", u"_", u"CLEAR"],
				[u"SHIFT", u"SPACE", u"OK", u"LEFT", u"RIGHT", u"~"]]
			self.lang = 'en_EN'
			self.nextLang = 'ar_AE'
		self["country"].setText(self.lang)
		self.max_key=47+len(self.keys_list[4])

	def buildVirtualKeyBoard(self, selectedKey=0):
		list = []
		
		if self.shiftMode:
			self.k_list = self.shiftkeys_list
			for keys in self.k_list:
				if selectedKey < 12 and selectedKey > -1:
					list.append(VirtualKeyBoardEntryComponent(keys, selectedKey,True))
				else:
					list.append(VirtualKeyBoardEntryComponent(keys, -1,True))
				selectedKey -= 12
		else:
			self.k_list = self.keys_list
			for keys in self.k_list:
				if selectedKey < 12 and selectedKey > -1:
					list.append(VirtualKeyBoardEntryComponent(keys, selectedKey))
				else:
					list.append(VirtualKeyBoardEntryComponent(keys, -1))
				selectedKey -= 12
		
		self["list"].setList(list)
	
	def backClicked(self):
		self["text"].deleteBackward()

	def forwardClicked(self):
		self["text"].deleteForward()

	def shiftClicked(self):
		self.smsChar = None
		self.shiftMode = not self.shiftMode
		self.buildVirtualKeyBoard(self.selectedKey)

	def okClicked(self):
		self.smsChar = None
		text = (self.shiftMode and self.shiftkeys_list or self.keys_list)[self.selectedKey / 12][self.selectedKey % 12].encode("UTF-8")

		if text == "EXIT":
			self.close(None)

		elif text == "BACKSPACE":
			self["text"].deleteBackward()

		elif text == "ALL":
			self["text"].markAll()

		elif text == "CLEAR":
			self["text"].deleteAllChars()
			self["text"].update()

		elif text == "SHIFT":
			self.shiftClicked()

		elif text == "SPACE":
			self["text"].char(" ".encode("UTF-8"))

		elif text == "OK":
			self.close(self["text"].getText())

		elif text == "LEFT":
			self["text"].left()

		elif text == "RIGHT":
			self["text"].right()

		else:
			self["text"].char(text)

	def ok(self):
		self.close(self["text"].getText())

	def exit(self):
		self.close(None)

	def cursorRight(self):
		self["text"].right()

	def cursorLeft(self):
		self["text"].left()

	def left(self):
		self.smsChar = None
		self.selectedKey -= 1
		if self.selectedKey == -1:
			self.selectedKey = 11
		elif self.selectedKey == 11:
			self.selectedKey = 23
		elif self.selectedKey == 23:
			self.selectedKey = 35
		elif self.selectedKey == 35:
			self.selectedKey = 47
		elif self.selectedKey == 47:
			self.selectedKey = self.max_key
		
		self.showActiveKey()

	def right(self):
		self.smsChar = None
		self.selectedKey += 1
		if self.selectedKey == 12:
			self.selectedKey = 0
		elif self.selectedKey == 24:
			self.selectedKey = 12
		elif self.selectedKey == 36:
			self.selectedKey = 24
		elif self.selectedKey == 48:
			self.selectedKey = 36
		elif self.selectedKey > self.max_key:
			self.selectedKey = 48
		self.showActiveKey()

	def up(self):
		self.smsChar = None
		self.selectedKey -= 12
		if (self.selectedKey < 0) and (self.selectedKey > (self.max_key-60)):
			self.selectedKey += 48
		elif self.selectedKey < 0:
			self.selectedKey += 60	
		self.showActiveKey()

	def down(self):
		self.smsChar = None
		self.selectedKey += 12
		if (self.selectedKey > self.max_key) and (self.selectedKey > 59):
			self.selectedKey -= 60
		elif self.selectedKey > self.max_key:
			self.selectedKey -= 48
		self.showActiveKey()

	def showActiveKey(self):
		self.buildVirtualKeyBoard(self.selectedKey)

	def keyNumberGlobal(self, number):
		self.smsChar = self.sms.getKey(number)
		print "SMS", number, self.smsChar
		self.selectAsciiKey(self.smsChar)

	def smsOK(self):
		print "SMS ok", self.smsChar
		if self.smsChar and self.selectAsciiKey(self.smsChar):
			print "pressing ok now"
			self.okClicked()

	def keyGotAscii(self):
		self.smsChar = None
		if self.selectAsciiKey(str(unichr(getPrevAsciiCode()).encode('utf-8'))):
			self.okClicked()

	def selectAsciiKey(self, char):
		if char == " ":
			char = "SPACE"
		for keyslist in (self.shiftkeys_list, self.keys_list):
			selkey = 0
			for keys in keyslist:
				for key in keys:
					if key == char:
						self.shiftMode = (keyslist is self.shiftkeys_list)
						self.selectedKey = selkey
						self.showActiveKey()
						return True
					selkey += 1
		return False