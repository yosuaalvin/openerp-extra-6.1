# -*- encoding: utf-8 -*-
##############################################################################
#
#    ETL system- Extract Transfer Load system
#    Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>). All Rights Reserved
#    $Id$
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
"""
 To write data into open object model.

 Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>).
 GNU General Public License.
"""
from etl.component.output.openobject_out import openobject_out
import datetime

class openobject_out_copy(openobject_out):
    """
    This is an ETL Component that writes data in open object model.

    Type                  : Data Component.
    Computing Performance : Streamline.
    Fields                : A mapping {OpenObject Field Name : Flow Name}.
    Input Flows           : 0-x.
    * .*                  : The main data flow with input data.
    Output Flows          : 0-1.
    * main                : Returns all data.
    """

    def __init__(self, openobject_connector, model, fields=[], key='id', new_key='new_id', name='component.output.openobject_out_copy', transformer=None, row_limit=0,raw_copy=True):
        """
        Parameters
        openobject_connector : Open object connector to connect with OpenERP server.
        model                : Open object model name.

        Extra Parameters
        name                 : Name of Component.
        transformer          : Transformer object to transform string data into particular object.
        fields               : Fields of open object model.
        model                : Open object model name.
        """
        super(openobject_out_copy, self).__init__(openobject_connector, model, fields=fields, name=name, transformer=transformer, row_limit=row_limit)
        self._type = 'component.output.openobject_out_copy'
        self.key = key
        self.new_key = new_key
        self.raw_copy = raw_copy

    def process(self):
        datas = []
        self.fields_keys = None
        self.op_oc = False
        for channel, trans in self.input_get().items():
            for iterator in trans:
                for d in iterator:    
                    if not self.fields:
                        self.fields = dict(map(lambda x: (x, x), d.keys()))
                    if type(self.fields) == type([]):
                        self.fields_keys = self.fields
                        self.fields = dict(map(lambda x: (x, x), self.fields))
                    if not self.fields_keys:
                        self.fields_keys = self.fields.keys()
                    if self.raw_copy:
                        values = {}
                    else:
                        values = dict(map(lambda x: (x,d[self.fields[x]]), self.fields_keys))
                    op_oc = self.connector.open()
                    res = self.connector.execute(op_oc, 'execute', self.model, 'copy', d[self.key], values)
                    self.connector.close(op_oc)
                    d.update({self.new_key:res})
                    yield d, 'main'

def test():
    pass

if __name__ == '__main__':
    test()

