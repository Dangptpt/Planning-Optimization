    // Date created: "10:41:14, 28-05-2024"
// Code by Dangptpt_
#include<bits/stdc++.h>

using namespace std;

#define fi first
#define se second
#define pb push_back

typedef long long LL;
typedef unsigned long long ULL;
typedef pair <int, int> II;

template <typename T> void read(T &t) {
    t = 0; char ch = getchar(); int f = 1;
    while (!isdigit(ch)) { if (ch == '-') f = -1; ch = getchar(); }
    do { (t *= 10) += ch - '0'; ch = getchar(); } while (isdigit(ch)); t *= f;
}

const int MAXN = 1 + 1e6;
const int mod = 1e9 + 7;
const int inf = 0x3f3f3f3f;

int n, m, M, d[10001], s[10001], e[10001], max_day, res, mark[10001];

void InOut() {
    #define TASK "../Test/test1000_1000"
    freopen(TASK ".inp", "r", stdin);
    //freopen(TASK ".out", "w", stdout);
}

bool check(int i, int sum, int day){
	if (mark[i] != 0) 
        return 0;
	if (sum > M) 
        return 0;
	if (day < s[i] || day > e[i]) 
        return 0;
	return 1;  
}

void Solve() {
    cin >> n >> m >> M;
    for (int i=1; i<=n; ++i) {
        cin >> d[i] >> s[i] >> e[i];
        max_day = max(max_day, e[i]);
        mark[i] = 0;
    }

    for (int day=1; day<=max_day; ++day) {
        int sum = 0;
        vector<int> tmp;
        for (int i=1; i<=n; ++i) {
            if (check(i, sum + d[i], day) == 1) {
                mark[i] = day;
                sum += d[i];
                tmp.push_back(i);
            }       
        }
        if (sum < m) {
            for (int i=0; i<tmp.size(); ++i) {
                mark[tmp[i]] = 0;
            }
        }
    }
    int total = 0;
    for (int i=1; i<=n; ++i) {
        if (mark[i] != 0) {
            res++;
            total += d[i];  
        }
    }
    cout << "Total harvested: " << res << '\n' << "Num of fields: " << total;
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