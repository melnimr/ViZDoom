"""
ViZDoom Python Type Stubs

This file provides type information for static analysis and IDE support.
For the official documentation, see: https://vizdoom.farama.org/
"""

from typing import List, Optional, Union, Dict
from enum import IntEnum
import numpy as np

# Sections:
# 0. Module Metadata / Constants            [line   20-  35]
# 1. ViZDoom Exceptions                     [line   36-  87]
# 2. ViZDoom Enums                          [line   88- 376]
# 3. ViZDoom Classes                        [line  377-1266]
# 4. ViZDoom Utility Functions              [line 1267-1325]
# 5. ViZDoom Global Enum Variables          [line 1326-1763]

# --------------- [0] Module Metadata / Constants ---------------
__version__: str

SLOT_COUNT: int
MAX_PLAYERS: int
MAX_PLAYER_NAME_LENGTH: int
USER_VARIABLE_COUNT: int
DEFAULT_TICRATE: int
DEFAULT_FPS: int
DEFAULT_FRAMETIME_MS: float
DEFAULT_FRAMETIME_S: float
BINARY_BUTTON_COUNT: int
DELTA_BUTTON_COUNT: int
BUTTON_COUNT: int


# --------------- [1] ViZDoom Exceptions ---------------
class FileDoesNotExistException(Exception):
    """
    Means that file specified as part of a configuration does not exist.
    """
    ...


class MessageQueueException(Exception):
    """
    Means that communication with ViZDoom's instance failed. 
    Usually, means a problem with permissions or system configuration.
    """
    ...


class SharedMemoryException(Exception):
    """
    Means that allocation/reading of shared memory failed. 
    Usually, means a problem with permissions or system configuration.
    """
    ...


class ViZDoomErrorException(Exception):
    """
    Means that an error in the ViZDoom engine occurred.
    """
    ...


class ViZDoomIsNotRunningException(Exception):
    """
    Means that called method cannot be used when ViZDoom instance is not running.
    """
    ...


class ViZDoomUnexpectedExitException(Exception):
    """
    Means that ViZDoom's instance was closed/terminated/killed from the outside.
    """
    ...


class SignalException(Exception):
    """
    Undocumented exception.
    """
    ...


# --------------- [2] ViZDoom Enums ---------------
class Mode(IntEnum):
    """
    Defines the mode for controlling the game.
    """
    PLAYER = 0
    SPECTATOR = 1
    ASYNC_PLAYER = 2
    ASYNC_SPECTATOR = 3

    __members__: Dict[str, Mode]


class ScreenFormat(IntEnum):
    """
    Defines the format of the screen buffer.
    """
    CRCGCB = 0
    RGB24 = 1
    RGBA32 = 2
    ARGB32 = 3
    CBCGCR = 4
    BGR24 = 5
    BGRA32 = 6
    ABGR32 = 7
    GRAY8 = 8
    DOOM_256_COLORS8 = 9

    __members__: Dict[str, ScreenFormat]


class ScreenResolution(IntEnum):
    """
    Defines the resolution of the screen buffer.
    """
    RES_160X120 = 0
    RES_200X125 = 1
    RES_200X150 = 2
    RES_256X144 = 3
    RES_256X160 = 4
    RES_256X192 = 5
    RES_320X180 = 6
    RES_320X200 = 7
    RES_320X240 = 8
    RES_320X256 = 9
    RES_400X225 = 10
    RES_400X250 = 11
    RES_400X300 = 12
    RES_512X288 = 13
    RES_512X320 = 14
    RES_512X384 = 15
    RES_640X360 = 16
    RES_640X400 = 17
    RES_640X480 = 18
    RES_800X450 = 19
    RES_800X500 = 20
    RES_800X600 = 21
    RES_1024X576 = 22
    RES_1024X640 = 23
    RES_1024X768 = 24
    RES_1280X720 = 25
    RES_1280X800 = 26
    RES_1280X960 = 27
    RES_1280X1024 = 28
    RES_1400X787 = 29
    RES_1400X875 = 30
    RES_1400X1050 = 31
    RES_1600X900 = 32
    RES_1600X1000 = 33
    RES_1600X1200 = 34
    RES_1920X1080 = 35

    __members__: Dict[str, ScreenResolution]


class AutomapMode(IntEnum):
    """
    Defines the automap rendering mode.
    """
    NORMAL = 0
    WHOLE = 1
    OBJECTS = 2
    OBJECTS_WITH_SIZE = 3

    __members__: Dict[str, AutomapMode]


