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
{
    'name' : 'Leagues Management',
    'version': '1.0',
    'author' : 'Leo Tran (leotran.hpvn@gmail.com)',
    'website': 'http://openerpdev.com',
    'summary': 'Leagues Management',    
    'category': 'Leagues',
    'sequence': 1,    
    'description':"""
Leagues Management
==================
    """,
    'depends': ['base', 'mail'],
    'data': [
         'data/module_data.xml',
         'data/league_data.xml',
         'data/team_data.xml',   
         'security/league_security.xml',
         'security/ir.model.access.csv',
         'views/league_view.xml',
         'views/team_view.xml',
         'views/league_season_view.xml',
         'views/fixture_view.xml',      
    ],
    'installable': True,
    'application': True,    
}