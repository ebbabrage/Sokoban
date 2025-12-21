%Initiate board: walls, open space
%XXXXXX
%XPOCGX
%XXCXXX
%XXGXXX
%XXXXXX

%if it is a w then create a cell(x,y,wall) otherwise cell(x,y,open)
cell(0,0,wall) . cell(0,1,wall) . cell(0,2,wall) . cell(0,3,wall) . cell(0,4,wall) . cell(0,5,wall) .
cell(1,0,wall) . cell(1,1,open) . cell(1,2,open) . cell(1,3,open) . cell(1,4,open) . cell(1,5,wall) .
cell(2,0,wall) . cell(2,1,wall) . cell(2,2,open) . cell(2,3,wall) . cell(2,4,wall) . cell(2,5,wall) .
cell(3,0,wall) . cell(3,1,wall) . cell(3,2,open) . cell(3,3,wall) . cell(3,4,wall) . cell(3,5,wall) .
cell(4,0,wall) . cell(4,1,wall) . cell(4,2,open) . cell(4,3,wall) . cell(4,4,wall) . cell(4,5,wall) .
cell(5,0,wall) . cell(5,1,wall) . cell(5,2,wall) . cell(5,3,wall) . cell(5,4,wall) . cell(5,5,wall) .

%Initiate player_position(row,col), crates(row,col)
player_position(1,2) . %get from player
crate(1,3) . %read from board
crate(2,2) .

%Goal coordinates as crates
goal_requirement :- crate(1,4,T), crate(3,2,T) .