class GameVariable(IntEnum):
    """
    Defines available game variables that can be accessed to get information about the game state.
    """
    KILLCOUNT = 0
    ITEMCOUNT = 1
    SECRETCOUNT = 2
    FRAGCOUNT = 3
    DEATHCOUNT = 4
    HITCOUNT = 5
    HITS_TAKEN = 6
    DAMAGECOUNT = 7
    DAMAGE_TAKEN = 8
    HEALTH = 9
    ARMOR = 10
    DEAD = 11
    ON_GROUND = 12
    ATTACK_READY = 13
    ALTATTACK_READY = 14
    SELECTED_WEAPON = 15
    SELECTED_WEAPON_AMMO = 16
    AMMO0 = 17
    AMMO1 = 18
    AMMO2 = 19
    AMMO3 = 20
    AMMO4 = 21
    AMMO5 = 22
    AMMO6 = 23
    AMMO7 = 24
    AMMO8 = 25
    AMMO9 = 26
    WEAPON0 = 27
    WEAPON1 = 28
    WEAPON2 = 29
    WEAPON3 = 30
    WEAPON4 = 31
    WEAPON5 = 32
    WEAPON6 = 33
    WEAPON7 = 34
    WEAPON8 = 35
    WEAPON9 = 36
    POSITION_X = 37
    POSITION_Y = 38
    POSITION_Z = 39
    ANGLE = 40
    PITCH = 41
    ROLL = 42
    VIEW_HEIGHT = 43
    VELOCITY_X = 44
    VELOCITY_Y = 45
    VELOCITY_Z = 46
    CAMERA_POSITION_X = 47
    CAMERA_POSITION_Y = 48
    CAMERA_POSITION_Z = 49
    CAMERA_ANGLE = 50
    CAMERA_PITCH = 51
    CAMERA_ROLL = 52
    CAMERA_FOV = 53
    PLAYER_NUMBER = 54
    PLAYER_COUNT = 55
    PLAYER1_FRAGCOUNT = 56
    PLAYER2_FRAGCOUNT = 57
    PLAYER3_FRAGCOUNT = 58
    PLAYER4_FRAGCOUNT = 59
    PLAYER5_FRAGCOUNT = 60
    PLAYER6_FRAGCOUNT = 61
    PLAYER7_FRAGCOUNT = 62
    PLAYER8_FRAGCOUNT = 63
    PLAYER9_FRAGCOUNT = 64
    PLAYER10_FRAGCOUNT = 65
    PLAYER11_FRAGCOUNT = 66
    PLAYER12_FRAGCOUNT = 67
    PLAYER13_FRAGCOUNT = 68
    PLAYER14_FRAGCOUNT = 69
    PLAYER15_FRAGCOUNT = 70
    PLAYER16_FRAGCOUNT = 71
    USER1 = 72
    USER2 = 73
    USER3 = 74
    USER4 = 75
    USER5 = 76
    USER6 = 77
    USER7 = 78
    USER8 = 79
    USER9 = 80
    USER10 = 81
    USER11 = 82
    USER12 = 83
    USER13 = 84
    USER14 = 85
    USER15 = 86
    USER16 = 87
    USER17 = 88
    USER18 = 89
    USER19 = 90
    USER20 = 91
    USER21 = 92
    USER22 = 93
    USER23 = 94
    USER24 = 95
    USER25 = 96
    USER26 = 97
    USER27 = 98
    USER28 = 99
    USER29 = 100
    USER30 = 101
    USER31 = 102
    USER32 = 103
    USER33 = 104
    USER34 = 105
    USER35 = 106
    USER36 = 107
    USER37 = 108
    USER38 = 109
    USER39 = 110
    USER40 = 111
    USER41 = 112
    USER42 = 113
    USER43 = 114
    USER44 = 115
    USER45 = 116
    USER46 = 117
    USER47 = 118
    USER48 = 119
    USER49 = 120
    USER50 = 121
    USER51 = 122
    USER52 = 123
    USER53 = 124
    USER54 = 125
    USER55 = 126
    USER56 = 127
    USER57 = 128
    USER58 = 129
    USER59 = 130
    USER60 = 131

    __members__: Dict[str, GameVariable]


