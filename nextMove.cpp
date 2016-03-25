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

/*

rnbqkbnr
pppppppp

PPPPPPPP
RNBQKBNR

*/

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

int main()
{
	int i, j;

	fl(i,0,LIMIT)
	{
		string temp;
		cin>>temp;
		inBoard.PB(temp);
	}

	preprocessMoves();


	return 0;
}
/*
	Powered by Buggy Plugin
*/
