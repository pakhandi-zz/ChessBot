/*
	Author : Asim Krishna Prasad

	Aim :
		1> Take a board matrix and player as input
		2> Output the best possible move

*/
using namespace std;

#include<bits/stdc++.h>

#define wl(n) while(n--)
#define fl(i,a,b) for(i=a; i<b; i++)
#define rev(i,a,b) for(i=a; i>=b; i--)

#define si(n) scanf("%d", &n)
#define sll(l) scanf("%lld",&l)
#define ss(s) scanf("%s", s)
#define sc(c) scanf("%c", &c)
#define sd(f) scanf("%lf", &f)

#define pi(n) printf("%d\n", n)
#define pll(l) printf("%lld\n", l)
#define ps(s) printf("%s\n", s)
#define pc(c) printf("%c\n", c)
#define pd(f) printf("%lf\n", f)

#define debug(x) cout<<"\n#("<<x<<")#\n"
#define nline printf("\n")

#define mem(a,i) memset(a,i,sizeof(a))

#define MOD 1000000007
#define ll long long int
#define u64 unsigned long long int

#define mclr(strn) strn.clear()
#define ignr cin.ignore()
#define PB push_back
#define SZ size
#define MP make_pair
#define fi first
#define sec second

const int LIMIT = 8;
int MYPLAYER;	

std::vector<string> inBoard;

map<char,int> value;

map<char,vector<pair<int,int> > > moves;
vector<vector<int> > playerMatrix;

vector<pair<int,int> > finalMove;

/*

rnbqkbnr
pppppppp

PPPPPPPP
RNBQKBNR

0 => white
1 => black

*/

bool isEmpty(int,int,vector<string>);

bool canReach(pair<int,int> src, pair<int,int> dest, vector<string> board)
{
	int i;
	if(board[src.first][src.second] == 'N' || board[src.first][src.second] == 'n')
		return 1;
	else if(src.first == dest.first)
	{
		if(dest.second < src.second)
			swap(src,dest);

		fl(i,src.second + 1,dest.second)
		{
			if(!isEmpty(src.first,i,board))
				return 0;
		}
		return 1;
	}
	else if(src.second == dest.second)
	{
		if(dest.first < src.first)
			swap(src,dest);

		fl(i,src.first + 1,dest.first)
		{
			if(!isEmpty(i,src.second,board))
				return 0;
		}
		return 1;
	}
	else if( (src.second - dest.second) / (src.first - dest.first) == 1 )
	{
		if(dest.first < src.first)
			swap(src,dest);

		src.first++;
		src.second++;

		if(src == dest)
			return 1;

		while(src != dest)
		{
			if(!isEmpty(src.first,src.second,board))
				return 0;
			src.first++;
			src.second++;
		}
		return 1;
	}
	else
	{
		if(dest.second > src.second)
			swap(src,dest);

		src.first++;
		src.second--;

		if(src == dest)
			return 1;

		while(src != dest)
		{
			if(!isEmpty(src.first,src.second,board))
				return 0;
			src.first++;
			src.second--;
		}
		return 1;
	}
}


vector<vector<int> > getPlayerMatrix(vector<string> board)
{
	int i, j;
	vector<vector<int> > ret;
	ret.resize(LIMIT);
	fl(i,0,LIMIT)
		ret[i].resize(LIMIT);

	fl(i,0,LIMIT)
	{
		fl(j,0,LIMIT)
		{
			if( board[i][j] >= 'A' && board[i][j] <= 'Z' )
				ret[i][j] = 0;
			else if( board[i][j] >= 'a' && board[i][j] <= 'z' )
				ret[i][j] = 1;
			else
				ret[i][j] = -1;
		}	
	}
	return ret;
}


