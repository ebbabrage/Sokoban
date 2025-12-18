%Time horizon, time(T)
time(0..30) .

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

%Inertia of fluents, i.e crates and plater position remain the same if not affected
player_position(ROW,COL,T+1) :- player_position(ROW,COL,T),time(T), not -player_position(ROW,COL,T+1) .
crate(ROW,COL,T+1) :- crate(ROW,COL,T), time(T), not -crate(ROW,COL,T+1) .

%Define effect of move_to(), i.e player movement and pushing crates. A space becomes empty if the player moves away from it. A crate gets pushed if a player moves into it
player_position(ROW,COL,T+1) :- move_to(ROW,COL,T), not player_one_way_teleporter(ROW, COL, _, _) .
-player_position(ROW,COL,T+1) :- move_to(_,_,T), player_position(ROW,COL,T) .

%player teleporter movement
player_position(DESTIONATION_ROW,DESTIONATION_COL,T+1) :- move_to(ROW,COL,T), player_one_way_teleporter(ROW, COL, DESTIONATION_ROW, DESTIONATION_COL), not crate(DESTIONATION_ROW,DESTIONATION_COL,T) .

%If the player teleporter destination is occupied
player_position(ROW,COL,T+1) :- move_to(ROW,COL,T), player_one_way_teleporter(ROW, COL, DESTIONATION_ROW, DESTIONATION_COL), not crate(DESTIONATION_ROW,DESTIONATION_COL,T)  .

%Normal tiles crate movement
crate(ROW+1,COL,T+1) :- crate(ROW,COL,T),move_to(ROW,COL,T), player_position(P_ROW,P_COL,T), P_ROW < ROW, not crate_one_way_teleporter(ROW+1, COL, _, _) . %south
crate(ROW-1,COL,T+1) :- crate(ROW,COL,T),move_to(ROW,COL,T), player_position(P_ROW,P_COL,T), P_ROW > ROW, not crate_one_way_teleporter(ROW-1, COL, _, _) . %north
crate(ROW,COL-1,T+1) :- crate(ROW,COL,T),move_to(ROW,COL,T), player_position(P_ROW,P_COL,T), P_COL > COL, not crate_one_way_teleporter(ROW, COL-1, _, _) . %west
crate(ROW,COL+1,T+1) :- crate(ROW,COL,T),move_to(ROW,COL,T), player_position(P_ROW,P_COL,T), P_COL < COL, not crate_one_way_teleporter(ROW, COL+1, _, _) . %east
-crate(ROW,COL,T+1)  :- move_to(ROW,COL,T),crate(ROW,COL,T) .

%Teleporter crate movement
crate(DESTIONATION_ROW, DESTIONATION_COL,T+1) :- crate(ROW,COL,T),move_to(ROW,COL,T), player_position(P_ROW,P_COL,T), P_ROW < ROW, crate_one_way_teleporter(ROW+1, COL, DESTIONATION_ROW, DESTIONATION_COL), not crate(DESTIONATION_ROW, DESTIONATION_COL) . %south
crate(DESTIONATION_ROW, DESTIONATION_COL,T+1) :- crate(ROW,COL,T),move_to(ROW,COL,T), player_position(P_ROW,P_COL,T), P_ROW > ROW, crate_one_way_teleporter(ROW-1, COL, DESTIONATION_ROW, DESTIONATION_COL), not crate(DESTIONATION_ROW, DESTIONATION_COL) . %north
crate(DESTIONATION_ROW, DESTIONATION_COL,T+1) :- crate(ROW,COL,T),move_to(ROW,COL,T), player_position(P_ROW,P_COL,T), P_COL > COL, crate_one_way_teleporter(ROW, COL-1, DESTIONATION_ROW, DESTIONATION_COL), not crate(DESTIONATION_ROW, DESTIONATION_COL) . %west
crate(DESTIONATION_ROW, DESTIONATION_COL,T+1) :- crate(ROW,COL,T),move_to(ROW,COL,T), player_position(P_ROW,P_COL,T), P_COL < COL, crate_one_way_teleporter(ROW, COL+1, DESTIONATION_ROW, DESTIONATION_COL), not crate(DESTIONATION_ROW, DESTIONATION_COL) . %east

%If the destination of the teleporter is occupied
crate(ROW, COL,T+1) :- crate(ROW,COL,T),move_to(ROW,COL,T), player_position(P_ROW,P_COL,T), P_ROW < ROW, crate_one_way_teleporter(ROW+1, COL, DESTIONATION_ROW, DESTIONATION_COL), crate(DESTIONATION_ROW, DESTIONATION_COL) . %south
crate(ROW, COL,T+1) :- crate(ROW,COL,T),move_to(ROW,COL,T), player_position(P_ROW,P_COL,T), P_ROW > ROW, crate_one_way_teleporter(ROW-1, COL, DESTIONATION_ROW, DESTIONATION_COL), crate(DESTIONATION_ROW, DESTIONATION_COL) . %north
crate(ROW, COL,T+1) :- crate(ROW,COL,T),move_to(ROW,COL,T), player_position(P_ROW,P_COL,T), P_COL > COL, crate_one_way_teleporter(ROW, COL-1, DESTIONATION_ROW, DESTIONATION_COL), crate(DESTIONATION_ROW, DESTIONATION_COL) . %west
crate(ROW, COL,T+1) :- crate(ROW,COL,T),move_to(ROW,COL,T), player_position(P_ROW,P_COL,T), P_COL < COL, crate_one_way_teleporter(ROW, COL+1, DESTIONATION_ROW, DESTIONATION_COL), crate(DESTIONATION_ROW, DESTIONATION_COL) . %east

%Ensure that crates and players will not exist at the same cell
:- crate(ROW,COL,T), player_position(ROW,COL,T) .

%A cell can not be both open and a wall
:- cell(ROW,COL,open), cell(ROW,COL,wall) .

%A players and crates can not be in a wall
:- cell(ROW,COL,wall), player_position(ROW,COL,_) .
:- cell(ROW,COL,wall), crate(ROW,COL,_) .

%two crates can not exist in the same cell
:- cell(ROW,COL,_), time(T), #count {crate(ROW,COL,T)} > 1 .

%Check if crates cover all goal states (do this by checking if there exists a crate which is not covered)
:- not goal_requirement . 

%Minimize solution
number_of_moves_to_solve(COUNT) :- COUNT = #count { 1:move_to(_,_,_) } .
#minimize { COUNT:number_of_moves_to_solve(COUNT) } .

%OBS this can risk failing to find solutions, therefore only use for testing. to reduce calculations restrict the player from moving back to the tile it came from
#show move_to/3 .