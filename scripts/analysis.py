import chess
import chess.engine
import threading
import time

class EngineManager:
    def __init__(self, path):
        self.path = path
        self.current_score = "0.0"
        self.current_depth = 0
        self.board_to_analyze = None
        self.running = True
        
        self.thread = threading.Thread(target=self._engine_loop, daemon=True)
        self.thread.start()

    def start_analysis(self, board):
        self.board_to_analyze = board.copy()

    def _analyze_score(self, score_obj):
        """Helper to format the score correctly"""
        white_score = score_obj.white()
        if white_score.is_mate():
            mate_moves = white_score.mate()
            if mate_moves > 0:
                return f"+M{mate_moves}"  # White is winning
            else:
                return f"-M{-mate_moves}" # Black is winning
        else:
            cp = white_score.score()
            if cp is None: return "0.0"
            return f"{cp / 100.0:.1f}"

    def _engine_loop(self):
        while self.running:
            if self.board_to_analyze is None:
                time.sleep(0.1)
                continue

            try:
                # Use a context manager for the engine
                with chess.engine.SimpleEngine.popen_uci(self.path) as engine:
                    current_pos = self.board_to_analyze
                    with engine.analysis(current_pos) as analysis:
                        for info in analysis:
                            if self.board_to_analyze != current_pos or not self.running:
                                break
                            
                            if "score" in info:
                                self.current_score = self._analyze_score(info["score"])
                                
                            if "depth" in info:
                                self.current_depth = info["depth"]
                                if self.current_depth >= 244:
                                    break
                            
                            # Allow other threads to breathe
                            time.sleep(0.05) 
            except Exception as e:
                print(f"Engine Error: {e}")
                time.sleep(1)