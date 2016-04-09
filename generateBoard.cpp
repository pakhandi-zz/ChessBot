/*
	Author : Asim Krishna Prasad

	Aim :
		1> Generate the current board matrix using current player matrix and 
			previous board matrix

*/
using namespace std;

#include <bits/stdc++.h>

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

vector<string> playerMatrix, prevBoard;
char pieceLifted;

int main()
{
	int i, j, l;

	fl(i,0,LIMIT)
	{
		string temp;
		cin>>temp;
		playerMatrix.PB(temp);
	}

	freopen("prevBoard", "r", stdin);

	fl(i,0,LIMIT)
	{
		string temp;
		cin>>temp;
		prevBoard.PB(temp);
	}

	bool doBreak = 0;

	fl(i,0,LIMIT)
	{
		fl(j,0,LIMIT)
		{
			if( playerMatrix[i][j] == '.' && prevBoard[i][j] != '.' && islower(prevBoard[i][j]))
			{
				pieceLifted = prevBoard[i][j];
				//cout<<pieceLifted<<" "<<i<<" "<<j; nline;
				prevBoard[i][j] = '.';
				doBreak = 1;
				break;
			}
		}
		if(doBreak)
			break;
	}
	
	doBreak = 0;

	fl(i,0,LIMIT)
	{
		fl(j,0,LIMIT)
		{
			if( playerMatrix[i][j] != '.' && prevBoard[i][j] == '.' )
			{
				prevBoard[i][j] = pieceLifted;
				doBreak = 1;
				break;
			}
		}
		if(doBreak)
			break;
	}

	fl(i,0,LIMIT)
	{
		fl(j,0,LIMIT)
		{
			cout<<prevBoard[i][j];
		}
		nline;
	}
	
	return 0;

}