class Button(IntEnum):
    """
    Defines available game buttons/actions that can be used to control the game.
    """
    ATTACK = 0
    USE = 1
    JUMP = 2
    CROUCH = 3
    TURN180 = 4
    ALTATTACK = 5
    RELOAD = 6
    ZOOM = 7
    SPEED = 8
    STRAFE = 9
    MOVE_RIGHT = 10
    MOVE_LEFT = 11
    MOVE_BACKWARD = 12
    MOVE_FORWARD = 13
    TURN_RIGHT = 14
    TURN_LEFT = 15
    LOOK_UP = 16
    LOOK_DOWN = 17
    MOVE_UP = 18
    MOVE_DOWN = 19
    LAND = 20
    SELECT_WEAPON1 = 21
    SELECT_WEAPON2 = 22
    SELECT_WEAPON3 = 23
    SELECT_WEAPON4 = 24
    SELECT_WEAPON5 = 25
    SELECT_WEAPON6 = 26
    SELECT_WEAPON7 = 27
    SELECT_WEAPON8 = 28
    SELECT_WEAPON9 = 29
    SELECT_WEAPON0 = 30
    SELECT_NEXT_WEAPON = 31
    SELECT_PREV_WEAPON = 32
    DROP_SELECTED_WEAPON = 33
    ACTIVATE_SELECTED_ITEM = 34
    SELECT_NEXT_ITEM = 35
    SELECT_PREV_ITEM = 36
    DROP_SELECTED_ITEM = 37
    LOOK_UP_DOWN_DELTA = 38
    TURN_LEFT_RIGHT_DELTA = 39
    MOVE_FORWARD_BACKWARD_DELTA = 40
    MOVE_LEFT_RIGHT_DELTA = 41
    MOVE_UP_DOWN_DELTA = 42

    __members__: Dict[str, Button]


class SamplingRate(IntEnum):
    """
    Defines available audio sampling rates.
    """
    SR_11025 = 0
    SR_22050 = 1
    SR_44100 = 2

    __members__: Dict[str, SamplingRate]


# --------------- [3] ViZDoom Classes ---------------
class Label:
    """Represents object labels in the game world with associated properties."""

    def __init__(self, /, *args, **kwargs) -> None:
        ...

    @property
    def object_id(self) -> int:
        ...

    @property
    def object_name(self) -> str:
        ...

    @property
    def value(self) -> int:
        ...

    @property
    def x(self) -> int:
        ...

    @property
    def y(self) -> int:
        ...

    @property
    def width(self) -> int:
        ...

    @property
    def height(self) -> int:
        ...

    @property
    def object_position_x(self) -> float:
        ...

    @property
    def object_position_y(self) -> float:
        ...

    @property
    def object_position_z(self) -> float:
        ...

    @property
    def object_angle(self) -> float:
        ...

    @property
    def object_pitch(self) -> float:
        ...

    @property
    def object_roll(self) -> float:
        ...

    @property
    def object_velocity_x(self) -> float:
        ...

    @property
    def object_velocity_y(self) -> float:
        ...

    @property
    def object_velocity_z(self) -> float:
        ...

class Object:
    """Represents objects in the game world with position and other properties."""

    def __init__(self, /, *args, **kwargs) -> None:
        ...

    @property
    def id(self) -> int:
        ...

    @property
    def name(self) -> str:
        ...

    @property
    def position_x(self) -> float:
        ...

    @property
    def position_y(self) -> float:
        ...

    @property
    def position_z(self) -> float:
        ...

    @property
    def angle(self) -> float:
        ...

    @property
    def pitch(self) -> float:
        ...

    @property
    def roll(self) -> float:
        ...

    @property
    def velocity_x(self) -> float:
        ...

    @property
    def velocity_y(self) -> float:
        ...

    @property
    def velocity_z(self) -> float:
        ...

class Line:
    """Represents line segments in the game world geometry."""

    def __init__(self, /, *args, **kwargs) -> None:
        ...

    @property
    def x1(self) -> float:
        ...

    @property
    def y1(self) -> float:
        ...

    @property
    def x2(self) -> float:
        ...

    @property
    def y2(self) -> float:
        ...

    @property
    def is_blocking(self) -> bool:
        ...

class Sector:
    """Represents sectors (floor/ceiling areas) in the game world geometry."""

    def __init__(self, /, *args, **kwargs) -> None:
        ...

    @property
    def floor_height(self) -> float:
        ...

    @property
    def ceiling_height(self) -> float:
        ...

    @property
    def lines(self) -> List[Line]:
        ...

