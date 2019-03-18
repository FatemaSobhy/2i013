#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from math import *
from soccersimulator import*


class SuperState(object):
    def __init__(self, state, id_team, id_player):
        self.state = state
        self.id_team = id_team 
        self.id_player = id_player

    def __getattr__(self, attr):
        return getattr(self.state, attr)     

    @property
    def ball(self):
        return self.state.ball.position
    
    @property
    def player(self):
        return self.state.player_state(self.id_team, self.id_player).position
   
    @property 
    def goal(self):
        return Vector2D(GAME_WIDTH * ((self.id_team-1)), GAME_HEIGHT /2)
    
    @property 
    def goal_opponent(self):
        return Vector2D(GAME_WIDTH * (2- self.id_team), GAME_HEIGHT /2)
    
    @property
    def pos_def(self):
        if self.id_team == 1:
            pos = GAME_WIDTH/5
        else:
            pos = (4*GAME_WIDTH)/5
        return pos
    
    @property
    def milieu(self):
        if self.id_team == 1:
            return self.ball.x <= GAME_WIDTH/2
        else:
            return self.ball.x > GAME_WIDTH/2
    #id_team de l'équipe adverse
    @property
    def id_opponent(self):
        return (self.id_team % 2)+1
    #pour se deplacer vers un objet 
    def deplacement(self, obj):
        return (obj -self.player).normalize()*6
    
    @property
    def goal_radius(self):
        return GAME_GOAL_HEIGHT/2.
    
    #centre des cages
    @property
    def goal_center(self):
        return self.goal_radius + GAME_HEIGHT/2.
    
    #foncer vers le but 
    @property
    def foncer_vers_but(self):
        return SoccerAction(shoot = (self.goal - self.ball).normalize())
   
    #shoot vers le but 
    @property
    def tirer_au_but(self):
        return SoccerAction(shoot =(self.goal - self.ball).normalize()*maxPlayerShoot) 
    
    @property
    def can_shoot(self):
        return (self.state.ball.position - self.state.player_state(self.id_team, self.id_player).position).norm <= BALL_RADIUS + PLAYER_RADIUS
    
    @property
    def shoot(self, target, strength):
        return (target-state.player_state(id_team, id_player).position).normalize() * strength
    
	#liste des opponents
    @property
    def opponents(self):
        return [self.state.player_state(id_team, id_player).position for (id_team, id_player) in self.state.players if id_team != self.id_team]
    
    #si c'est un adversaire ou pas
    @property
    def Test_opponents(self):
        for i in opponents:
            return True
        return False
    
    #trouver l'adversaire le plus proche
    @property
    def closest_opponent(self):
        return min([(self.player.distance(player), player) for player in self.opponents],key=lambda x: x[0])[1]
	
    #liste des joueurs
    @property
    def list_player(self):
        return [self.state.player_state(it, ip).position for (it, ip) in self.state.players]

	#joueur avec la balle 
    @property
    def player_with_ball(self):
        return min([(player.distance(self.ball),player) for player in self.list_player], key=lambda x: x[0])[1]
     
    def has_ball (self, pos):
        return self.ball.distance(pos) <= PLAYER_RADIUS+ BALL_RADIUS
    
    #test joueur avec la balle
    @property
    def test_ball(self):
        return (self.player_with_ball == self.player)
    
    #coin haut gauche
    @property
    def tirCoinHautG(self):
        return Vector2D(0, 90) - self.ball
    
    #coin bas gauche
    @property
    def tirCoinBasG(self):
        return Vector2D(0, 0) - self.ball
    
    #coin haut droit
    @property
    def tirCoinBasG(self):
        return Vector2D(150, 90) - self.ball
    
    #coin bas gdroit
    @property
    def tirCoinBasG(self):
        return Vector2D(150, 0) - self.ball
    
    @property
    def ballameliorer(self):
        return self.state.ball.position  + 5* self.state.ball.vitesse
    
    @property 
    def teamdef(self):
        if self.id_team == 1:
            (posdef, condition) = (1/4, self.ballameliorer.x > GAME_WIDTH*(1/3))
        else:
            (posdef,condition) =(3/4, self.ballameliorer.x < GAME_WIDTH*(2/3))
        return (posdef, condition)
    
    @property 
    def teamatt(self):
        if self.id_team == 1:
            (posatta, nextpos) = (self.player.x < GAME_WIDTH*(1/2), GAME_WIDTH*(6/10))
        else:
            (posatta,nextpos) =(self.player.x > GAME_WIDTH*(1/2), GAME_WIDTH*(4/10))
        return (posatta, nextpos)
        
    @property
    def coequipier(self):
        for(id_team, id_player) in self.state.players:
            if (id_team == self.id_team) and (id_player != self.id_player):
                return self.state.player_state(id_team, id_player).position
    
    #liste des coequipiers
    @property
    def listecoequipier(self):
        return [self.state.player_state(id_team, id_player).position for (id_team, id_player) in self.state.players if (id_team == self.id_team) and (id_player != self.id_player)]
   
    @property
    def coequipierproche(self):
        return min([(self.player.distance(player), player) for player in self.listecoequipier],key=lambda x: x[0])[1]
        
                  
    #trouver la distance entre 2 points
    def getDistanceTo(self, obj):
        return self.player.distance(obj)
    
    @property
    def coequipierprochedugoal(self):
        return min([(self.player.distance(self.goal), player) for player in self.listecoequipier],key=lambda x: x[0])[1]
    @property
    def coequipierprocheball(self):
        return min([(self.player.distance(self.ball), player) for player in self.listecoequipier],key=lambda x: x[0])[1]
   
    @property
    def dist_coequipier_player(self):
        return Vector2D(self.player.x - self.coequipierproche.x, self.player.y - self.coequipierproche.y).norm
    
    @property
    def dist_opponent_player(self):
        return Vector2D(self.player.x - self.closest_opponent.x, self.player.y - self.closest_opponent.y).norm  
    
    @property 
    def terrain_5 (self):
        if self.id_team == 1:
            return self.ball.x >= 2*GAME_WIDTH/3
        else:
            return self.ball.x <= GAME_WIDTH/3
    @property
    def estderriere(self):
        if self.id_team == 1:
            return self.closest_opponent.x > self.player.x
            
        if self.id_team == 2:
            return self.closest_opponent.x < self.player.x
    @property
    def estderriere(self):
        if self.id_team == 1:
            return self.closest_opponent.x > self.player.x
            
        if self.id_team == 2:
            return self.closest_opponent.x < self.player.x

    @property
    def dribble(self) :
        if self.estderriere: #si l'adversaire est derrière on dribble 
            if self.closest_opponent.y > self.player.y or self.closest_opponent.y == self.player.y : #Si le joueur vient par la droite
                dir = (self.goal_opponent - self.player).normalize() * 1.5
                dir.angle -= 3.14/6
                return SoccerAction(shoot = dir)                    
            else : 
                dir = (self.goal_opponent - self.player).normalize() * 1.5
                dir.angle += 3.14/6
                return SoccerAction(shoot = dir)                
        else : 
            shoot = self.goal_opponent - self.player
            return SoccerAction(shoot = shoot.normalize()*1.2)
    
    @property 
    def pos_att(self):
        if self.id_team ==1:
            return Vector2D(4*GAME_WIDTH/5, GAME_HEIGHT/3)
        else:
            return Vector2D(GAME_WIDTH/5, GAME_HEIGHT/3)
    @property
    def pos_att2(self):
        if self.id_team == 1:
            return Vector2D( 2*GAME_WIDTH/3,  2*GAME_HEIGHT/3)
        else:
            return Vector2D(GAME_WIDTH/3, 2*GAME_HEIGHT/3)
        
        
    @property 
    def balldevantjoueur(self):
        if self.id_team == 1:
            return self.ball.x > self.player.x
        else:
            return self.ball.x < self.player.x






#class SimpleStrategy ( Strategy ):
#    def __init__ ( self , action , name ):
#        super().__init__ ( name )
#        self.action = action
#        
#    def compute_strategy (self, state , id_team , id_player):
#        s = SuperState (state , id_team , id_player )
#        return self.action(s)
#            
#            
