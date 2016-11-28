
# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
def strip_or_none(val):
	if val is None: return None
	if isinstance(val, basestring):
		val = val.strip()
		if val=="": return None
	return val


def doc_type_equivalences(doc_type):
	if doc_type==1:
		return "DNI"
	elif doc_type==2:
		return "LE"
	elif doc_type==3:
		return "LC"
	elif doc_type==6:
		return "CUIT"
	elif doc_type==7:
		return "PAS"
	else:
		return None

def doc_number_normalize(doc_type, number):
	try:
		number=int(number)
	except:
		number = None

	if (number<=1111) or "11111" in str(number) or number is None or doc_type is None:
		dt=None
		d=None
	else:
		dt = doc_type_equivalences(doc_type)
		d=number
	return (dt,d)