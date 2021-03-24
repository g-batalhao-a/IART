import copy


class Tube:
    def __init__(self, balls: list = [], capacity: int = 4) -> None:
        self.capacity = capacity
        self.balls = balls

    def is_empty(self):
        return len(self.balls) == 0

    def is_full(self):
        return len(self.balls) == self.capacity

    def get_ball(self):
        return self.balls[-1]

    def get_num_of_balls(self):
        return len(self.balls)

    def get_balls(self):
        return self.balls

    def remove_ball(self):
        top_ball = self.get_ball()
        self.balls = self.balls[:-1]
        return top_ball

    def all_same_colored(self):
        for i in range(1, len(self.balls)):
            if self.balls[i] != self.balls[i - 1]:
                return False
        return True

    def __eq__(self, other):
        return self.balls == other.balls

    def put_ball(self, ball):
        if self.is_full():
            return False
        self.balls.append(ball)

    def print(self, place: int):
        try:
            print("|", self.balls[place], "|", end="")
        except:
            print("|   |", end="")

    def clone(self):
        return copy.deepcopy(self)

################### added to work with UI #####################
    def put_ball_r(self, ball):
        if self.is_full():
            return False
        self.balls.append(ball)
        return True

    def is_completed(self):
        return self.all_same_colored() and self.is_full()


class Game:
    def __init__(self, tubes: list) -> None:
        self.tubes = tubes
        self.num_of_colors = self.calculate_colors()

    def calculate_colors(self):
        colors = set()
        for tube in self.tubes:
            balls = tube.get_balls()
            for ball in balls:
                colors.add(ball)
        return len(colors)

    def completed_tube(self, tube: Tube):
        return tube.all_same_colored() and tube.is_full()

    def finished(self):
        completed_tubes = 0
        for tube in self.tubes:
            if self.completed_tube(tube):
                completed_tubes += 1
        return completed_tubes == self.num_of_colors

    def expand(self):
        moves = []
        for to_index in range(0, len(self.tubes)):
            if self.tubes[to_index].is_full():
                continue
            from_indexes = self.find_moves_from_tube(to_index)
            for from_idx in from_indexes:
                moves.append((from_idx, to_index))
        return moves

    def find_moves_from_tube(self, to_index: int):
        indexes = []
        to_tube = self.tubes[to_index]
        for from_index in range(0, len(self.tubes)):
            if from_index == to_index:
                continue
            if self.tubes[from_index].is_empty():
                continue
            if to_tube.is_empty() or self.tubes[from_index].get_ball() == to_tube.get_ball():
                indexes.append(from_index)
        return indexes

    def move_ball(self, from_i: int, to_i: int):
        (self.tubes[to_i]).put_ball(self.tubes[from_i].remove_ball())

    def get_tubes(self):
        return self.tubes



    def __eq__(self, other):
        for tube in self.tubes:
            if tube not in other.tubes:
                return False
        return True

    def print(self):
        for places in range(3, -1, -1):
            for tube in self.tubes:
                tube.print(places)
            print("")

        print(" --- " * len(self.tubes))

    def clone(self):
        return copy.deepcopy(self)




################### added to work with UI #####################
    def move_ball_r(self, from_i: int, to_i: int):
        if self.tubes[from_i].is_empty() or self.tubes[to_i].is_full() or (not self.tubes[to_i].is_empty() and (self.tubes[from_i].get_ball() != self.tubes[to_i].get_ball())):
            return False
        else:
             return self.tubes[to_i].put_ball_r(self.tubes[from_i].remove_ball())
            
