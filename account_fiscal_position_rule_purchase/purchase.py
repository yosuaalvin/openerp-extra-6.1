# -*- encoding: utf-8 -*-
#################################################################################
#
#    Copyright (C) 2010  Renato Lima - Akretion
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
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
#################################################################################

from osv import fields, osv

class purchase_order(osv.osv):
    _inherit = 'purchase.order'
    
    def onchange_partner_id(self, cr, uid, ids, part, company_id=False):
        
        result = super(purchase_order, self ).onchange_partner_id(cr, uid, ids, part)
        
        if not part or not company_id or not result['value']['partner_address_id']:
            return result

        obj_company = self.pool.get('res.company').browse(cr, uid, company_id)

        company_addr = self.pool.get('res.partner').address_get(cr, uid, [obj_company.partner_id.id], ['default'])
        company_addr_default = self.pool.get('res.partner.address').browse(cr, uid, company_addr['default'])

        from_country = company_addr_default.country_id.id
        from_state = company_addr_default.state_id.id

        obj_partner = self.pool.get('res.partner').browse(cr, uid, part)
        if obj_partner.property_account_position:
            result['value']['fiscal_position'] = obj_partner.property_account_position.id
            return result
        
        partner_addr_default = self.pool.get('res.partner.address').browse(cr, uid, [result['value']['partner_address_id']])[0]

        to_country = partner_addr_default.country_id.id
        to_state = partner_addr_default.state_id.id

        fsc_pos_id = self.pool.get('account.fiscal.position.rule').search(cr, uid, ['&',('company_id','=',company_id),('use_purchase','=',True), '|',('from_country','=',from_country),('from_country','=',False),'|',('to_country','=',to_country), ('to_country','=',False),'|',('from_state','=',from_state),('from_state','=',False),'|',('to_state','=',to_state),('to_state','=',False)])

        if fsc_pos_id:
            obj_fpo_rule = self.pool.get('account.fiscal.position.rule').read(cr, uid, fsc_pos_id, ['fiscal_position_id'])
            result['value']['fiscal_position'] = obj_fpo_rule[0]['fiscal_position_id']

        return result

    def onchange_partner_address_id(self, cr, uid, ids, partner_address_id, company_id=False):

        result = {'value': {}}

        if not partner_address_id or not company_id:
	    result = {'value': {'fiscal_position': False}}
            return result

        obj_company = self.pool.get('res.company').browse(cr, uid, company_id)

        company_addr = self.pool.get('res.partner').address_get(cr, uid, [obj_company.partner_id.id], ['default'])
        company_addr_default = self.pool.get('res.partner.address').browse(cr, uid, [company_addr['default']])[0]

        from_country = company_addr_default.country_id.id
        from_state = company_addr_default.state_id.id
        
        partner_addr_default = self.pool.get('res.partner.address').browse(cr, uid, [partner_address_id])[0]

        obj_partner = self.pool.get('res.partner').browse(cr, uid, [partner_addr_default.partner_id.id])[0]
        if obj_partner.property_account_position:
            result['value']['fiscal_position'] = obj_partner.property_account_position.id
            return result

        to_country = partner_addr_default.country_id.id
        to_state = partner_addr_default.state_id.id

        fsc_pos_id = self.pool.get('account.fiscal.position.rule').search(cr, uid, ['&',('company_id','=',company_id),('use_purchase','=',True),'|',('from_country','=',from_country),('from_country','=',False),'|',('to_country','=',to_country),('to_country','=',False),'|',('from_state','=',from_state),('from_state','=',False),'|',('to_state','=',to_state),('to_state','=',False)])
        
        if fsc_pos_id:
            obj_fpo_rule = self.pool.get('account.fiscal.position.rule').read(cr, uid, fsc_pos_id,['fiscal_position_id'])
            result['value']['fiscal_position'] = obj_fpo_rule[0]['fiscal_position_id']
            
        return result

purchase_order()
