# Mars rover kata

## Your Task

You're part of the team that explores Mars by sending remotely controlled vehicles to the surface of the planet. Develop an API that translates the commands sent from earth to instructions that are understood by the rover.

## Requirements
You are given the initial starting point (x,y) of a rover and the direction (N,S,E,W) it is facing.
The rover receives a character array of commands.
- Implement commands that move the rover forward/backward (f,b).
- Implement commands that turn the rover left/right (l,r). <-- **StartHere**
- Implement wrapping from one edge of the grid to another. (planets are spheres after all)
- Implement obstacle detection before each move to a new square. If a given sequence of commands encounters an obstacle, the rover moves up to the last possible point, aborts the sequence and reports the obstacle.

#

## My notes

### Rover:

- Description:

    - Position_x
    - Position_y
    - Orientation

- Actions defined by a character **array**:
    - Functions such as:
        ```
        move_forward
        move_backward
        turn_left
        turn_right
        ```
        Might not be needed unless private.

    - Instead use:
        ```
        move(f or b), move(fbfbfb)
        turn(l or r), turn(lrlrlr)
        ```

    - Special cases:
        ```
        if command list is empty: do nothing
        if command list contains some char not in ( 'f','b','l','r' ):
            do nothing/throw exception

        move     affected by obstacles
        turn NOT affected by obstacles
        ```

    - Two actions move & turn:
        - Move: forward/backward, already implemented?

        - Turn: left/right

            We can do:
            ```
            orientation_map = "NESW"
            orientation = 0 # index
            turn_right:
                orientation = (orientation + 1) % len(orientation_map)
            turn_left:
                orientation -= 1
                if orientation < 0:
                    orientation += len(orientation_map)
                ... or pythonesque ...
                orientation = (orientation - 1) % len(orientation_map)
            __str__/get_name:
                return orientation_map[orientation]
            ```
            instead of:
            ```
            turn_right:
                if   "N" then "E"
                elif "E" then "S"
                elif "S" then "W"
                ...
            ```

        - Doubts:

            - Current implementation of `move`, can we modify it?
                ```
                move(movs):
                    for m in movs: move rover with m
                ```

            - Then the `turn` must also be (?):
                ```
                turn(turns):
                    for t in turns: turn rover with t
                ```

            - Do we need something like?
                ```
                move(m): move rover with m
                turn(t): turn rover with t
                ```

            - Do we want to move+turn+move+turn+move+turn...?
                ```
                move_or_turn(commands):
                    for c in commands:
                        if c in 'fb': move rover with c
                        if c in 'lr': turn rover with c
                ```

### Planet (not specified):

- Call it Planet instead of Grid
- Description:
    - Size 2D HxW
    - Contents:
        ```
        '.': empty cell, can move
        'o': obstacle
        ```

### Thoughts:
- Rover actions called on a planet:
    - Which is best?

    ```
        rover.move(planet, 'ffff')

        ... or ...

        rover.planet = planet
        rover.move('ffff')

        ... or ...

        planet.rover = rover
        planet.rover.move('ffff')

        ... or ...

        planet.rover = rover
        planet.move('ffff')
    ```

    - Assume:
        1. You are moving a rover, not the planet.
        1. A rover can be on only one planet at the time.
        2. But a planet might contain multiple rovers (?).

        This means:

        - [x] A rover must be linked to a planet on definition, or
        - [ ] A planet contains a list of rovers, then call `planet.move(rover_id, commands)`, or
        - [ ] Create a Context class

- Problem requirements:

    1. Implement wrapping from one edge of the grid to another. (planets are spheres after all)

        What does this mean?

        - Idea-1:
        ```
            orientation=E before & after 1st move
            ...              ...              ...
            ..r -> move f -> r.. -> move f -> .r.
            ...              ...              ...

            orientation=S before & after 1st move
            ...              .r.              ...
            ... -> move f -> ... -> move f -> .r.
            .r.              ...              ...
        ```

        But if 'planets are spheres', can we do this:

        - Idea-2:
        ```
            orientation=E before move, orientation=W after 1st move
            ...              ...              ...
            ..r -> move f -> ..r -> move f -> .r.
            ...              ...              ...

            orientation=S before move, orientation=N after 1st move
            ...              ...              ...
            ... -> move f -> ... -> move f -> .r.
            .r.              .r.              ...
        ```
        as if we had two planes of the grid?

        Will implement **Idea-1**, Idea-2 has no sense.

        The wrapping is basically doing:
        ```
            rover.pos_x = (rover.pos_x + 1) % planet.size_x
            rover.pos_x = (rover.pos_x - 1) % planet.size_x
        ```
        This is, no bound-checking is needed.

    2. Implement obstacle detection before each move to a new square. If a given sequence of commands encounters an obstacle, the rover moves up to the last possible point, aborts the sequence and reports the obstacle.

        This means:
        1. If the move with command_i is possible:
            1. Move the rover.
            2. Update the position.
        2. If not (obstacle found at next position):
            1. Do not update the position.
            1. Abort the rest of commands (from command_{i+1}..N).
            2. Report a warning.
            3. Finish.

        This line: 'the rover moves up to the last possible point'...

        - Can we ignore the obstacle (by not moving to that position) and keep moving until the last possible point? **We cannot because it is stated to 'abort the SEQUENCE of commands' and not just 'abort the COMMAND'**.

