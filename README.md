# Among Us Polus Maze Task

Uh oh... it's the dreaded Maze Task again... yep! I coded the Among Us Maze Task in Python using the Tkinter package as the GUI. To use this application, first fork it, then run

```
python maze.py
```

on your local terminal.

### How to use
- The size of your maze is given by what you input for the height and width. The default is height=7, width=19, which has proportions most similar to an actual Among Us maze.
- Start by dragging your mouse from the top left of the window towards the bottom right. Avoid obstacles! 
- You cannot return to a square you have already visited. Sometimes, the program will glitch and thinks you visited a square you haven't; just release your mouse to reset the maze.
- Once you reach the bottom right, you will be prompted with a "Congratulations!" screen, which will show the time it took you to complete the maze.
- Click one of the buttons on the screen accordingly to be returned to the same/a different maze.
- To try a maze with different dimensions, close out of the window and re-run the script.
- If you are interested in the data for the maze generation (number of retries, length of path, number of barriers), it is printed to your terminal.

### Strengths
- Flexibility, you are able to input variable heights and widths.
- Simple, the arithmetic and code is not very complicated to understand and modify.
- Understandable, I tried to document the code as best as possible for anyone to understand the functionality.

### For reproduction/future work
- The maze.py file is the driver code for the game, the algo.py file consists of the Depth-first search algorithm that was used to find possible maze configurations.
- Turn self.debug to true for certain print statements to appear for more convenient debugging.
- Images could be more precise (minimize whitespace); the obstacles don't have the exact same proportions as the ones in Among Us.
- Mouse movements:
  - Mouse sensitivity is not great
  - Yellow trail is oftentimes glitchy
  - Ability to skip corners is problematic
  - Visiting squares that haven't been visited can break the game sometimes
- The main limitation is definitely that this is not a web application; unfortunately, Tkinter is not integrable into Flask or any other web application building language. 
- Converting the game logic into a dynamic front-end language, like React or Vue, would be the best way for this project to progress vertically. If anyone has suggestions
or would like to collaborate, please let me know!