class GameState:
    """Contains the state of the game including screen buffer, game variables, and world geometry."""

    def __init__(self, /, *args, **kwargs) -> None:
        ...

    @property
    def number(self) -> int:
        ...

    @property
    def tic(self) -> int:
        ...

    @property
    def screen_buffer(self) -> np.ndarray:
        ...

    @property
    def depth_buffer(self) -> Optional[np.ndarray]:
        ...

    @property
    def labels_buffer(self) -> Optional[np.ndarray]:
        ...

    @property
    def automap_buffer(self) -> Optional[np.ndarray]:
        ...

    @property
    def audio_buffer(self) -> Optional[np.ndarray]:
        ...

    @property
    def game_variables(self) -> Optional[np.ndarray]:
        ...

    @property
    def labels(self) -> List[Label]:
        ...

    @property
    def objects(self) -> List[Object]:
        ...

    @property
    def sectors(self) -> List[Sector]:
        ...

class ServerState:
    """Contains the state of the multiplayer server."""

    def __init__(self, /, *args, **kwargs) -> None:
        ...

    @property
    def tic(self) -> int:
        ...

    @property
    def player_count(self) -> int:
        ...

    @property
    def players_in_game(self) -> List[bool]:
        ...

    @property
    def players_frags(self) -> List[int]:
        ...

    @property
    def players_names(self) -> List[str]:
        ...

    @property
    def players_afk(self) -> List[bool]:
        ...

    @property
    def players_last_action_tic(self) -> List[int]:
        ...

    @property
    def players_last_kill_tic(self) -> List[int]:
        ...