### Design:
- Position
    - Notes:
        - Simple 2D coordinate

- Orientation
    - Notes:
        - ~~Make class~~
        - ~~Make enum+methods~~
        - ~~Make within Rover~~
    - Attributes:
    - ~~Constructor~~ Enum:
        - North, South, East, West
    - Methods:

- ~~OrientationUtils~~
    - ~~Notes:~~
        - ~~Uses Orientation and turns it in a defined direction~~
        - ~~Static class~~
    - ~~Attributes: auxiliar maps~~
    - ~~Methods:~~
        - ~~turn_orientation(turn, orientation): return orientation+turn~~

- Direction:
    - Attributes:
        - position
        - orientation
        - priv limit_x = -1, used to wrap only if > 0
        - priv limit_y = -1
    - Constructor:
        - [x] Direction(pos_x, pos_y, enum Orientation)
        - Direction(obj Position, enum Orientation)
        - We can overload
    - Methods:
        - private:
            - move
            - turn
        - public:
            - next_position_forward
            - next_position_backward
            - next_orientation_left
            - next_orientation_right
    - Notes:
        - ~~If just the Rover knows where is it moving, I cannot call `move` or `turn` as public.~~
        - Move action will be:
            ```
            position.x = (position.x + 1)
            if limit_x > 0: # ... > 0 | >= 0
                position.x = position.x % limit_x
            ```
            This is, apply the clamp only when the limit is defined.

            ValueErrors if limits <= 0.

- Obstacle:
    - Notes:
        - Position type alias, we do not need more attributes

- Planet
    - Attributes:
        - size_x: grid width
        - size_y: grid height
        - ~~grid: 2D-matrix of chars '.' and 'o'~~
            - Too many restrictions
            - What if we just passed a list of coordinates of the obstacles?
    - Constructor:
        - ~~Planet(grid)~~
        - Planet(size_x, size_y, obstacles: List[Obstacle] = [])
            - Better than a list of int tuples to distinguish pos_x, pos_y
            - Somehow must be asserted that obstacles are within size_x, size_y, but it is not the Planet's job
    - Methods:
        - build(...): to random fill?
        - ~~is_inside_bounds(test_x, test_y): return if 0 <= (test_x, test_y) < (size_x, size_y)~~
        - has_obstacle_at(obs): return True if ~~grid[test_y][test_x] == 'o'~~ any (obs in obstacles) else False

- Commands
    - Enum, only known to rover

- Rover
    - Attributes:
        - direction: Direction object
        - planet: Planet object
    - Constructor:
        - Rover(pos_x, pos_y, orientation)?
        - Rover(direction)?
            - Is it possible to build a rover without a planet?
            - Can we move/turn if there is no planet?
        - Rover(pos_x, pos_y, orientation, planet)
        - [x] Rover(direction, planet)
    - Methods:
        - move(move_commands):
            - Logic:
                1. calc next pos
                2. if planet allows it:
                    - update pos
                3. else:
                    - print warn
                    - abort&finish
            - Pseudo-coded logic
            ```
            next_position = self.direction.next_position()
            if planet.has_obstacle_at(next_position):
                print("warn")
                break
            self.direction.update_position(next_position)
            ...
            Direction::next_position():
                move_x, move_y = ...
                next_position = Position()
                next_position.x = (self.position.x + move_x) % limit_x
                next_position.y = (self.position.y + move_y) % limit_y
                return next_position
                ...
            Direction::update_position(other_position=None):
                if other_position is not None:
                    self.position = other_position
                else: # ... maybe ...
                    self.position = self.next_position()
            ```
            - Logic doubt:
                - How does the Direction know the limit_x, limit_y?
                    - [ ] `direction.next_position(planet.limit_x, planet.limit_y)`
                        - Too many parameters, the limit's will probably always be the same.
                    - [x] Inside Direction's constructor `direction.set_limit_x(planet.limit_x)`
        - turn(turn_commands):
            - What tells me that "N"+turn_right = "E"?
                - [ ] ~~Orientation class~~
                    - Why? Because of an orientation sequence/order.
                    - Use static class?
                - [x] Direction class
                    - `rover.direction.turn_{left/right}()`
                - [ ] Rover class
                - [ ] Other class
                - [ ] ???
        - Do we need process(move_and_turn_commands)?
        - move_commands and turn_commands format:
            - List[str]: ['f','f','f']
            - str: 'fff'
            - Ignore with _Duck typing_?
    - Notes:
        - Keep the
            ```
            if cmd == 'f'
            if cmd == 'b'
            ...
            ```
            logic with the Rover class, instead of Orientation/Utils.

- (optional)
    - PlanetBuilder
