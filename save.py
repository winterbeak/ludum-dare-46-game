class ProgressTracker:
    def __init__(self, level_count):
        self._completed_levels = [False] * level_count

    @property
    def completed_levels(self):
        return self._completed_levels

    def complete_level(self, level_num):
        self._completed_levels[level_num] = True

    def uncomplete_level(self, level_num):
        self._completed_levels[level_num] = False
