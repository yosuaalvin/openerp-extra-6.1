# -*- encoding: utf-8 -*-
##############################################################################
#    
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.     
#
##############################################################################

{
    "name": "Lunch Module",
    "author": "Tiny",
    "version": "0.1",
    "depends": ["base"],
    "category" : "Generic Modules/Others",
    "init_xml": [],
    "update_xml": [
        'security/ir.model.access.csv', 
        'lunch_wizard.xml', 
        'lunch_view.xml', 
        'lunch_report.xml',
        #'process/lunch_process.xml'
    ],
    "demo_xml": ['lunch_demo.xml'],
    "installable": True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

