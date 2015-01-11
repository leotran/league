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
from openerp.exceptions import except_orm

class league(models.Model):
    _name = 'league'
    _description = 'League'
    
    name = fields.Char(string='Name', required=True)
    country_id = fields.Many2one('res.country',string='Country')
    code = fields.Char(string='Code', required=True)
    
    def unlink(self, cr, uid, ids, context=None):
        raise except_orm(_('Error!'),_('League cannot delete!'))
        return True
    
class season(models.Model):
    _name = 'season'
    _description = 'Season'
    
    name = fields.Char(string='Name', required=True)

class league_season_team(models.Model):
    _name = 'league.season.team'
    _description = 'League Season Team'
    
    @api.one
    @api.depends(
         'fixture_home_ids.home_score',
         'fixture_home_ids.away_score',
         'fixture_home_ids.team_home_id',
         'fixture_home_ids.team_away_id',
         'fixture_home_ids.state',
         'fixture_away_ids.home_score',
         'fixture_away_ids.away_score',
         'fixture_away_ids.team_home_id',
         'fixture_away_ids.team_away_id',
         'fixture_away_ids.state'         
    )
    def _count(self):
        # home
        participate_home = 0
        win_home = 0
        draw_home = 0
        loss_home = 0
        gf_home = 0
        ga_home = 0
        point_home = 0        
        
        #way
        participate_away = 0
        win_away = 0
        draw_away = 0
        loss_away = 0
        gf_away = 0
        ga_away = 0
        point_away = 0        
        
        for item in self.fixture_home_ids:
            if item.state != 'draft':
                participate_home += 1
                if item.home_score > item.away_score:
                    win_home += 1
                    point_home += 3
                if item.home_score == item.away_score:
                    draw_home += 1
                    point_home += 1
                if item.home_score < item.away_score:
                    loss_home += 1
                gf_home += item.home_score
                ga_home += item.away_score
            
        for item in self.fixture_away_ids:
            if item.state != 'draft':
                participate_away += 1
                if item.away_score > item.home_score:
                    win_away += 1
                    point_away += 3
                if item.away_score == item.home_score:
                    draw_away += 1
                    point_away += 1
                if item.away_score < item.home_score:            
                    loss_away += 1
                gf_away += item.away_score
                ga_away += item.home_score
        
        self.participate = participate_home + participate_away
        self.win = win_home + win_away
        self.draw = draw_home + draw_away
        self.loss = loss_home + loss_away
        self.goal_for = gf_home + gf_away
        self.goal_against = ga_home + ga_away
        self.goal_defference = (gf_home + gf_away) - (ga_home + ga_away)
        self.point = point_home + point_away 
    
    league_season_id = fields.Many2one('league.season', string='League Season',
        ondelete='cascade')
    league_id = fields.Many2one('league', string='League',
        related='league_season_id.league_id', store=True, readonly=True)
    season_id = fields.Many2one('season', string='Season',
        related='league_season_id.season_id', store=True, readonly=True)
    team_id = fields.Many2one('team', string='Team', required=True)
    name = fields.Char(string='Name', related='team_id.name', store=True, readonly=True)
    participate = fields.Integer(string='P', store=True, readonly=True, compute='_count')
    win = fields.Integer(string='W', store=True, readonly=True, compute='_count')
    draw = fields.Integer(string='D', store=True, readonly=True, compute='_count')
    loss = fields.Integer(string='L', store=True, readonly=True, compute='_count')
    goal_for = fields.Integer(string='GF', store=True, readonly=True, compute='_count')
    goal_against = fields.Integer(string='GA', store=True, readonly=True, compute='_count')
    goal_defference = fields.Integer(string='GD', store=True, readonly=True, compute='_count')
    point = fields.Integer(string='Pts', store=True, readonly=True, compute='_count')
    fixture_home_ids = fields.One2many('fixture', 'team_home_id', string='Matches Home', readonly=True)
    fixture_away_ids = fields.One2many('fixture', 'team_away_id', string='Matches Away', readonly=True)
    rank = fields.Integer('Rank', default=1)
    
    _order = 'rank,name'    

