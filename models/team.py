# -*- coding: utf-8 -*-
##############################################################################
#
#    @package league Leagues Management for Odoo 8.0
#    @copyright Copyright (C) 2015 Leo Tran (leotran.hpvn@gmail.com). All rights reserved.#
#    @license http://www.gnu.org/licenses GNU Affero General Public License version 3 or later; see LICENSE.txt
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
from openerp import models, fields

class team(models.Model):
    _name = 'team'
    _description = 'Team'
    
    name = fields.Char(string='Name', size=128, required=True)
    image = fields.Binary(string='Photo')
    country_id = fields.Many2one('res.country', string='Country', required=True)
    
class res_partner(models.Model):
    _inherit = 'res.partner'
    
    football_player = fields.Boolean(string="Football Player")