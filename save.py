import files
import misc


class ProgressTracker:
    def __init__(self, level_count, save_file_path):
        self._level_count = level_count
        self._save_file_path = save_file_path
        self._completed_levels = [False] * level_count

    @property
    def completed_levels(self):
        return self._completed_levels

    def complete_level(self, level_num):
        self._completed_levels[level_num] = True

    def uncomplete_level(self, level_num):
        self._completed_levels[level_num] = False

    def save_progress(self):
        files.json_write(self._save_file_path, self._completed_levels)

    def load_progress(self):
        self._completed_levels = files.json_read(self._save_file_path)
        misc.force_length(self.completed_levels, self._level_count, False)

    def clear_progress(self):
        self._completed_levels = [False] * self._level_count
        self.save_progress()