class league_season_player(models.Model):
    _name = 'league.season.player'
    
    @api.one
    @api.depends(
        'fixture_player_ids.player_id',
        'fixture_player_ids.goal'
    )
    def _count(self):        
        goals = 0
        for f in self.fixture_player_ids:
            goals += f.goal
        self.total_goal = goals
        self.total_played = len(self.fixture_player_ids)
        self.total_yc = 0
        self.total_rc = 0
    
    league_season_id = fields.Many2one('league.season', string='League Season',
        ondelete='cascade', required=True)
    league_id = fields.Many2one('league', string='League',
        related='league_season_id.league_id', store=True, readonly=True)
    season_id = fields.Many2one('season', string='Season',
        related='league_season_id.season_id', store=True, readonly=True)
    team_id = fields.Many2one('team', string='Team', required=True)
    player_id = fields.Many2one('res.partner', string="Player", required=True,
        domain=[('football_player','=',True)])
    name = fields.Char(string='Name', related='player_id.name', store=True, readonly=True)
    squad = fields.Integer('Squad')
    total_played = fields.Integer(string="Played", readonly=True,store=True, compute='_count')
    total_goal = fields.Integer(string="Goals", readonly=True, store=True, compute='_count')
    total_yc = fields.Integer(string="Yellow Card", readonly=True, store=True, compute='_count')
    total_rc = fields.Integer(string="Red Card", readonly=True, store=True, compute='_count')
    fixture_player_ids = fields.One2many('fixture.player', 'player_id', string="Matches")    
    
    _order = "total_goal desc,total_played,name"
    
    @api.multi
    def name_get(self):
        reads = self.read(['name','team_id'])
        res = []
        for record in reads:
            name = record['name']
            if record['team_id']:
                name = record['team_id'][1]+' / '+name
            res.append((record['id'], name))
        return res

class league_season(models.Model):
    _name = 'league.season'
    _description = 'League Season'
    _inherit = ['mail.thread']
    
    name = fields.Char(string='Name', required=True)
    league_id = fields.Many2one('league', string='League', required=True, readonly=True)
    country_id = fields.Many2one('res.country', string='Country',
         related='league_id.country_id')
    season_id = fields.Many2one('season', string='Season', required=True,
         states={'open': [('readonly', True)], 'finish': [('readonly', True)]})
    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')
    team_ids = fields.One2many('league.season.team', 'league_season_id', string='Team',
         states={'open': [('readonly', True)], 'finish': [('readonly', True)]})
    player_ids = fields.One2many('league.season.player', 'league_season_id', string='Team',
         states={'open': [('readonly', True)], 'finish': [('readonly', True)]})
    state = fields.Selection([
              ('draft', 'New'),
              ('open', 'Opening'),
              ('finish', 'Finished'),
         ], string='Status', index=True, default='draft')
    
    _sql_constraints = [
        ('league_season_uniq', 'unique(league_id, season_id)',
            'Season must be unique per League!'),
    ]
    
    @api.multi
    def onchange_league_id(self, league_id):
        if not league_id:
            return {'value':{}}
        league = self.env['league'].browse(league_id)
        return {'value': {
                      'country_id': league.country_id.id,
                  }}
    
    @api.multi
    def action_open(self):        
        if not self.team_ids:
            raise except_orm(_('Error!'),_('You cannot open season has no team!'))                
        
        item_id = self.search([('league_id','=',self.league_id.id),('state','=','open')])
        if item_id:
            raise except_orm(_('Error!'),_('You can only open one season per league!'))
                                
        self.message_post(body=_("New season is opened"))        
        return self.write({'state': 'open'})
    
    @api.multi
    def action_finish(self):
        self.message_post(body=_("Season is finished"))
        return self.write({'state': 'finish'})
    
    @api.multi
    def action_draft(self):
        self.message_post(body=_("Season is set to draft"))
        return self.write({'state': 'draft'})