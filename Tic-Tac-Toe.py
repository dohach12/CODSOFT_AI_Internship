import streamlit as st
import numpy as np
import time
from typing import List, Tuple, Optional

class TicTacToe:
    def __init__(self):
        self.board = [' ' for _ in range(9)]
        self.human_player = 'X'
        self.ai_player = 'O'
    
    def make_move(self, position: int, player: str) -> bool:
        if self.board[position] == ' ':
            self.board[position] = player
            return True
        return False
    
    def available_moves(self) -> List[int]:
        return [i for i, spot in enumerate(self.board) if spot == ' ']
    
    def check_winner(self, player: str) -> bool:
        # Check rows
        for i in range(0, 9, 3):
            if all(self.board[i+j] == player for j in range(3)):
                return True
        
        # Check columns
        for i in range(3):
            if all(self.board[i+j*3] == player for j in range(3)):
                return True
        
        # Check diagonals
        if all(self.board[i] == player for i in [0, 4, 8]):
            return True
        if all(self.board[i] == player for i in [2, 4, 6]):
            return True
        
        return False
    
    def is_board_full(self) -> bool:
        return ' ' not in self.board
    
    def minimax(self, board: List[str], depth: int, is_maximizing: bool) -> int:
        if self.check_winner(self.ai_player):
            return 1
        if self.check_winner(self.human_player):
            return -1
        if self.is_board_full():
            return 0
            
        if is_maximizing:
            best_score = float('-inf')
            for move in self.available_moves():
                board[move] = self.ai_player
                score = self.minimax(board, depth + 1, False)
                board[move] = ' '
                best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for move in self.available_moves():
                board[move] = self.human_player
                score = self.minimax(board, depth + 1, True)
                board[move] = ' '
                best_score = min(score, best_score)
            return best_score
    
    def get_best_move(self) -> int:
        best_score = float('-inf')
        best_move = 0
        
        for move in self.available_moves():
            self.board[move] = self.ai_player
            score = self.minimax(self.board, 0, False)
            self.board[move] = ' '
            
            if score > best_score:
                best_score = score
                best_move = move
        
        return best_move

def initialize_game():
    if 'board' not in st.session_state:
        st.session_state.board = [' ' for _ in range(9)]
    if 'game_over' not in st.session_state:
        st.session_state.game_over = False
    if 'winner' not in st.session_state:
        st.session_state.winner = None
    if 'scores' not in st.session_state:
        st.session_state.scores = {'Human': 0, 'AI': 0, 'Ties': 0}

def reset_board():
    st.session_state.board = [' ' for _ in range(9)]
    st.session_state.game_over = False
    st.session_state.winner = None

def main():
    st.set_page_config(page_title="Tic-Tac-Toe AI", layout="wide")
    
    st.title("🎮 Tic-Tac-Toe AI Platform")
    initialize_game()
    
    # Create two columns for layout
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Game Board")
        
        # Create the 3x3 grid using columns
        for i in range(0, 9, 3):
            cols = st.columns(3)
            for j in range(3):
                if st.session_state.board[i + j] == ' ':
                    if cols[j].button('Play here', key=f'button_{i+j}', disabled=st.session_state.game_over):
                        # Human move
                        st.session_state.board[i + j] = 'X'
                        
                        # Check if human won
                        game = TicTacToe()
                        game.board = st.session_state.board
                        if game.check_winner('X'):
                            st.session_state.winner = 'Human'
                            st.session_state.game_over = True
                            st.session_state.scores['Human'] += 1
                        elif not game.available_moves():
                            st.session_state.winner = 'Tie'
                            st.session_state.game_over = True
                            st.session_state.scores['Ties'] += 1
                        else:
                            # AI move
                            ai_move = game.get_best_move()
                            st.session_state.board[ai_move] = 'O'
                            
                            # Check if AI won
                            if game.check_winner('O'):
                                st.session_state.winner = 'AI'
                                st.session_state.game_over = True
                                st.session_state.scores['AI'] += 1
                            elif not game.available_moves():
                                st.session_state.winner = 'Tie'
                                st.session_state.game_over = True
                                st.session_state.scores['Ties'] += 1
                        
                        st.rerun()
                else:
                    cols[j].markdown(f"<h1 style='text-align: center; color: {'blue' if st.session_state.board[i + j] == 'X' else 'red'};'>{st.session_state.board[i + j]}</h1>", unsafe_allow_html=True)
    
    with col2:
        st.subheader("Game Status")
        
        # Display scores
        st.write("### Scores:")
        st.write(f"🧑 Human: {st.session_state.scores['Human']}")
        st.write(f"🤖 AI: {st.session_state.scores['AI']}")
        st.write(f"🤝 Ties: {st.session_state.scores['Ties']}")
        
        # Display game status
        if st.session_state.winner:
            if st.session_state.winner == 'Tie':
                st.info("🤝 Game Over - It's a Tie!")
            else:
                st.success(f"🎉 Game Over - {st.session_state.winner} wins!")
        
        # Reset button
        if st.button("New Game"):
            reset_board()
            st.rerun()
        
        # Reset scores button
        if st.button("Reset Scores"):
            st.session_state.scores = {'Human': 0, 'AI': 0, 'Ties': 0}
            st.rerun()
        
        # Instructions
        with st.expander("How to Play"):
            st.write("""
            1. Click on any empty square to make your move
            2. You play as X (blue), AI plays as O (red)
            3. Try to get three in a row horizontally, vertically, or diagonally
            4. The AI uses the Minimax algorithm and plays perfectly
            5. Click 'New Game' to start over
            """)

if __name__ == "__main__":
    main()