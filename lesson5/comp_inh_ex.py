"""
Lesson 5: Composition vs Inheritance

This script illustrates the difference between inheritance ("is-a" relationship)
and composition ("has-a" relationship) using a Logging example.
"""

# ==========================================
# 1. Inheritance Approach ("is-a")
# ==========================================

class Logger:
    def log(self, message):
        print(f"[LOG] {message}")

class Robot(Logger):
    """
    Inheritance: Robot IS-A Logger (semantically questionable).
    Tight coupling: Robot is forced to have Logger's interface.
    """
    def __init__(self, name):
        self.name = name

    def work(self):
        self.log(f"{self.name} is starting to work.")
        # ... doing work ...
        self.log(f"{self.name} finished working.")

# ==========================================
# 2. Composition Approach ("has-a")
# ==========================================

class BetterLogger:
    def log(self, message):
        print(f"[BETTER-LOG] {message}")

class AdvancedRobot:
    """
    Composition: AdvancedRobot HAS-A Logger.
    Loose coupling: We can swap the logger easily (Dependency Injection).
    """
    def __init__(self, name, logger=None):
        self.name = name
        # If no logger provided, we could use a default or handle None
        self._logger = logger or BetterLogger()

    def work(self):
        self._logger.log(f"{self.name} is starting to work.")
        # ... doing work ...
        self._logger.log(f"{self.name} finished working.")

# ==========================================
# Verification / Demonstration
# ==========================================

if __name__ == "__main__":
    print("--- Inheritance Approach ---")
    r1 = Robot("Robbie")
    r1.work()
    # Problem: r1.log("Oops") is exposed as part of Robot's public API!
    
    print("\n--- Composition Approach ---")
    # We can use the default logger
    r2 = AdvancedRobot("Tars")
    r2.work()

    print("\n--- Composition Flexibility (Swapping Behavior) ---")
    class FileLogger:
        def log(self, message):
            print(f"[FILE] Writing to log file: {message}")

    # Injecting a different behavior without changing AdvancedRobot code
    file_logger = FileLogger()
    r3 = AdvancedRobot("Case", logger=file_logger)
    r3.work()
