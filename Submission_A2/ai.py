import random
import time
from turtle import st
import numpy as np
from typing import List, Tuple, Dict
from connect4.utils import get_pts, get_valid_actions, Integer
from copy import deepcopy

class Node:
    def __init__(self,state,player):
        self.state=state
        self.board=state[0]
        self.temp=state[1]
        self.parent=None
        self.player=player
        self.pts=get_pts(player,state[0])
        self.nextmoves=None
        self.child_states=[]
class AIPlayer:
    def __init__(self, player_number: int, time: int):
        """
        :param player_number: Current player number
        :param time: Time per move (seconds)
        """
        self.player_number = player_number
        self.type = 'ai'
        self.player_string = 'Player {}:ai'.format(player_number)
        self.time = time
        # Do the rest of your implementation here
    def height_board(self,board):
        row,col=board.shape
        for each in board:
            col-=1
            if self.player_number in each:
                return col
        return 0

    def get_intelligent_move(self, state: Tuple[np.array, Dict[int, Integer]]) -> Tuple[int, bool]:
        """
        Given the current state of the board, return the next move
        This will play against either itself or a human player
        :param state: Contains:
                        1. board
                            - a numpy array containing the state of the board using the following encoding:
                            - the board maintains its same two dimensions
                                - row 0 is the top of the board and so is the last row filled
                            - spaces that are unoccupied are marked as 0
                            - spaces that are occupied by player 1 have a 1 in them
                            - spaces that are occupied by player 2 have a 2 in them
                        2. Dictionary of int to Integer. It will tell the remaining popout moves given a player
        :return: action (0 based index of the column and if it is a popout move)
        """
        times=time.time()
        # Do the rest of your implementation here
        start_flag=True
        row,col=state[0].shape
        for i in range(col):
            if(state[0][row-1][i]!=0):
                start_flag=False 
        if start_flag:
            return (col//2,False)
        if get_pts(self.player_number,state[0])==0 and get_pts(3-self.player_number,state[0])==0 and state[0][row-1][col//2]==0:
            return col//2,False
        if get_pts(self.player_number,state[0])==0 and get_pts(3-self.player_number,state[0])==0 and state[0][row-1][(col//2)-1]==0:
            return (col//2)-1,False
        if get_pts(self.player_number,state[0])==0 and get_pts(3-self.player_number,state[0])==0:
            var1=len(state[0][0])//2
            if state[0][len(state[0])-2][var1]!=0:
                var1=var1-1
            return var1,False   
        print("*******************************************")
        depth=5
        if self.time<=8:
            depth=3
        INF=10000000    
        move,val=self.minimax(state,depth,-INF,INF,True,self.player_number,times)
        print(val)
        return move 
        raise NotImplementedError('Whoops I don\'t know what to do')

    def get_expectimax_move(self, state: Tuple[np.array, Dict[int, Integer]]) -> Tuple[int, bool]:
        """
        Given the current state of the board, return the next move based on
        the Expecti max algorithm.
        This will play against the random player, who chooses any valid move
        with equal probability
        :param state: Contains:
                        1. board
                            - a numpy array containing the state of the board using the following encoding:
                            - the board maintains its same two dimensions
                                - row 0 is the top of the board and so is the last row filled
                            - spaces that are unoccupied are marked as 0
                            - spaces that are occupied by player 1 have a 1 in them
                            - spaces that are occupied by player 2 have a 2 in them
                       	2. Dictionary of int to Integer. It will tell the remaining popout moves given a player
        :return: action (0 based index of the column and if it is a popout move)
        """
        # Do the rest of your implementation here
        start_flag=True
        row,col=state[0].shape
        for i in range(col):
            if(state[0][row-1][i]!=0):
                start_flag=False
        if start_flag:
            return (col//2,False)
        if get_pts(self.player_number,state[0])==0 and get_pts(3-self.player_number,state[0])==0 and state[0][row-1][col//2]==0:
            return col//2,False
        if get_pts(self.player_number,state[0])==0 and get_pts(3-self.player_number,state[0])==0 and state[0][row-1][(col//2)-1]==0:
            return (col//2)-1,False
        if get_pts(self.player_number,state[0])==0 and get_pts(3-self.player_number,state[0])==0:
            var1=len(state[0][0])//2
            if state[0][len(state[0])-2][var1]!=0:
                var1=var1-1
            return var1,False
        depth=3
        print("***************************************************")
        root=Node(state,self.player_number)
        self.create_tree(depth,root)
        max_val=-10000000
        max_index=0
        for i in range(len(root.child_states)):
            kk=1
            if root.child_states[i].state[1][self.player_number]==0:
                kk=0
            temp=self.expectimax(root.child_states[i],False,kk)
            print("ee "+str(i)+" "+str(temp))
            if(max_val<temp):
                max_val=temp
                max_index=i
        print(max_index)
        return root.nextmoves[max_index]
	
        raise NotImplementedError('Whoops I don\'t know what to do')

    def next_state(self,state_original,move,player):
        state=(deepcopy(state_original[0]),deepcopy(state_original[1]))
        if move[1]:
            s=len(state[0])
            for i in range(s-1):
                state[0][i+1][move[0]]=state[0][i][move[0]]
            state[1][player].decrement()
            #print(state[1][player].get_int())
            return state
        else:
            s=len(state[0])
            check_flag=True
            for i in range(s-1):
                if state[0][i+1][move[0]]!=0:
                    state[0][i][move[0]]=player
                    check_flag=False
            if check_flag:
                state[0][s-1][move[0]]=player
            return state

    def create_tree(self,depth,root):
        
        state=root.state
        board=root.board
        player=root.player
        next_player=player+1
        if(next_player>2):
            next_player=1
        next_moves=get_valid_actions(player,state)
        #print("hello "+str(root.player)+" "+str(len(next_moves))+" "+str(depth))
        #print(state)
        root.nextmoves=next_moves
        for move in next_moves:
            temp_node=Node(self.next_state(state,move,player),next_player)
            temp_node.parent=root
            root.child_states.append(temp_node)
        if depth==1:
            return
        else:
            depth-=1
            for each_node in root.child_states:
                self.create_tree(depth,each_node)
    
    def expectimax(self,node,is_max,no_pops):
        child=node.child_states
        if node.nextmoves==None or len(child)==0:
            kk=1
            if node.temp[self.player_number]==0:
                kk=0
            return 2*(get_pts(self.player_number,node.state[0])-get_pts(3-self.player_number,node.board))-no_pops*(get_pts(self.player_number,node.parent.state[0])-get_pts(3-self.player_number,node.parent.board))
        if(is_max):
            max_expecti=0
            child=node.child_states
            for each_node in child:
                e=self.expectimax(each_node,False,no_pops)
                if (e>max_expecti):
                    max_expecti=e
            return max_expecti
        else:
            sum_expecti=0
            for each_node in child:
                sum_expecti+=self.expectimax(each_node,True,no_pops)
            avg_expecti=sum_expecti/len(child)
            return avg_expecti

    def heuristic(self,board,player):
        return get_pts(player,board)-get_pts(3-player,board)

    def minimax(self,state, depth, alpha, beta, maximizingPlayer,player_no,times):
        next_player_no=3-player_no
        board=state[0]
        temp=state[1]
        INF=10000000
        valid_moves = get_valid_actions(player_no,state)
        if depth == 0 or len(valid_moves)==0 or (self.time-(time.time()-times))<=2.5:
            if len(valid_moves)==0:
                return (None, self.heuristic(board,self.player_number))
            else: # Depth is zero
                return (None, self.heuristic(board,self.player_number))
        if maximizingPlayer:
            value = -INF
            move_made = random.choice(valid_moves)
            ###
            next_sta=self.next_state(state,move_made,player_no)
            new_score = self.minimax(next_sta, depth-1, alpha, beta, False,next_player_no,times)[1]
            if new_score > value:
                #print("max")
                value = new_score
            alpha = max(alpha, value)
            ###
            for curr_move in valid_moves:
                next_sta=self.next_state(state,curr_move,player_no)
                new_score = self.minimax(next_sta, depth-1, alpha, beta, False,next_player_no,times)[1]
                if new_score > value:
                    #print("max")
                    value = new_score
                    move_made=curr_move
                    #print(move_made)
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return move_made, value

        else: # Minimizing player
            value = INF
            move_made = random.choice(valid_moves)
            ###
            next_sta=self.next_state(state,move_made,player_no)
            new_score = self.minimax(next_sta, depth-1, alpha, beta, True,next_player_no,times)[1]
            if new_score < value:
                #print("min")
                value = new_score
            beta = min(beta, value)
            ###
            for curr_move in valid_moves:
                next_sta=self.next_state(state,curr_move,player_no)
                new_score = self.minimax(next_sta, depth-1, alpha, beta, True,next_player_no,times)[1]
                if new_score < value:
                    #print("min")
                    value = new_score
                    #move_made=curr_move
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return move_made, value

        