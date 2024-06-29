// Date created: "08:59:41, 17-06-2024"
// Code by Dangptpt_
#include<bits/stdc++.h>

using namespace std;

#define fi first
#define se second
#define pb push_back

typedef long long LL;
typedef unsigned long long ULL;
typedef pair <int, int> II;
typedef pair <int, II> III;

template <typename T> void read(T &t) {
    t = 0; char ch = getchar(); int f = 1;
    while (!isdigit(ch)) { if (ch == '-') f = -1; ch = getchar(); }
    do { (t *= 10) += ch - '0'; ch = getchar(); } while (isdigit(ch)); t *= f;
}

const int MAXN = 1 + 1e6;
const int mod = 1e9 + 7;
const int inf = 0x3f3f3f3f;

int n, m, M, max_day, res, mark[MAXN];
LL bit[MAXN], harvest[MAXN];
III p[MAXN];
bool cmp (III a, III b) {
    if (a.se.fi == b.se.fi) {
        if (a.se.se == b.se.se)
            return a.fi < b.fi;
        else return a.se.se < b.se.se;
    }
    else return a.se.fi < b.se.fi;
}
void InOut() {
    #define TASK "../Test/test1000"
    freopen(TASK ".inp", "r", stdin);
    //freopen(TASK ".out", "w", stdout);
}

bool check(int i, int sum, int day){
	if (mark[i] != 0) 
        return 0;
	if (sum > M) 
        return 0;
	if (day < p[i].se.fi || day > p[i].se.se) 
        return 0;
	return 1;  
}

void Solve() {
    cin >> n >> m >> M;
    for (int i=1; i<=n; ++i) {
        cin >> p[i].fi >> p[i].se.fi >> p[i].se.se;
        max_day = max(max_day, p[i].se.se);
        mark[i] = 0;
    }
    sort(p+1, p+n+1, cmp);
    
    // for (int i=1; i<=n; ++i) cout << p[i].fi << " " << p[i].se.fi << " " << p[i].se.se << '\n';
    for (int day=max_day; day>0; --day) {
        int sum = 0;
        vector<int> tmp;
        for (int i=n; i>0; --i) {
            if (check(i, sum + p[i].fi, day) == 1) {
                mark[i] = day;
                sum += p[i].fi;
                tmp.push_back(i);
            }       
        }
        if (sum < m) {
            for (int i=0; i<tmp.size(); ++i) 
                mark[tmp[i]] = 0;
        }
    } 
    int total = 0;
    for (int i=1; i<=n; ++i) {
        if (mark[i] != 0) {
            res++;
            total += p[i].fi;  
        }
    }
    cout << res << '\n' << total;
    // for (int i=1; i<=n; ++i) {
    //     if (mark[i] != 0) 
    //         cout << i << ' ' << mark[i] << '\n';
    // }
}


int main() {
    InOut();
    ios_base::sync_with_stdio(false);
    cin.tie(0);
    cout.tie(0);
    Solve();
    return 0;
}