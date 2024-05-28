// Date created: "22:48:44, 06-03-2024"
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


int n, m, M, d[101], s[10001], e[10001], harvested[10001], max_day, current, res, max_havested, n_fields, mark[1001];

vector <II> ans;

bool check (int v, int k) {
    if (s[k] > v) return 0;
    if (e[k] < v) return 0;
    if (harvested[v] + d[k] < m || harvested[v] + d[k] > M) return 0;
    return 1;
}

void Try (int k) {
    for (int v=1; v<=max_day; ++v) {
        if (check (v, k) == 1) {
            harvested[v] += d[k];
            //cout << harvested[v] << '\n';
            current += d[k];
            mark[k] = v;
            if (k == n) {
                if (current > res) {
                    res = current;
                    ans.clear();
                    for (int i=1; i<=n; ++i) {
                        ans.push_back({i, mark[i]});
                    }
                }
            }
            else if (current + (n-k)*max_havested > res) Try(k+1);
            mark[k] = -1;
            current -= d[k];
            harvested[v] -= d[k];
        }
    }                                                                                                                                                                                                                               
}

void InOut() {
    #define TASK "test"
    freopen(TASK ".inp", "r", stdin);
    //freopen(TASK ".out", "w", stdout);
}

void Solve() {
    cin >> n >> m >> M;
    for (int i=1; i<=n; ++i) {
        cin >> d[i] >> s[i] >> e[i];
        max_day = max(max_day, e[i]);
        max_havested = max (max_havested, d[i]);
        mark[i] = 1;
    }

    Try(1);

    for (auto v:ans) {
        cout << v.first << " " << v.second << '\n';
    }
    //cout << res;
}

int main() {
    InOut();
    ios_base::sync_with_stdio(false);
    cin.tie(0);
    cout.tie(0);
    Solve();
    return 0;
}