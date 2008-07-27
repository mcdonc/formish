from formish.converter import *
from webhelpers.html import literal
from restish.templating import render

# Marker object for args that are not supplied
_UNSET = object()

class Widget(object):
    
    def pre_render(self, schemaType, data):
        return string_converter(schemaType).fromType(data)

    # ??: Should the validate be here? Confused
    def validate(self, data):
        errors = None
        return data, errors

    def convert(self, schemaType, data):
        return string_converter(schemaType).toType(data)    
    
    def __call__(self, field):
        return literal(render(field.form.request, "formish/widgets/default.html", {'widget': self, 'field': field}))

class Input(Widget):
    
    def pre_render(self, schemaType, data):
        return string_converter(schemaType).fromType(data)
    
    def convert(self, schemaType, data):
        return string_converter(schemaType).toType(data)
    
    def __call__(self, field):
        return literal(render(field.form.request, "formish/widgets/input.html", {'widget': self, 'field': field}))
    
class TextArea(Widget):
    
    def __init__(self, cols=None, rows=None):
        if cols is not None:
            self.cols = cols
        if rows is not None:
            self.rows = rows 
            
    def pre_render(self, schemaType, data):
        return string_converter(schemaType).fromType(data)
    
    def convert(self, schemaType, data):
        return string_converter(schemaType).toType(data)            
            
    def __call__(self, form, field):
        return literal(render(form.request, "formish/widgets/textarea.html", {'widget': self, 'field': field}))
    
class Checkbox(Widget):

    def pre_render(self, schemaType, data):
        return boolean_converter(schemaType).fromType(data)
    
    def convert(self, schemaType, data):
        return boolean_converter(schemaType).toType(data)            
            
    def __call__(self, form, field):
        if field.value is True:
            checked = 'checked="checked"'
        return literal(render(form.request, "formish/widgets/checkbox.html", {'widget': self, 'field': field, 'checked': checked}))    
    
class DateParts(Widget):
    
    def pre_render(self, schemaType, data):
        data = datetuple_converter(schemaType).fromType(data)
        d = {}
        d['year'] = data[0]
        d['month'] = data[1]
        d['day'] = data[2]
        return d
    
    def convert(self, schemaType, data):
        year = data.get('year', '')
        month = data.get('month', '')
        day = data.get('day', '')
        return datetuple_converter(schemaType).toType((year, month, day))
    
    def __call__(self, field):
        return literal(render(field.form.request, "formish/widgets/dateparts.html", {'widget': self, 'field': field}))
    
    
class Select(Widget):

    def __init__(self, options, noneOption=None):
        self.options = options
        self.noneOption = noneOption
            
    def pre_render(self, schemaType, data):
        return string_converter(schemaType).fromType(data)
    
    def convert(self, schemaType, data):
        return string_converter(schemaType).toType(data)

    def selected(self, option, value):
        if option[0] == value:
            return ' selected="selected"'
    
    def __call__(self, field):
        return literal(render(field.form.request, "formish/widgets/select.html", {'widget': self, 'field': field, 'options': self.options, 'noneOption': self.noneOption}))

 
class BoundWidget(object):
    
    def __init__(self, widget, field):
        self.widget = widget
        self.field = field
        
    def __call__(self):
        return self.widget(self.field)
    
    def pre_render(self, schemaType, data):
        return self.widget.pre_render(schemaType, data)

    def convert(self, schemaType, data):
        return self.widget.convert(schemaType, data)
        
    def validate(self, data):
        return self.widget.validate(data)
    