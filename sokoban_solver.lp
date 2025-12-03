%Initiate board: walls, open space
%XXXXXX
%XPOCGX
%XXCXXX
%XXGXXX
%XXXXXX

cell(0,0,wall) . cell(0,1,wall) . cell(0,2,wall) . cell(0,3,wall) . cell(0,4,wall) . cell(0,5,wall) .
cell(1,0,wall) . cell(1,1,open) . cell(1,2,open) . cell(1,3,open) . cell(1,4,open) . cell(1,5,wall) .
cell(2,0,wall) . cell(2,1,wall) . cell(2,2,open) . cell(2,3,wall) . cell(2,4,wall) . cell(2,5,wall) .
cell(3,0,wall) . cell(3,1,wall) . cell(3,2,open) . cell(3,3,wall) . cell(3,4,wall) . cell(3,5,wall) .
cell(4,0,wall) . cell(4,1,wall) . cell(4,2,open) . cell(4,3,wall) . cell(4,4,wall) . cell(4,5,wall) .
cell(5,0,wall) . cell(5,1,wall) . cell(5,2,wall) . cell(5,3,wall) . cell(5,4,wall) . cell(5,5,wall) .


%Initiate player_position(row,col), crates(row,col) and goal_cordinartes(row,col)
player_position(1,2) .
crate(1,3) .
crate(2,2) .
goal_cordinartes(1,4) .
goal_cordinartes(3,2) .

%Time horizon, time(T)
time(0..2) .

%Initiate players and crates as time based /3
player_position(ROW,COL,0) :- player_position(ROW,COL) .
crate(ROW,COL,0) :- crate(ROW,COL) .

%Establish adjacency to player_position(row, col, T)
adjacent(ROW+1,COL,T) :- player_position(ROW,COL,T) .
adjacent(ROW-1,COL,T) :- player_position(ROW,COL,T) .
adjacent(ROW,COL+1,T) :- player_position(ROW,COL,T) .
adjacent(ROW,COL-1,T) :- player_position(ROW,COL,T) .

%Establish if a space is open or if it contains a crate that has an open space after it (the crate check can be made using a pushable variable which checks space after crate relative to the players position)
pushable(ROW,COL,T) :- adjacent(ROW,COL,T), crate(ROW,COL,T), cell(ROW+1,COL,open), not crate(ROW+1,COL,T), player_position(P_ROW,P_COL,T), P_ROW + 1 = ROW, P_COL = COL .  %south
pushable(ROW,COL,T) :- adjacent(ROW,COL,T), crate(ROW,COL,T), cell(ROW-1,COL,open), not crate(ROW-1,COL,T), player_position(P_ROW,P_COL,T), P_ROW - 1 = ROW, P_COL = COL .  %north
pushable(ROW,COL,T) :- adjacent(ROW,COL,T), crate(ROW,COL,T), cell(ROW,COL-1,open), not crate(ROW,COL-1,T), player_position(P_ROW,P_COL,T), P_ROW = ROW, P_COL - 1 = COL .  %west
pushable(ROW,COL,T) :- adjacent(ROW,COL,T), crate(ROW,COL,T), cell(ROW,COL+1,open), not crate(ROW,COL+1,T), player_position(P_ROW,P_COL,T), P_ROW = ROW, P_COL + 1 = COL .  %east

%Combine these two into a available(row,col,T)
available_move(ROW,COL,T) :- pushable(ROW,COL,T) .
available_move(ROW,COL,T) :- adjacent(ROW,COL,T), cell(ROW,COL,open), not crate(ROW,COL,T) .

%Choose 1 move_to() per turn as a player action
{move_to(ROW,COL,T):available_move(ROW,COL,T)} <= 1 :- time(T) . 

%Define static relationships, i.e crates, walls and open spaces remain if not affected
player_position(ROW,COL,T+1) :- player_position(ROW,COL,T),time(T), not -player_position(ROW,COL,T+1) .
crate(ROW,COL,T+1) :- crate(ROW,COL,T), time(T), not -crate(ROW,COL,T+1) .

%Define effect of move_to(), i.e player movement and pushing crates. A space becomes empty if the player moves away from it. A crate gets pushed if a player moves into it
player_position(ROW,COL,T+1) :- move_to(ROW,COL,T) .
-player_position(ROW,COL,T+1) :- move_to(_,_,T), player_position(ROW,COL,T) .

crate(ROW+1,COL,T+1) :- crate(ROW,COL,T),move_to(ROW,COL,T), player_position(P_ROW,P_COL,T), P_ROW < ROW . %south
crate(ROW-1,COL,T+1) :- crate(ROW,COL,T),move_to(ROW,COL,T), player_position(P_ROW,P_COL,T), P_ROW > ROW . %north
crate(ROW,COL-1,T+1) :- crate(ROW,COL,T),move_to(ROW,COL,T), player_position(P_ROW,P_COL,T), P_COL > COL . %west
crate(ROW,COL+1,T+1) :- crate(ROW,COL,T),move_to(ROW,COL,T), player_position(P_ROW,P_COL,T), P_COL < COL . %east
-crate(ROW,COL,T+1)  :- move_to(ROW,COL,T),crate(ROW,COL,T) .

%Check if crates cover all goal states (do this by checking if there exists a crate which is not covered)
goal_requirement :- crate(1,4,T), crate(3,2,T) .
:- not goal_requirement . 

%OBS this can risk failing to find solutions, therefore only use for testing. to reduce calculations restrict the player from moving back to the tile it came from
#show move_to/3 .