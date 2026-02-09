MOVES = {'R': (1,0), 'L': (-1, 0), 'U': (0, -1), 'D': (0, 1)}
REVERSED_COMMANDS = {'R': 'L', 'L': 'R', 'U': 'D', 'D': 'U'}

class Field:
    def __init__(self):
        self.danger_zones = []

    def add_danger_zone(self, data):
        self.danger_zones.append(data)

    def is_valid_position(self, x, y):
        if not( 1 <= x <= 100 and 1 <= y <= 100 ):
            raise ValueError("Выход за границы поля")
        
        for x1, y1, x2, y2 in self.danger_zones:
            if x1 <= x <= x2 + x1 and y1 <= y <= y2 + y1:
                raise ValueError("Вход на запретную территорию")
            
        return True

class Robot:
    def __init__(self, field):
        self.x = 1
        self.y = 1

        self.commands = []
        self.position_history = [(1,1)]

        self.field = field

    def add_command(self, data):
        self.commands.append(data)

        print(self.commands)

    def parse_commands(self):
        self.commands.reverse()

        for i in range(len(self.commands)):
            if self.commands[i][0] == 'B':
                temp = [x for x in self.commands[i+1:] if x[0] != 'B']
                self.commands[i:i+1] = Robot.reverse_command(temp[:self.commands[i][1]])

        self.commands.reverse()

    @staticmethod
    def reverse_command(data):
        result = []

        for i in range(len(data)):
            result.append( (REVERSED_COMMANDS[data[i][0]], data[i][1]) )

        return result

    def run(self):
        self.parse_commands()

        for i, j in self.commands:
            for _ in range(j):
                dx, dy = MOVES[i]

                if field.is_valid_position(self.x + dx, self.y + dy):
                    self.x += dx
                    self.y += dy

                    self.position_history.append( (self.x, self.y) )


        for x, y in self.position_history:
            print(f"{x},{y}")

field = Field()
robot = Robot(field)

print("Введите запретные зоны (x,y,h,w):")
while True:
    line = input().strip()

    if not line: break

    data = tuple(map(int, line.split(',')))
    field.add_danger_zone(data)

print("Команды:")
while True:
    line = input().strip()

    if not line: break

    s_line = line.split(',')

    if len(s_line) == 1:
        robot.add_command( (s_line[0].upper(), 1) )
        continue

    robot.add_command( (s_line[0].upper(), int(s_line[1])) )

robot.run()