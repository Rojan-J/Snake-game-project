# STEP 1
## Basics of the Snake Game: 
Design a grid within which the snake can move and eat fruits.

# STEP 2
## Graphical Options
Enhance the game with features like a background, sound effects, and more.

### Features:
- Blinking Snake and Tongue Animation: The snake blinks and displays a tongue animation for added visual appeal.
- Background: Customizable backgrounds for the game.
- Start Page: Includes a "Start" button and a tutorial. Clicking "Start" begins the game, while clicking "Tutorial" puts the game in an automatic mode where the snake moves on its own.
- Different Fruits: Multiple fruit types with varying scores.
- Bonus: A special pepper bonus. If the snake eats it, it "burns," and the snake moves automatically.
- Score Display: The total score is displayed at the top of the screen. After eating a fruit, the points gained are briefly shown.
- Sounds: Engaging background music is added for the start and settings pages, along with sound effects for eating fruits.
- Settings Page: Users can customize the background color, snake color, and game difficulty.

# STEP 3
## A* Algorithm
We have implemented the A* algorithm to enable the snake to find its path to the fruit. You can see this algorithm in action in two scenarios:

1. By clicking on the "Tutorial" button.
2. By eating the pepper bonus on the main page.

In these scenarios, the snake moves faster and not only finds its path but also visually displays the planned route.

Additionally, we have implemented a backup path mechanism. If the snake cannot find a direct path to the fruit, it takes a path with the most free space until a valid path to the fruit becomes available.

