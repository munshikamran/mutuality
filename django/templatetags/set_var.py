from django import template
from django.conf import settings
from django.utils import formats
 
register = template.Library()
 
class SetVarNode(template.Node):
 
	def __init__(self, var_name, var_value):
		self.var_name = var_name
		self.var_value = var_value
 
	def render(self, context):
		try:
			first_pipe = self.var_value.find("|", 0, len(self.var_value))
			if first_pipe != -1:
				value = template.Variable(self.var_value[:first_pipe].strip()).resolve(context)
				arg = self.var_value[first_pipe+1:].strip()
				x = arg.find(":", 0, len(arg))
				if x > 0:
					format = arg[x+1:].strip()
					arg = arg[:x].strip()
				if arg == "length":
					value = len(value)
				elif arg == "increment":
					value = value+1
				elif arg == "date":
					value = date_format(value,format)
			else:
				value = template.Variable(self.var_value).resolve(context)
		except template.VariableDoesNotExist:
			value = ""
		context[self.var_name] = value
		return u""
 
def set_var(parser, token):
	"""
		{% set <var_name>  = <var_value> %}
	"""
	parts = token.split_contents()
	if len(parts) < 4:
		raise template.TemplateSyntaxError("'set' tag must be of the form:  {% set <var_name>  = <var_value> %}")
	return SetVarNode(parts[1], parts[3])
	
def date_format(value, arg=None):
	"""Formats a date according to the given format."""
	from django.utils.dateformat import format
	if not value:
		return u''
	if arg is None:
		arg = settings.DATE_FORMAT
	try:
		return formats.date_format(value, arg)
	except AttributeError:
		try:
			return format(value, arg)
		except AttributeError:
			return ''
 
register.tag('set', set_var)