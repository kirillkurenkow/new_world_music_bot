import logging
import os
import sys
import time
from datetime import datetime

from Source import (
    ConfigReader,
    ScreenShot,
    Game,
    UnknownKeyError,
    SongIsEmptyError,
    clear_console,
)

logging.basicConfig(
    filename='new_world_music_bot.log',
    filemode='w',
    format='[%(asctime)s] %(levelname)s: %(filename)s(%(lineno)d): %(funcName)s: %(message)s',
    level=logging.DEBUG,
    encoding='utf-8'
)
LOGGER = logging.getLogger(__name__)


class Config:
    def __init__(self):
        config_path = os.path.join('Resource', 'config.ini')
        config_reader = ConfigReader(filename=config_path)

        self.Global = self.__Global(config_reader)
        self.ScreenShot = self.__ScreenShot(config_reader)
        self.Songs = self.__Songs(config_reader)
        self.Timings = self.__Timings(config_reader)

    class __Global:
        def __init__(self, config_reader: ConfigReader):
            __section = 'GLOBAL'

            real_max_songs = 10_000
            self.max_songs = config_reader.getint(__section, 'max_songs')
            self.max_songs = self.max_songs if 1 <= self.max_songs <= real_max_songs else real_max_songs

    class __ScreenShot:
        def __init__(self, config_reader: ConfigReader):
            __section = 'SCREENSHOT'

            self.box_x_0 = config_reader.getint(__section, 'box_x_0')
            self.box_x_1 = config_reader.getint(__section, 'box_x_1')
            self.box_y_0 = config_reader.getint(__section, 'box_y_0')
            self.box_y_1 = config_reader.getint(__section, 'box_y_1')
            self.x_offset = config_reader.getint(__section, 'x_offset')

    class __Songs:
        def __init__(self, config_reader: ConfigReader):
            self.Novice = self.__Novice(config_reader)
            self.Skilled = self.__Skilled(config_reader)
            self.Expert = self.__Expert(config_reader)

        class __Novice:
            def __init__(self, config_reader: ConfigReader):
                __section = 'SONGS_NOVICE'

        class __Skilled:
            def __init__(self, config_reader: ConfigReader):
                __section = 'SONGS_SKILLED'

        class __Expert:
            def __init__(self, config_reader: ConfigReader):
                __section = 'SONGS_EXPERT'

                self.wyrdwood_leaves_guitar = config_reader.get(__section, 'wyrdwood_leaves_guitar')

    class __Timings:
        def __init__(self, config_reader: ConfigReader):
            __section = 'TIMINGS'

            self.mouse_press = config_reader.getnumber(__section, 'mouse_press')
            self.performance_end = config_reader.getnumber(__section, 'performance_end')
            self.screenshot_frequency = config_reader.getnumber(__section, 'screenshot_frequency')
            self.between_songs = config_reader.getnumber(__section, 'between_songs')
            self.before_start = config_reader.getnumber(__section, 'before_start')


def main():
    # Config init
    config = Config()

    # Select song
    select = None
    song_level = ''
    songs_to_select = []
    while select is None:
        clear_console()
        select = input('Select level:\n1. Novice\n2. Skilled\n3. Expert\n0. Exit\n\n>> ')
        if select == '1':
            song_level = 'Novice'
            songs_to_select = [song for song in dir(config.Songs.Novice) if not song.startswith('_')]
            break
        elif select == '2':
            song_level = 'Skilled'
            songs_to_select = [song for song in dir(config.Songs.Skilled) if not song.startswith('_')]
            break
        elif select == '3':
            song_level = 'Expert'
            songs_to_select = [song for song in dir(config.Songs.Expert) if not song.startswith('_')]
            break
        elif select == '0':
            return
        select = None
    select = None
    song = []
    while select is None:
        clear_console()
        print('Select song:')
        for i, song_name in enumerate(songs_to_select):
            print(f'{i + 1}. {song_name}')
        print('0. Exit')
        select = input('\n>> ')
        try:
            select = int(select)
            if select == 0:
                return
            if select in range(1, len(songs_to_select) + 1):
                song = list(config.Songs.__getattribute__(song_level).__getattribute__(songs_to_select[select - 1]))
                LOGGER.info(f'Song chosen: {songs_to_select[select - 1]}[{song_level}]')
                LOGGER.info(f'Song keys: {song}')
                break
        except ValueError:
            pass
        select = None
    clear_console()

    # Vars / config values
    screenshot_box = (
        config.ScreenShot.box_x_0 + config.ScreenShot.x_offset,
        config.ScreenShot.box_y_0,
        config.ScreenShot.box_x_1 + config.ScreenShot.x_offset,
        config.ScreenShot.box_y_1,
    )
    just_pressed = False
    no_black_pixel_count = 0
    songs_played = 0

    # Game init
    game = Game(
        song=song,
        mouse_press_time=config.Timings.mouse_press,
    )

    LOGGER.info(f'Songs to play: {config.Global.max_songs}')

    # Start delay
    LOGGER.info(f'Waiting before start: {config.Timings.before_start}')
    for i in range(config.Timings.before_start):
        print(f'Start in {config.Timings.before_start - i} ...')
        time.sleep(1)

    # Performance start
    game.start_performance()

    # Main cycle
    while True:
        cycle_time = datetime.now()
        screenshot = ScreenShot(screenshot_box)
        if screenshot.have_black_pixel and not just_pressed:
            try:
                game.press_next_key()
                just_pressed = True
            except UnknownKeyError as exception:
                LOGGER.exception(exception)
                raise
            except SongIsEmptyError:
                songs_played += 1
                LOGGER.info('Song complete')
                LOGGER.info(f'Songs played: {songs_played}')
                just_pressed = False

                # End performance
                time.sleep(config.Timings.performance_end)
                print('Ending performance ...')
                game.end_performance()

                # Check songs played quantity
                songs_left = config.Global.max_songs - songs_played
                if songs_left == 0:
                    text = 'All songs complete'
                    LOGGER.info(text)
                    print(text)
                    return
                text = f'Songs left: {songs_left}'
                LOGGER.info(text)
                print(text)
                game.refresh_song()
                time.sleep(config.Timings.between_songs)

                # Start performance
                print('Starting new performance ...')
                game.start_performance()
        else:
            no_black_pixel_count += 1
            if no_black_pixel_count > 30:
                just_pressed = False
        LOGGER.debug(f'Cycle time: {(datetime.now() - cycle_time).total_seconds()}')
        time.sleep(config.Timings.screenshot_frequency)


if __name__ == '__main__':
    try:
        main()
    except (SongIsEmptyError, UnknownKeyError):
        sys.exit(2)
    except KeyboardInterrupt:
        LOGGER.info('Stopped by KeyboardInterrupt')
        sys.exit(0)
    except Exception as main_exception:
        LOGGER.exception(main_exception)
        raise
