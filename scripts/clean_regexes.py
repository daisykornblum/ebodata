import re

"""Set up regular expressions for parts of sentences to strip"""
email_addresses_regex = re.compile(ur'[A-Za-z0-9\.]+@[A-Za-z]+[A-Za-z0-9\.]+', re.UNICODE)
username_regex =  re.compile(ur'@[A-Za-z]+[A-Za-z0-9_\.]+', re.UNICODE)
rt_regex =  re.compile(ur'RT', re.UNICODE)
embedded_url_regex =  re.compile(ur'http:\/\/[A-Za-z0-9\.\/]+', re.UNICODE)
punctuation_regex =  re.compile(ur'[\.,\*\&\^\%\$£!\?\":;\#\+=\-_\'\|]+', re.UNICODE)

EMOTICONS = { # (facial expression, sentiment)-keys
("love" , +1.00): set(("<3", u"♥", u"❤")),
("grin" , +1.00): set((">:D", ":-D", ":D", "=-D", "=D", "X-D", "x-D", "XD", "xD", "8-D")),
("taunt", +0.75): set((">:P", ":-P", ":P", ":-p", ":p", ":-b", ":b", ":c)", ":o)", ":^)")),
("smile", +0.50): set((">:)", ":-)", ":)", "=)", "=]", ":]", ":}", ":>", ":3", "8)", "8-)")),
("wink" , +0.25): set((">;]", ";-)", ";)", ";-]", ";]", ";D", ";^)", "*-)", "*)")),
("blank", +0.00): set((":-|", ":|")),
("gasp" , -0.05): set((">:o", ":-O", ":O", ":o", ":-o", "o_O", "o.O", u"°O°", u"°o°")),
("worry", -0.25): set((">:/", ":-/", ":/", ":\\", ">:\\", ":-.", ":-s", ":s", ":S", ":-S", ">.>")),
("frown", -0.75): set((">:[", ":-(", ":(", "=(", ":-[", ":[", ":{", ":-<", ":c", ":-c", "=/")),
("cry" , -1.00): set((":'(", ":'''(", ";'("))
}
RE_EMOTICONS = [r" ?".join(map(re.escape, e)) for v in EMOTICONS.values() for e in v]
RE_EMOTICONS = re.compile(r"(%s)($|\s)" % "|".join(RE_EMOTICONS))

# Common emoji.
EMOJI = { # (facial expression, sentiment)-keys
("love" , +1.00): set((u"❤️", u"💜", u"💚", u"💙", u"💛", u"💕")),
("grin" , +1.00): set((u"😀", u"😄", u"😃", u"😆", u"😅", u"😂", u"😁", u"😻", u"😍", u"😈", u"👌")),
("taunt", +0.75): set((u"😛", u"😝", u"😜", u"😋", u"😇")),
("smile", +0.50): set((u"😊", u"😌", u"😏", u"😎", u"☺", u"👍")),
("wink" , +0.25): set((u"😉")),
("blank", +0.00): set((u"😐", u"😶")),
("gasp" , -0.05): set((u"😳", u"😮", u"😯", u"😧", u"😦", u"🙀")),
("worry", -0.25): set((u"😕", u"😬")),
("frown", -0.75): set((u"😟", u"😒", u"😔", u"😞", u"😠", u"😩", u"😫", u"😡", u"👿")),
("cry" , -1.00): set((u"😢", u"😥", u"😓", u"😪", u"😭", u"😿")),
("misc" , -1.00): set((u"🍕",)),
}
RE_EMOJI = [e for v in EMOJI.values() for e in v]
RE_EMOJI = re.compile(r"(\s?)(%s)(\s?)" % "|".join(RE_EMOJI))