int evaluate(vector<string> mat)
{
	value['r'] = value['R'] = 10;
	value['n'] = value['N'] = 15;
	value['b'] = value['B'] = 13;
	value['q'] = value['Q'] = 50;
	value['k'] = value['K'] = 1000;
	value['K'] = 5000;
	value['p'] = value['P'] = 5;

	int i, j;

	int ret = 0;

	/*fl(i,0,LIMIT)
	{
		fl(j,0,LIMIT)
		{
			cout<<mat[i][j]<<" ";
		}
		nline;
	}*/

	vector<vector<int> > thisPlayerMatrix = getPlayerMatrix(mat);
	

	fl(i,0,LIMIT)
	{
		fl(j,0,LIMIT)
		{
			if(!isEmpty(i,j,mat))
			{
				int val = value[mat[i][j]];

				if( thisPlayerMatrix[i][j] == MYPLAYER )
					ret += val;
				else
					ret -= val;
			}
		}
	}

	/*cout<<ret; nline;
	cout<<"-----------------------"; nline;*/

	return ret;
}

void preprocessMoves()
{
	int i;

	moves['p'].PB(MP(+1,0));
	moves['p'].PB(MP(+1,-1));
	moves['p'].PB(MP(+1,+1));
	moves['p'].PB(MP(+2,0));
	
	moves['P'].PB(MP(-1,0));
	moves['P'].PB(MP(-1,-1));
	moves['P'].PB(MP(-1,+1));
	moves['P'].PB(MP(-2,0));

	fl(i,1,LIMIT)
	{
		moves['r'].PB(MP(i,0));
		moves['r'].PB(MP(-i,0));
		moves['r'].PB(MP(0,i));
		moves['r'].PB(MP(0,-i));
	}
	moves['R'] = moves['r'];

	moves['n'].PB(MP(+1,+2));	moves['n'].PB(MP(+2,+1));
	moves['n'].PB(MP(+1,-2));	moves['n'].PB(MP(-2,+1));
	moves['n'].PB(MP(-1,+2));	moves['n'].PB(MP(+2,-1));
	moves['n'].PB(MP(-1,-2));	moves['n'].PB(MP(-2,-1));
	moves['N'] = moves['n'];

	fl(i,1,LIMIT)
	{
		moves['b'].PB(MP(+i,+i));
		moves['b'].PB(MP(-i,-i));
		moves['b'].PB(MP(+i,-i));
		moves['b'].PB(MP(-i,+i));
	}
	moves['B'] = moves['b'];

	moves['q'] = moves['r'];
	moves['q'].insert(moves['q'].end(), moves['b'].begin(), moves['b'].end() );
	moves['Q'] = moves['q'];

	moves['k'].PB(MP(-1,+0));
	moves['k'].PB(MP(-1,+1));
	moves['k'].PB(MP(+0,+1));
	moves['k'].PB(MP(+1,+1));
	moves['k'].PB(MP(+1,+0));
	moves['k'].PB(MP(+1,-1));
	moves['k'].PB(MP(+0,-1));
	moves['k'].PB(MP(-1,-1));
	moves['K'] = moves['k'];
}

bool isOnBoard(int x, int y)
{
	if(x<0 || x>=LIMIT || y<0 || y>=LIMIT)
		return 0;
	return 1;
}

bool isEmpty(int x, int y, vector<string> mat)
{
	if(mat[x][y] == '.')
		return 1;
	return 0;
}

bool isSamePlayer(int x, int y, int player, vector<vector<int> > mat)
{
	return player == mat[x][y];
}

int alphaBetaMin(int,int,int,int,vector<string>);

