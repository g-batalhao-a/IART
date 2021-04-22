import copy

class Tube:
    def __init__(self, balls: list = None, capacity: int = 4) -> None:
        """Initializes Tube

        Args:
            balls (list, optional): List with the balls. Defaults to [].
            capacity (int, optional): Capacity of a tube. Defaults to 4.
        """
        if balls is None:
            balls = []

        self.capacity = capacity
        self.balls = balls

    def is_empty(self):
        """Check if tube is empty

        Returns:
            boolean: True if empty, False otherwise
        """
        return len(self.balls) == 0

    def is_full(self):
        """Check if tube is full

        Returns:
            boolean: True if full, False otherwise
        """
        return len(self.balls) == self.capacity

    def get_ball(self):
        """Get the ball from the top of the tube

        Returns:
            int: Ball from the top
        """
        return self.balls[-1]


    def remove_ball(self):
        """Removes the top ball of a tube

        Returns:
            int: Removed ball
        """
        top_ball = self.get_ball()
        self.balls = self.balls[:-1]
        return top_ball

    def all_same_colored(self):
        """Check if all the balls in the tube have the same color

        Returns:
            boolean: True if the balls have the same color, False otherwise
        """
        for i in range(1, len(self.balls)):
            if self.balls[i] != self.balls[i - 1]:
                return False
        return True


    def put_ball(self, ball):
        """Put ball in tube

        Args:
            ball (int): New ball

        Returns:
            boolean: True if the ball was put in the tube, False if the tube was already full
        """
        if self.is_full():
            return False
        self.balls.append(ball)
        return True

    def print(self, place: int):
        """Print a tube

        Args:
            place (int): Height of the tube to print
        """
        try:
            print("|", self.balls[place], "|", end="")
        except:
            print("|   |", end="")

    def is_completed(self):
        """Check if tube is completed

        Returns:
            boolean: True if tube is completed, False otherwise
        """
        return self.all_same_colored() and self.is_full()

    def get_balls(self):
        return self.balls


class Game:
    def __init__(self, tubes: list) -> None:
        self.tubes=[]
        for tube in tubes:
            self.tubes.append(Tube(tube))

    def finished(self):
        """Checks if the game is finished

        Returns:
            boolean: True if the game is finished, False otherwise
        """
        completed_tubes = 0
        for tube in self.tubes:
            if tube.is_completed():
                completed_tubes += 1
        return completed_tubes == self.num_of_colors

    def move_ball(self, from_i: int, to_i: int):
        """Moves a ball from a tube to another

        Args:
            from_i (int): Index of the tube to remove the ball
            to_i (int): Index of the tube to put the ball

        Returns:
            boolean: True if the ball was moved, False otherwise
        """
        if self.tubes[from_i].is_empty() or self.tubes[to_i].is_full() or (
                not self.tubes[to_i].is_empty() and (self.tubes[from_i].get_ball() != self.tubes[to_i].get_ball())):
            return False
        else:
            return self.tubes[to_i].put_ball(self.tubes[from_i].remove_ball())


    def print(self):
        """Print a game state
        """
        for places in range(3, -1, -1):
            for tube in self.tubes:
                tube.print(places)
            print("")

        print(" --- " * len(self.tubes))

    # IF INVALID STATE_: -10 
    # FOR EACH TUBE:
    #  - COUNT BALLS OF SAME COLOUR FROM BOTTOM TOP, 1*consecutive balls
    #  - COUNT NUMBER OF INCORRECTLY PLACED BALLS (not sure of this): -1
    def evaluate(self):
        reward = 0

        for tube in self.gamestate.tubes:
            balls = tube.balls.copy()

            if len(balls) == 0: continue

            idx = next((i for i, v in enumerate(balls) if v != balls[0]), -1)
            if idx == -1: reward +=len(balls)

            balls = balls[idx:]
            reward -= len(balls)

        return reward

    def to_list(self):
        list=[]
        for tube in self.tubes:
            list.append(tube.get_balls())


