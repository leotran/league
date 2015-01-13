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
from openerp import models, fields, api, _

class fixture_month(models.Model):
    _name = 'fixture.month'
    
    name = fields.Char(string="Month", required=True)
    
class fixture_player(models.Model):
    _name = 'fixture.player'
    
    fixture_id = fields.Many2one('fixture', string="Fixture", ondelete='restrict')
    player_id = fields.Many2one('league.season.player', string="Player", required=True)
    goal = fields.Integer(string="Goals", default=0)
    home = fields.Boolean(string="Home")
    
    _sql_constraints = [
        ('player_uniq', 'unique(fixture_id,player_id)',
            'Player must be unique per fixture!'),
    ]    

class fixture(models.Model):
    _name = 'fixture'
    _description = 'Fixture'
    _inherit = ['mail.thread']
    
    league_season_id = fields.Many2one('league.season', string='Season', 
       domain=[('state','=','open')], reqruied=True, 
       readonly=True, states={'draft': [('readonly', False)]})
    league_id = fields.Many2one('league', string='League',
        related='league_season_id.league_id', store=True,
        readonly=True, states={'draft': [('readonly', False)]})
    season_id = fields.Many2one('season', string='Season',
        related='league_season_id.season_id', store=True,
        readonly=True, states={'draft': [('readonly', False)]})
    month_id = fields.Many2one('fixture.month', string="Month")
    datetime = fields.Date(string='Datetime',
        readonly=True, states={'draft': [('readonly', False)]})
    team_home_id = fields.Many2one('league.season.team', string='Home', required=True,
        readonly=True, states={'draft': [('readonly', False)]})
    player_home_ids = fields.One2many('fixture.player', 'fixture_id', string="Home Players", domain=[('home','=',True)])
    team_away_id = fields.Many2one('league.season.team', string='Away', required=True,
        readonly=True, states={'draft': [('readonly', False)]})
    player_away_ids = fields.One2many('fixture.player', 'fixture_id', string="Away Players", domain=[('home','=',False)])
    home_score = fields.Integer('Score', required=True,
        readonly=True, states={'draft': [('readonly', False)]})
    away_score = fields.Integer('Score', required=True,
        readonly=True, states={'draft': [('readonly', False)]})
    state = fields.Selection([
              ('draft', 'New'),
              ('finish', 'Finished'),
              ('close', 'Closed'),
         ], string='Status', index=True, default='draft')
    name = fields.Selection([
              ('round1', 'Round 1'),
               ('round2', 'Round 2'),
               ('round3', 'Round 3'),
               ('round4', 'Round 4'),
               ('round5', 'Round 5'),
               ('round6', 'Round 6'),
               ('round7', 'Round 7'),
               ('round8', 'Round 8'),
               ('round9', 'Round 9'),
               ('round10', 'Round 10'),
               ('round11', 'Round 11'),
               ('round12', 'Round 12'),
               ('round13', 'Round 13'),
               ('round14', 'Round 14'),
               ('round15', 'Round 15'),
               ('round16', 'Round 16'),
               ('round17', 'Round 17'),
               ('round18', 'Round 18'),
               ('round19', 'Round 19'),
               ('round20', 'Round 20'),
               ('round21', 'Round 21'),
               ('round22', 'Round 22'),
               ('round23', 'Round 23'),
               ('round24', 'Round 24'),
               ('round25', 'Round 25'),
               ('round26', 'Round 26'),
               ('round27', 'Round 27'),
               ('round28', 'Round 28'),
               ('round29', 'Round 29'),
               ('round30', 'Round 30'),
               ('round31', 'Round 31'),
               ('round32', 'Round 32'),
               ('round33', 'Round 33'),
               ('round34', 'Round 34'),
               ('round35', 'Round 35'),
               ('round36', 'Round 36'),
               ('round37', 'Round 37'),
               ('round38', 'Round 38'),
         ], string='Round', index=True, required=True,
        readonly=True, states={'draft': [('readonly', False)]})
    
    @api.multi
    def onchange_league_id(self, league_id):
        if not league_id:
            return {'value': {}}
        league_season_ids = self.env['league.season'].search([
                ('league_id', '=', league_id),
                ('state', '=', 'open')
            ])
        if league_season_ids:
            return {'value': {
                          'league_season_id': league_season_ids[0]
                      }}
        return {'value': {}}
    
    @api.multi
    def onchange_league_season_id(self, league_season_id):
        if not league_season_id:
            return {'value': {}}
        league_season = self.env['league.season'].browse(league_season_id)
        return {'value': {
                      'season_id': league_season.season_id.id,
                  }}
        
    def read_group(self, cr, uid, domain, fields, groupby, offset=0, limit=None, context=None, orderby=False, lazy=True):
        if 'home_score' in fields:
            fields.remove('home_score')
        if 'away_score' in fields:
            fields.remove('away_score')
        return super(fixture, self).read_group(cr, uid, domain, fields, groupby, offset=offset, limit=limit, context=context, orderby=orderby, lazy=lazy)
    
    @api.multi
    def action_finish(self):    
        self.message_post(body=_("Match is finished"))
        self.write({'state': 'finish'})
        season_team_obj = self.env['league.season.team']
        order = 'point desc'
        if self.league_id.code == 'PL':
            order = order + ',goal_defference desc,goal_for desc'
        elif self.league_id.code == 'Liga':
            order = order + ',goal_defference desc,goal_for desc'
        season_team_ids = season_team_obj.search([('league_id', '=', self.league_id.id)], order=order)
        rank = 0
        for item in season_team_ids:            
            rank = rank + 1
            item.write({'rank': rank})
        
        return True
    
    @api.multi
    def action_close(self):
        self.message_post(body=_("Match is closed"))
        return self.write({'state': 'close'})
    
    @api.multi
    def action_draft(self):
        self.message_post(body=_("Match is set to draft"))
        return self.write({'state': 'draft'})
    
    @api.multi
    def unlink(self):
        for item in self:
            if item.state not in ('draft'):
                raise Warning(_('You cannot delete an record which is not draft.'))
        return super(fixture, self).unlink()
    
    