//Author : pakhandi
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

int LIMIT = 8;

std::vector<pair<int,int> > cells;
std::vector<string> playerMatrix;

int main()
{
	int i, j;

	freopen("thisPlayerMatrix.txt", "r", stdin);

	fl(i,0,6)
	{
		cells.PB(MP(i,0));
		cells.PB(MP(i,LIMIT - 1));
	}
	cells.PB(MP(0,1));
	cells.PB(MP(0,2));
	cells.PB(MP(0,5));
	cells.PB(MP(0,6));


	string str1;

	fl(i,0,LIMIT)
	{
		cin>>str1;
		playerMatrix.PB(str1);
	}

	fl(i,0,cells.SZ())
	{
		if( playerMatrix[cells[i].first][cells[i].second] != 'B' )
		{
			return 1;
		}
	}

	fl(i,0,LIMIT)
	{
		fl(j,0,LIMIT)
		{
			if( find(cells.begin(), cells.end(), MP(i,j)) == cells.end() )
			{
				if( playerMatrix[i][j] == 'B' )
					return 1;
			}
		}
	}

	//cout<<"here";

	return 0;
}
/*
	Powered by Buggy Plugin
*/