class DoomGame:
    """
    DoomGame is the main class for interacting with ViZDoom.
    """
    def __init__(self, /, *args, **kwargs) -> None:
        """
        Initialize a new DoomGame instance.
        """
        ...

    def load_config(self, config_file: str) -> None:
        """
        Load configuration from a file.
        """
        ...

    def init(self) -> None:
        """
        Initialize the game.
        """
        ...

    def close(self) -> None:
        """
        Close the game.
        """
        ...

    def new_episode(self, recording_file_path: str = '') -> None:
        """
        Start a new episode.
        """
        ...

    def replay_episode(self, file_path: str, player: int = 0) -> None:
        """
        Replay an episode from a file.
        """
        ...

    def is_running(self) -> bool:
        """
        Check if the game is running.
        """
        ...

    def is_multiplayer_game(self) -> bool:
        """
        Check if this is a multiplayer game.
        """
        ...

    def is_recording_episode(self) -> bool:
        """
        Check if episode recording is enabled.
        """
        ...

    def is_replaying_episode(self) -> bool:
        """
        Check if episode replaying is active.
        """
        ...

    def set_action(self, action: object) -> None:
        """
        Set the action for the next tic.
        """
        ...

    def advance_action(self, tics: int = 1, update_state: bool = True) -> None:
        """
        Advance the game by a specified number of tics.
        """
        ...

    def make_action(self, action: object, tics: int = 1) -> float:
        """
        Make an action and advance the game.
        """
        ...

    def get_state(self) -> Optional[GameState]:
        """
        Get the current game state.
        """
        ...

    def get_last_reward(self) -> float:
        """
        Get the reward from the last action.
        """
        ...

    def get_total_reward(self) -> float:
        """
        Get the total reward for the current episode.
        """
        ...

    def is_episode_finished(self) -> bool:
        """
        Check if the current episode is finished.
        """
        ...

    def is_new_episode(self) -> bool:
        """
        Check if this is a new episode.
        """
        ...

    def is_player_dead(self) -> bool:
        """
        Check if the player is dead.
        """
        ...

    def respawn_player(self) -> None:
        """
        Respawn the player.
        """
        ...

    def send_game_command(self, command: str) -> None:
        """
        Send a command to the game console.
        """
        ...

    def get_mode(self) -> Mode:
        """
        Get the current game mode.
        """
        ...

    def set_mode(self, mode: Mode) -> None:
        """
        Set the game mode.
        """
        ...

    def get_ticrate(self) -> int:
        """
        Get the current ticrate.
        """
        ...

    def set_ticrate(self, ticrate: int) -> None:
        """
        Set the ticrate.
        """
        ...

    def set_doom_scenario_path(self, path: str) -> None:
        """
        Set the path to the Doom scenario file.
        """
        ...

    def set_doom_map(self, map_name: str) -> None:
        """
        Set the Doom map to use.
        """
        ...

    def set_doom_skill(self, skill: int) -> None:
        """
        Set the Doom skill level.
        """
        ...

    def set_doom_config_path(self, path: str) -> None:
        """
        Set the path to the Doom configuration file.
        """
        ...

    def set_vizdoom_path(self, path: str) -> None:
        """
        Set the path to the ViZDoom executable.
        """
        ...

    def set_doom_game_path(self, path: str) -> None:
        """
        Set the path to the Doom game executable.
        """
        ...

    def get_available_game_variables(self) -> List[GameVariable]:
        """
        Get the list of available game variables.
        """
        ...

    def set_available_game_variables(self, variables: List[GameVariable]) -> None:
        """
        Set the available game variables.
        """
        ...

    def add_available_game_variable(self, variable: GameVariable) -> None:
        """
        Add a game variable to the available variables.
        """
        ...

    def clear_available_game_variables(self) -> None:
        """
        Clear all available game variables.
        """
        ...

    def get_game_variable(self, variable: GameVariable) -> float:
        """
        Get the value of a specific game variable.
        """
        ...

    def get_available_game_variables_size(self) -> int:
        """
        Get the number of available game variables.
        """
        ...

    # Game arguments methods
    def set_game_args(self, args: str) -> None:
        """
        Sets game arguments.
        """
        ...

    def add_game_args(self, args: str) -> None:
        """
        Adds game arguments.
        """
        ...

    def clear_game_args(self) -> None:
        """
        Clear all game arguments.
        """
        ...

    def get_game_args(self) -> str:
        """
        Get current game arguments.
        """
        ...

    def get_available_buttons(self) -> List[Button]:
        """
        Get the list of available buttons.
        """
        ...

    def set_available_buttons(self, buttons: List[Button]) -> None:
        """
        Set the available buttons.
        """
        ...

    def add_available_button(self, button: Button, max_value: float = -1) -> None:
        """
        Add a button to the available buttons.
        """
        ...

    def clear_available_buttons(self) -> None:
        """
        Clear all available buttons.
        """
        ...

    def set_button_max_value(self, button: Button, max_value: float) -> None:
        """
        Set the maximum value for a button.
        """
        ...

    def get_button_max_value(self, button: Button) -> float:
        """
        Get the maximum value for a button.
        """
        ...

    def get_available_buttons_size(self) -> int:
        """
        Get the number of available buttons.
        """
        ...

    def get_button(self, button: Button) -> float:
        """
        Get the current value of a specific button.
        """
        ...

    def get_living_reward(self) -> float:
        """
        Get the living reward.
        """
        ...

    def set_living_reward(self, reward: float) -> None:
        """
        Set the living reward.
        """
        ...

    def get_death_penalty(self) -> float:
        """
        Get the death penalty.
        """
        ...

    def set_death_penalty(self, penalty: float) -> None:
        """
        Set the death penalty.
        """
        ...

    def get_last_action(self) -> list:
        """
        Get the last action performed.
        """
        ...

    def get_episode_timeout(self) -> int:
        """
        Get the episode timeout.
        """
        ...

    def set_episode_timeout(self, timeout: int) -> None:
        """
        Set the episode timeout.
        """
        ...

    def get_episode_start_time(self) -> int:
        """
        Get the episode start time.
        """
        ...

    def set_episode_start_time(self, time: int) -> None:
        """
        Set the episode start time.
        """
        ...

    def get_episode_time(self) -> int:
        """
        Get the current episode time.
        """
        ...

    def get_server_state(self) -> Optional[ServerState]:
        """
        Get the current server state.
        """
        ...

    def save(self, file_path: str) -> None:
        """
        Save the game state to a file.
        """
        ...

    def load(self, file_path: str) -> None:
        """
        Load the game state from a file.
        """
        ...

    def set_console_enabled(self, console: bool) -> None:
        """
        Enable or disable console.
        """
        ...

    def set_sound_enabled(self, sound: bool) -> None:
        """
        Enable or disable sound.
        """
        ...

    def is_audio_buffer_enabled(self) -> bool:
        """
        Check if audio buffer is enabled.
        """
        ...

    def set_audio_buffer_enabled(self, enabled: bool) -> None:
        """
        Enable or disable audio buffer.
        """
        ...

    def get_audio_sampling_rate(self) -> SamplingRate:
        """
        Get the audio sampling rate.
        """
        ...

    def set_audio_sampling_rate(self, rate: SamplingRate) -> None:
        """
        Set the audio sampling rate.
        """
        ...

    def get_audio_buffer_size(self) -> int:
        """
        Get the audio buffer size.
        """
        ...

    def set_audio_buffer_size(self, size: int) -> None:
        """
        Set the audio buffer size.
        """
        ...

    def is_depth_buffer_enabled(self) -> bool:
        """
        Check if depth buffer is enabled.
        """
        ...

    def set_depth_buffer_enabled(self, enabled: bool) -> None:
        """
        Enable or disable depth buffer.
        """
        ...

    def is_labels_buffer_enabled(self) -> bool:
        """
        Check if labels buffer is enabled.
        """
        ...

    def set_labels_buffer_enabled(self, enabled: bool) -> None:
        """
        Enable or disable labels buffer.
        """
        ...

    def is_automap_buffer_enabled(self) -> bool:
        """
        Check if automap buffer is enabled.
        """
        ...

    def set_automap_buffer_enabled(self, enabled: bool) -> None:
        """
        Enable or disable automap buffer.
        """
        ...

    def set_automap_mode(self, mode: AutomapMode) -> None:
        """
        Set the automap mode.
        """
        ...

    def set_automap_rotate(self, rotate: bool) -> None:
        """
        Set automap rotation.
        """
        ...

    def set_automap_render_textures(self, textures: bool) -> None:
        """
        Set automap texture rendering.
        """
        ...

    def set_render_hud(self, hud: bool) -> None:
        """
        Set HUD rendering.
        """
        ...

    def set_render_minimal_hud(self, hud: bool) -> None:
        """
        Set minimal HUD rendering.
        """
        ...

    def set_render_crosshair(self, crosshair: bool) -> None:
        """
        Set crosshair rendering.
        """
        ...

    def set_render_weapon(self, weapon: bool) -> None:
        """
        Set weapon rendering.
        """
        ...

    def set_render_decals(self, decals: bool) -> None:
        """
        Set decals rendering.
        """
        ...

    def set_render_particles(self, particles: bool) -> None:
        """
        Set particles rendering.
        """
        ...

    def set_render_effects_sprites(self, sprites: bool) -> None:
        """
        Set effects sprites rendering.
        """
        ...

    def set_render_messages(self, messages: bool) -> None:
        """
        Set messages rendering.
        """
        ...

    def set_render_corpses(self, corpses: bool) -> None:
        """
        Set corpses rendering.
        """
        ...

    def set_render_screen_flashes(self, flashes: bool) -> None:
        """
        Set screen flashes rendering.
        """
        ...

    def set_render_all_frames(self, all_frames: bool) -> None:
        """
        Set all frames rendering.
        """
        ...

    def get_screen_format(self) -> ScreenFormat:
        """
        Get the screen format.
        """
        ...

    def set_screen_format(self, format: ScreenFormat) -> None:
        """
        Set the screen format.
        """
        ...

    def set_screen_resolution(self, resolution: ScreenResolution) -> None:
        """
        Set the screen resolution.
        """
        ...

    def get_screen_width(self) -> int:
        """
        Get the screen width.
        """
        ...

    def get_screen_height(self) -> int:
        """
        Get the screen height.
        """
        ...

    def get_screen_channels(self) -> int:
        """
        Get the number of screen channels.
        """
        ...

    def get_screen_pitch(self) -> int:
        """
        Get the screen pitch.
        """
        ...

    def get_screen_size(self) -> int:
        """
        Get the screen size in bytes.
        """
        ...

    def set_window_visible(self, visible: bool) -> None:
        """
        Set window visibility.
        """
        ...

    def is_objects_info_enabled(self) -> bool:
        """
        Check if objects info is enabled.
        """
        ...

    def set_objects_info_enabled(self, enabled: bool) -> None:
        """
        Enable or disable objects info.
        """
        ...

    def is_sectors_info_enabled(self) -> bool:
        """
        Check if sectors info is enabled.
        """
        ...

    def set_sectors_info_enabled(self, enabled: bool) -> None:
        """
        Enable or disable sectors info.
        """
        ...

    def get_seed(self) -> int:
        """
        Get the random seed.
        """
        ...

    def set_seed(self, seed: int) -> None:
        """
        Set the random seed.
        """
        ...


