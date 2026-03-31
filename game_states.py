from state_machine import State


# State used while the collision test is actively running and updating.
class GamePlayingState(State):
    def __init__(self, game):
        self.game = game

    def get_state_name(self):
        return "playing"

    def enter(self):
        # marks the game as actively running gameplay
        self.game.playing = True

    def exit(self):
        pass

    def update(self):
        # only while playing do we update sprite movement and collision status
        self.game.all_sprites.update()
        self.game.update_collision_state()


# State used when movement is frozen but the game is still open.
class GamePausedState(State):
    def __init__(self, game):
        self.game = game

    def get_state_name(self):
        return "paused"

    def enter(self):
        # paused stops gameplay updates but still allows UI and event handling
        self.game.playing = False

    def exit(self):
        pass

    def update(self):
        # no gameplay update while paused
        pass


# State used for the title / start screen before the collision test begins.
class GameStartState(State):
    def __init__(self, game):
        self.game = game

    def get_state_name(self):
        return "start"

    def enter(self):
        # start screen waits for the player to begin the run
        self.game.playing = False

    def exit(self):
        pass

    def update(self):
        # start screen also waits for input instead of updating gameplay
        pass
