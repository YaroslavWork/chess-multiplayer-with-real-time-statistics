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

    def _engine_loop(self):
        while self.running:
            if self.board_to_analyze is None:
                time.sleep(0.1)
                continue

            try:
                with chess.engine.SimpleEngine.popen_uci(self.path) as engine:
                    last_analyzed = self.board_to_analyze
                    
                    with engine.analysis(last_analyzed) as analysis:
                        for info in analysis:
                            if self.board_to_analyze != last_analyzed or not self.running:
                                break
                            
                            if "score" in info:
                                self.current_score = str(info["score"].white())
                            if "depth" in info:
                                self.current_depth = info["depth"]
            except Exception as e:
                print(f"Engine Error: {e}")
                time.sleep(1) # Wait before trying to reboot engine