# --------------- [4] ViZDoom Utility Functions ---------------
def doom_tics_to_ms(doom_tics: float, fps: int = 35) -> float:
    """
    Calculates how many tics will be made during given number of milliseconds.
    """
    ...


def ms_to_doom_tics(doom_tics: float, fps: int = 35) -> float:
    """
    Calculates the number of milliseconds that will pass during specified number of tics.
    """
    ...


def doom_tics_to_sec(doom_tics: float, fps: int = 35) -> float:
    """
    Calculates how many tics will be made during given number of seconds.
    """
    ...


def sec_to_doom_tics(doom_tics: float, fps: int = 35) -> float:
    """
    Calculates the number of seconds that will pass during specified number of tics.
    """
    ...


def doom_fixed_to_float(doom_fixed: Union[int, float]) -> float:
    """
    Converts fixed point numeral to a floating point value.
    Doom engine internally use fixed point numbers.
    """
    ...


def doom_fixed_to_double(doom_fixed: Union[int, float]) -> float:
    """
    Converts fixed point numeral to a floating point value.
    Doom engine internally use fixed point numbers.
    """
    ...


def is_binary_button(button: Button) -> bool:
    """
    Returns True if Button is binary button.
    """
    ...


def is_delta_button(button: Button) -> bool:
    """
    Returns True if Button is delta button.
    """
    ...


