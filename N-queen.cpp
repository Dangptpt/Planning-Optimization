// Date created: "12:38:58, 14-03-2024"
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

const int MAXN = 1 + 1e3;
const int mod = 1e9 + 7;
const int inf = 0x3f3f3f3f; 

// Lớp CP solver giải quyết bài toán n Queens
class NQueensSolver {
    /*
    Đóng gói solver
    size: kích thước bàn cờ
    result: mảng 2 chiều với 1 là vị trí quân cờ, 0 ngược lại
    phương thức solve: giải bài toán N queen
    phương thức printSolution: in ra kết quả.
    */ 
    public: 
        int size;
        int** result;
        NQueensSolver(int n) {
            this->size = n;
            
        }

        void solve() {
            this->init();
            this->DFS(0);
        }

        void printSolution() {
            for (int i=0; i<this->size; ++i) {
                for (int j=0; j<this->size; ++j) {
                    cout << result[i][j] << " ";
                }
                cout << '\n';
            }
        }

    // các phương thức private
    private:
        vector<int> candidates[MAXN];
        int** tmp;
        bool check_stop = false;

        // phương thức init: cáp phát bộ nhớ, khởi tạo 
        void init() {
            tmp = new int*[this->size];
            result = new int*[this->size];
        
            for (int i=0; i<size; ++i) {
                tmp[i] = new int[this->size];
                result[i] = new int[this->size];
                for (int j=0; j<size; ++j) {
                    candidates[i].push_back(j);
                    tmp[i][j] = result[i][j] = 0;
                }
            }
        }

        void popElement(int i, int val) {
            for (int j=0; j<candidates[i].size(); ++j) {
                if (candidates[i][j] == val){
                    candidates[i].erase(candidates[i].begin()+j);
                    break;
                } 
            }
        }

        void pushElement(int i, int val) {
            candidates[i].push_back(val);
        }
        
        // Propagation Algorithm: lan truyền ràng buộc
        void propagation(int pos, int val) {
            for (int i=pos+1; i<size; ++i) {
                this->popElement(i, val);
                if (pos+val-i >= 0)
                    this->popElement(i, pos+val-i);
                if (-pos+val+i < this->size)
                    this->popElement(i, -pos+val+i);
            }
        }

        void reversePropagation(int pos, int val) {
            for (int i=pos+1; i<size; ++i) {
                this->pushElement(i, val);
                if (pos+val-i >= 0)
                    this->pushElement(i, pos+val-i);
                if (-pos+val+i < this->size)
                    this->pushElement(i, -pos+val+i);
            }
        }

        // Exploration Algorithm: dfs tìm lời giải
        void DFS(int k) {
            if (check_stop == true) return;
            // Branching Algorithm: phân nhánh trong cây tìm kiếm
            for (auto c:candidates[k]) {
                tmp[k][c] = 1;
                this->propagation(k, c);
                if (k == this->size-1) {
                    check_stop = true;
                    for (int i=0; i<this->size; ++i) 
                        for (int j=0; j<this->size; ++j) this->result[i][j] = this->tmp[i][j]; 
                    return;
                }
                else DFS(k+1);
                tmp[k][c] = 0;
                this->reversePropagation(k, c);
            }
            
        }
};


void InOut() {
    #define TASK "ABC"
    freopen(TASK ".inp", "r", stdin);
    freopen(TASK ".out", "w", stdout);
}

void Solve() {
    int n;
    cin >> n;
    NQueensSolver solver(n);
    solver.solve();
    solver.printSolution();
}

int main() {
    InOut();
    ios_base::sync_with_stdio(false);
    cin.tie(0);
    cout.tie(0);
    Solve();
    return 0;
}   