#!/usr/bin/env python
import sys
import ctypes

def EnumFactory(cls):
	classname = cls.__name__
	class MetaEnum(type(cls)):
		def __new__(cls, name, bases, dct):
			items = dct.pop("_members_", None)
			if not items:
				items = dict(filter(lambda x: not str(x[0]).startswith("__"), dct.items()))
			else:
				if type(items) in [list, tuple]:
					start = dct.pop("startwith", 0)
					items = dict([(x[1], x[0]) for x in enumerate(items, start = start)])
				dct.update(items)
			dct["_items"] = items
			dct["_rev"] = dict(zip(items.values(), items.keys()))

			module = sys.modules[dct["__module__"]]
			for key,value in items.items():
				setattr(module, key, value)

			return super(MetaEnum, cls).__new__(cls, name, bases, dct)

		def __call__(self, value, *args, **kwargs):
			if isinstance(value, basestring):
				if not hasattr(self, value):
					raise KeyError(u"No enumeration member with name %s" % value)

				name = value
				value = getattr(self, value)
			elif value not in self._items.values():
				raise ValueError("No enumeration member with value %r" % value)
			else:
				name = self._rev[value]
			res = super(MetaEnum, self).__call__(value, *args, **kwargs)
			res.name = name
			return res

		def __contains__(self, value):
			return value in self._items.values()

		def __repr__(self):
			return "<Enum [%s] %s: %s>" % (cls.__name__, self.__name__, str(self._items.keys()), )

	class Enum(cls):
		__metaclass__ = MetaEnum

		def get_value(self):
			if hasattr(self, "value"):
				return self.value
			return self

		def get_name(self):
			name = getattr(self, "name", None)
			value = self.get_value()
			if name and self._items[name] == value:
				return name
			return self._rev[value]

		def __repr__(self):
			return "<Enum [%s] %s: %s = %s (%s)>" % (cls.__name__, self.__class__.__name__, str(self._items.keys()), str(self.get_value()), self.get_name())

	return Enum

Enum = EnumFactory(ctypes.c_uint32)