# --------------- [5] ViZDoom Global Enum Variables ---------------

RES_160X120: ScreenResolution

RES_200X125: ScreenResolution

RES_200X150: ScreenResolution

RES_256X144: ScreenResolution

RES_256X160: ScreenResolution

RES_256X192: ScreenResolution

RES_320X180: ScreenResolution

RES_320X200: ScreenResolution

RES_320X240: ScreenResolution

RES_320X256: ScreenResolution

RES_400X225: ScreenResolution

RES_400X250: ScreenResolution

RES_400X300: ScreenResolution

RES_512X288: ScreenResolution

RES_512X320: ScreenResolution

RES_512X384: ScreenResolution

RES_640X360: ScreenResolution

RES_640X400: ScreenResolution

RES_640X480: ScreenResolution

RES_800X450: ScreenResolution

RES_800X500: ScreenResolution

RES_800X600: ScreenResolution

RES_1024X576: ScreenResolution

RES_1024X640: ScreenResolution

RES_1024X768: ScreenResolution

RES_1280X720: ScreenResolution

RES_1280X800: ScreenResolution

RES_1280X960: ScreenResolution

RES_1280X1024: ScreenResolution

RES_1400X787: ScreenResolution

RES_1400X875: ScreenResolution

RES_1400X1050: ScreenResolution

RES_1600X900: ScreenResolution

RES_1600X1000: ScreenResolution

RES_1600X1200: ScreenResolution

RES_1920X1080: ScreenResolution

NORMAL: AutomapMode

WHOLE: AutomapMode

OBJECTS: AutomapMode

OBJECTS_WITH_SIZE: AutomapMode

KILLCOUNT: GameVariable

ITEMCOUNT: GameVariable

SECRETCOUNT: GameVariable

FRAGCOUNT: GameVariable

DEATHCOUNT: GameVariable

HITCOUNT: GameVariable

HITS_TAKEN: GameVariable

DAMAGECOUNT: GameVariable

DAMAGE_TAKEN: GameVariable

HEALTH: GameVariable

ARMOR: GameVariable

DEAD: GameVariable

ON_GROUND: GameVariable

ATTACK_READY: GameVariable

ALTATTACK_READY: GameVariable

SELECTED_WEAPON: GameVariable

SELECTED_WEAPON_AMMO: GameVariable

AMMO0: GameVariable

AMMO1: GameVariable

AMMO2: GameVariable

AMMO3: GameVariable

AMMO4: GameVariable

AMMO5: GameVariable

AMMO6: GameVariable

AMMO7: GameVariable

AMMO8: GameVariable

AMMO9: GameVariable

WEAPON0: GameVariable

WEAPON1: GameVariable

WEAPON2: GameVariable

WEAPON3: GameVariable

WEAPON4: GameVariable

WEAPON5: GameVariable

WEAPON6: GameVariable

WEAPON7: GameVariable

WEAPON8: GameVariable

WEAPON9: GameVariable

POSITION_X: GameVariable

POSITION_Y: GameVariable

POSITION_Z: GameVariable

ANGLE: GameVariable

PITCH: GameVariable

ROLL: GameVariable

VIEW_HEIGHT: GameVariable

VELOCITY_X: GameVariable

VELOCITY_Y: GameVariable

VELOCITY_Z: GameVariable

CAMERA_POSITION_X: GameVariable

