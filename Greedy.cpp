#include <iostream>
#include <vector>

using namespace std;

const int MAXN = 10000;

int n, m, M;
vector<int> d, s, e;
vector<int> x; // thu hoach hay chua
int dsday[10000]; // ngay chon
int tmp = 0;
bool check(int i, int sum, int day){
	if(x[i] == 1) return false;
	if(sum > M) return false;
	if(day < s[i] || day > e[i]) return false;
	return true;  
}

void Try(int sum, int day) {
	for(int i = 1; i <= n; i++){
		if(check(i, sum + d[i], day)){
			x[i] = 1;
			dsday[i] = day;
			sum += d[i];
			if(i==n){
				Try(sum, day);
			}			
		}		
	}
}

int main() {
  #define TASK "test"
  freopen(TASK ".inp", "r", stdin);
  //freopen(TASK ".out", "w", stdout);
  cin >> n >> m >> M;
  d.resize(n + 1);
  s.resize(n + 1);
  e.resize(n + 1);
  x.resize(n + 1);
  int dmin = 99999, dmax = 0;
  for (int i = 1; i <= n; i++) {
    cin >> d[i] >> s[i] >> e[i];
    if(s[i] < dmin) dmin = s[i];
    if(e[i] > dmax) dmax = e[i];
    x[i] = 0;
  }
  for(int i = 1; i<=n; i++){
  	dsday[i] = 0;
  }
  
  for(int f=dmin; f<=dmax;f++) Try(0, f);
  int res = 0;
  for(int i=1; i<=n;i++){
  	res += x[i];
  }
  cout << res << endl;
  for (int i = 1; i <= n; i++) {
  	if(dsday[i] == 0) dsday[i] = -1;
    if(dsday[i] != -1) cout << i << " " << dsday[i] << '\n';
  }
  return 0;
}