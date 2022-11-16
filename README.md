# sudoku2

In the second iteration of my sudoku project, I built a GUI from scratch with PyGame. Documentation for the first version is located <a href="https://github.com/pkulavic/sudoku1">here</a>, though I have not worked on it in a while.

![Screenshot 1](images/sudoku2-sc1.png)
Screenshot of the desktop GUI I created. 

## Overview
This summer, I created a <a href="https://github.com/pkulavic/sudoku2/blob/master/engine.py">Python class</a> that randomly generated sudoku puzzles, but I had no way to visualize or play them. When I found out about <a href="https://www.pygame.org/docs/">PyGame</a>, it seemed like a plausible solution, so I decided to dive in to my first GUI project.

## Design
I stole the design for this app from the <a href="https://www.nytimes.com/puzzles/sudoku/easy">New York Times</a>' online sudoku page, because this project focused on UI implementation, not UI <em>design</em>. Although I will eventually design my own UI for this project, I wanted this version to challenge me to implement a UI according to a predetermined specification, instead of making it up as I went along. Even though I began with a well-defined spec, it was not immediately obvious to me how I would implement it. As I would soon learn, PyGame and JavaScript-based web apps have very little in common.

## Development Process: Challenges and Solutions