int alphaBetaMax(int alpha, int beta, int depthLeft, int player, vector<string> board)
{
	if(depthLeft == 0) return evaluate(board);

	vector<vector<int> > thisPlayerMatrix = getPlayerMatrix(board);

	int i, j, l;

	fl(i,0,LIMIT)
	{
		fl(j,0,LIMIT)
		{
			if(thisPlayerMatrix[i][j] == player)
			{
				char thisPiece = board[i][j];

				int inLimit = moves[thisPiece].SZ();

				fl(l,0,inLimit)
				{
					int dx = moves[thisPiece][l].first;
					int dy = moves[thisPiece][l].second;

					int x = i + dx;
					int y = j + dy;
					
					if(thisPiece == 'P' || thisPiece == 'p')
					{
						if (!isOnBoard(x,y))
							continue;
						int pos = thisPiece == 'P'? 6 : 1;
						if(l == 0 && !(isEmpty(x,y,board)) && isOnBoard(x,y) )
							continue;
						if(l == 3 && (i != pos || !(isEmpty(x,y,board) ) ) && isOnBoard(x,y) )
							continue;
						if( (l == 1 || l == 2) && isOnBoard(x,y) && (isEmpty(x,y,inBoard) || (isSamePlayer(x,y,player,thisPlayerMatrix) ) ) )
							continue;
					}

					if( isOnBoard(x,y) && ( isEmpty(x,y,board) || !isSamePlayer(x,y,player,thisPlayerMatrix) ) && canReach(MP(i,j),MP(x,y),board) )
					{
						vector<string> temp = board;
						temp[x][y] = temp[i][j];
						temp[i][j] = '.';
						
						//cout<<i<<" "<<j<<" : "<<x<<" "<<y; nline;

						int score = alphaBetaMin(alpha, beta, depthLeft - 1, !player, temp);

						if( score >= beta )
							return beta;   // fail hard beta-cutoff
						if( score > alpha )
							alpha = score; // alpha acts like max in MiniMax
					}
				}
			}
		}
	}

	return alpha;

}


int alphaBetaMin(int alpha, int beta, int depthLeft, int player, vector<string> board)
{
	if(depthLeft == 0) return -evaluate(board);

	vector<vector<int> > thisPlayerMatrix = getPlayerMatrix(board);

	int i, j, l;

	fl(i,0,LIMIT)
	{
		fl(j,0,LIMIT)
		{
			if(thisPlayerMatrix[i][j] == player)
			{
				char thisPiece = board[i][j];

				int inLimit = moves[thisPiece].SZ();

				fl(l,0,inLimit)
				{
					int dx = moves[thisPiece][l].first;
					int dy = moves[thisPiece][l].second;

					int x = i + dx;
					int y = j + dy;
					
					if(thisPiece == 'P' || thisPiece == 'p')
					{
						if (!isOnBoard(x,y))
							continue;
						int pos = thisPiece == 'P'? 6 : 1;
						if(l == 0 && !(isEmpty(x,y,board)) )
							continue;
						if(l == 3 && (i != pos || !(isEmpty(x,y,board) ) )  )
							continue;
						if( (l == 1 || l == 2) && isOnBoard(x,y) && (isEmpty(x,y,inBoard) || (isSamePlayer(x,y,player,thisPlayerMatrix) ) ) )
							continue;
					}

					if( isOnBoard(x,y) && ( isEmpty(x,y,board) || !isSamePlayer(x,y,player,thisPlayerMatrix) ) && canReach(MP(i,j),MP(x,y),board) )
					{
						vector<string> temp = board;
						temp[x][y] = temp[i][j];
						temp[i][j] = '.';

						//cout<<i<<" "<<j<<" : "<<x<<" "<<y; nline;

						int score = alphaBetaMax(alpha, beta, depthLeft - 1, !player, temp);

						if( score <= alpha )
							return alpha;   // fail hard alpha-cutoff
						if( score < beta )
							beta = score; // alpha acts like min in MiniMax
					}
				}
			}
		}
	}

	return beta;

}