CAMERA_POSITION_Y: GameVariable

CAMERA_POSITION_Z: GameVariable

CAMERA_ANGLE: GameVariable

CAMERA_PITCH: GameVariable

CAMERA_ROLL: GameVariable

CAMERA_FOV: GameVariable

USER1: GameVariable

USER2: GameVariable

USER3: GameVariable

USER4: GameVariable

USER5: GameVariable

USER6: GameVariable

USER7: GameVariable

USER8: GameVariable

USER9: GameVariable

USER10: GameVariable

USER11: GameVariable

USER12: GameVariable

USER13: GameVariable

USER14: GameVariable

USER15: GameVariable

USER16: GameVariable

USER17: GameVariable

USER18: GameVariable

USER19: GameVariable

USER20: GameVariable

USER21: GameVariable

USER22: GameVariable

USER23: GameVariable

USER24: GameVariable

USER25: GameVariable

USER26: GameVariable

USER27: GameVariable

USER28: GameVariable

USER29: GameVariable

USER30: GameVariable

USER31: GameVariable

USER32: GameVariable

USER33: GameVariable

USER34: GameVariable

USER35: GameVariable

USER36: GameVariable

USER37: GameVariable

USER38: GameVariable

USER39: GameVariable

USER40: GameVariable

USER41: GameVariable

USER42: GameVariable

USER43: GameVariable

USER44: GameVariable

USER45: GameVariable

USER46: GameVariable

USER47: GameVariable

USER48: GameVariable

USER49: GameVariable

USER50: GameVariable

USER51: GameVariable

USER52: GameVariable

USER53: GameVariable

USER54: GameVariable

USER55: GameVariable

USER56: GameVariable

USER57: GameVariable

USER58: GameVariable

USER59: GameVariable

USER60: GameVariable

PLAYER_NUMBER: GameVariable

PLAYER_COUNT: GameVariable

PLAYER1_FRAGCOUNT: GameVariable

PLAYER2_FRAGCOUNT: GameVariable

PLAYER3_FRAGCOUNT: GameVariable

PLAYER4_FRAGCOUNT: GameVariable

PLAYER5_FRAGCOUNT: GameVariable

PLAYER6_FRAGCOUNT: GameVariable

PLAYER7_FRAGCOUNT: GameVariable

PLAYER8_FRAGCOUNT: GameVariable

PLAYER9_FRAGCOUNT: GameVariable

PLAYER10_FRAGCOUNT: GameVariable

PLAYER11_FRAGCOUNT: GameVariable

PLAYER12_FRAGCOUNT: GameVariable

PLAYER13_FRAGCOUNT: GameVariable

PLAYER14_FRAGCOUNT: GameVariable

PLAYER15_FRAGCOUNT: GameVariable

PLAYER16_FRAGCOUNT: GameVariable

ATTACK: Button

USE: Button

JUMP: Button

CROUCH: Button

TURN180: Button

ALTATTACK: Button

RELOAD: Button

ZOOM: Button

SPEED: Button

STRAFE: Button

MOVE_RIGHT: Button

MOVE_LEFT: Button

MOVE_BACKWARD: Button

MOVE_FORWARD: Button

TURN_RIGHT: Button

TURN_LEFT: Button

LOOK_UP: Button

LOOK_DOWN: Button

MOVE_UP: Button

MOVE_DOWN: Button

LAND: Button

SELECT_WEAPON1: Button

SELECT_WEAPON2: Button

SELECT_WEAPON3: Button

SELECT_WEAPON4: Button

SELECT_WEAPON5: Button

SELECT_WEAPON6: Button

SELECT_WEAPON7: Button

SELECT_WEAPON8: Button

SELECT_WEAPON9: Button

SELECT_WEAPON0: Button

SELECT_NEXT_WEAPON: Button

SELECT_PREV_WEAPON: Button

DROP_SELECTED_WEAPON: Button

ACTIVATE_SELECTED_ITEM: Button

SELECT_NEXT_ITEM: Button

SELECT_PREV_ITEM: Button

DROP_SELECTED_ITEM: Button

LOOK_UP_DOWN_DELTA: Button

TURN_LEFT_RIGHT_DELTA: Button

MOVE_FORWARD_BACKWARD_DELTA: Button

MOVE_LEFT_RIGHT_DELTA: Button

MOVE_UP_DOWN_DELTA: Button

SR_11025: SamplingRate

SR_22050: SamplingRate

SR_44100: SamplingRate
