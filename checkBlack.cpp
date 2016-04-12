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

std::vector<string> cells;
std::vector<string> playerMatrix;

int main()
{
	int i, j;

	freopen("thisPlayerMatrix.txt", "r", stdin);

	cells.PB("B..BB..B");
	cells.PB("........");
	cells.PB("........");
	cells.PB("B..BB..B");
	cells.PB("B..BB..B");
	cells.PB("........");
	cells.PB("........");
	cells.PB("B..BB..B");


	string str1;

	fl(i,0,LIMIT)
	{
		cin>>str1;
		playerMatrix.PB(str1);
	}

	fl(i,0,LIMIT)
	{
		fl(j,0,LIMIT)
		{
			if(cells[i][j] == 'B' && playerMatrix[i][j] != 'B')
				return 1;

			else if(cells[i][j] != 'B' && playerMatrix[i][j] =='B')
				return 1;
		}
	}

	return 0;
}
/*
	Powered by Buggy Plugin
*/