int main()
{
	int i, j, l;

	playerMatrix.resize(LIMIT);
	fl(i,0,LIMIT)
	{
		playerMatrix[i].resize(LIMIT);
	}
	finalMove.resize(2);
	
	

	fl(i,0,LIMIT)
	{
		string temp;
		cin>>temp;
		inBoard.PB(temp);

		fl(j,0,LIMIT)
		{
			if( temp[j] >= 'A' && temp[j] <= 'Z' )
				playerMatrix[i][j] = 0;
			else if( temp[j] >= 'a' && temp[j] <= 'z' )
				playerMatrix[i][j] = 1;
			else
				playerMatrix[i][j] = -1;
		}
	}

	cin>>MYPLAYER;
	
	/*fl(i,0,LIMIT)
	{
		fl(j,0,LIMIT)
		{
			cout<<playerMatrix[i][j];
		}
		nline;
	}*/
	
	//cout<<isEmpty(5,1,inBoard);
	
	//return 0;
	
	//cout<<isSamePlayer(7,0,0,playerMatrix); return 0;

	preprocessMoves();
	
	//cout<<moves['P'].SZ(); nline;

	int maxx = INT_MIN;

	int alpha = INT_MIN;
	int beta = INT_MAX;

	int depthLeft = 4;

	fl(i,0,LIMIT)
	{
		fl(j,0,LIMIT)
		{
			if(playerMatrix[i][j] == MYPLAYER)
			{
				char thisPiece = inBoard[i][j];

				int inLimit = moves[thisPiece].SZ();

				fl(l,0,inLimit)
				{
					int dx = moves[thisPiece][l].first;
					int dy = moves[thisPiece][l].second;

					int x = i + dx;
					int y = j + dy;
					
					if(thisPiece == 'P' || thisPiece == 'p')
					{
						if (!isOnBoard(x,y))
							continue;
						int pos = thisPiece == 'P'? 6 : 1;
						if(l == 0 && !(isEmpty(x,y,inBoard)) && isOnBoard(x,y) )
							continue;
						if(l == 3 && (i != pos || !(isEmpty(x,y,inBoard) ) ) && isOnBoard(x,y) )
							continue;
						if( (l == 1 || l == 2) && isOnBoard(x,y) && (isEmpty(x,y,inBoard) || (isSamePlayer(x,y,MYPLAYER,playerMatrix) ) ) )
							continue;
					}
					
					/*if(thisPiece == 'p')
					{
						if(l == 3 && i != 1)
							break;
						if( (l == 1 || l == 2) && isOnBoard(x,y) && !isEmpty(x,y,inBoard) && !(isSamePlayer(x,y,MYPLAYER,playerMatrix)) )
							break;
					}*/
					
					if( isOnBoard(x,y) && ( isEmpty(x,y,inBoard) || !isSamePlayer(x,y,MYPLAYER,playerMatrix) ) && canReach(MP(i,j),MP(x,y),inBoard) )
					{
						
						vector<string> temp = inBoard;
						temp[x][y] = temp[i][j];
						temp[i][j] = '.';
						//cout<<i<<" "<<j<<" : "<<x<<" "<<y; nline;
						int score = alphaBetaMin(alpha, beta, depthLeft - 1, !MYPLAYER, temp);
						//cout<<i<<" "<<j<<" : "<<x<<" "<<y<<" -> "<<score; nline;

						if(score > maxx)
						{
							maxx = score;
							finalMove[0] = (MP(i,j));
							finalMove[1] = (MP(x,y));
						}
					}
				}
			}
		}
	}

	fl(i,0,2)
	{
		cout<<finalMove[i].first<<" "<<finalMove[i].second;
		nline;
	}

	inBoard[finalMove[1].first][finalMove[1].second] = inBoard[finalMove[0].first][finalMove[0].second];
	inBoard[finalMove[0].first][finalMove[0].second] = '.';

	freopen("prevBoard.txt", "w", stdout);

	fl(i,0,LIMIT)
	{
		fl(j,0,LIMIT)
		{
			cout<<inBoard[i][j];
		}
		nline;
	}

	return 0;
}
/*
	Powered by Buggy Plugin
*/

