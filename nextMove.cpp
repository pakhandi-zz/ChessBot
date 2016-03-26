//Author : Asim Krishna Prasad
//
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

std::vector<string> inBoard;

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

int evaluate(vector<string> mat)
{
	return 10;
}

void preprocessMoves()
{
	int i;

	moves['p'].PB(MP(-1,0));
	moves['P'].PB(MP(+1,0));

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

bool isSamePlayer(int x, int y, int player, vector<string> mat)
{
	return player == mat[x][y];
}

int alphaBetaMin(int,int,int,int,vector<string>);

int alphaBetaMax(int alpha, int beta, int depthLeft, int player, vector<string> board)
{
	if(depthLeft == 0) return evaluate(board);

	int i, j, l;

	fl(i,0,LIMIT)
	{
		fl(j,0,LIMIT)
		{
			if(playerMatrix[i][j] == player)
			{
				char thisPiece = inBoard[i][j];

				int inLimit = moves[thisPiece].SZ();

				fl(l,0,inLimit)
				{
					int dx = moves[thisPiece][l].first;
					int dy = moves[thisPiece][l].second;

					int x = i + dx;
					int y = j + dy;

					if( isOnBoard(x,y) && ( isEmpty(x,y,board) || !isSamePlayer(x,y,player,board) ) )
					{
						vector<string> temp = board;
						temp[x][y] = temp[i][j];
						temp[i][j] = '.';

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

	int i, j, l;

	fl(i,0,LIMIT)
	{
		fl(j,0,LIMIT)
		{
			if(playerMatrix[i][j] == player)
			{
				char thisPiece = inBoard[i][j];

				int inLimit = moves[thisPiece].SZ();

				fl(l,0,inLimit)
				{
					int dx = moves[thisPiece][l].first;
					int dy = moves[thisPiece][l].second;

					int x = i + dx;
					int y = j + dy;

					if( isOnBoard(x,y) && ( isEmpty(x,y,board) || !isSamePlayer(x,y,player,board) ) )
					{
						vector<string> temp = board;
						temp[x][y] = temp[i][j];
						temp[i][j] = '.';

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

	preprocessMoves();

	int maxx = INT_MIN;

	int player = 0;

	int alpha = INT_MIN;
	int beta = INT_MAX;

	int depthLeft = 2;

	fl(i,0,LIMIT)
	{
		fl(j,0,LIMIT)
		{
			if(playerMatrix[i][j] == player)
			{
				char thisPiece = inBoard[i][j];

				int inLimit = moves[thisPiece].SZ();

				fl(l,0,inLimit)
				{
					int dx = moves[thisPiece][l].first;
					int dy = moves[thisPiece][l].second;

					int x = i + dx;
					int y = j + dy;

					if( isOnBoard(x,y) && ( isEmpty(x,y,inBoard) || !isSamePlayer(x,y,player,inBoard) ) )
					{
						vector<string> temp = inBoard;
						temp[x][y] = temp[i][j];
						temp[i][j] = '.';

						int score = alphaBetaMin(alpha, beta, depthLeft - 1, !player, temp);

						if(score > maxx)
						{
							maxx = score;
							finalMove.PB(MP(i,j));
							finalMove.PB(MP(x,y));
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


	return 0;
}
/*
	Powered by Buggy Plugin
*/
