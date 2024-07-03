// Date created: "08:59:41, 17-06-2024"
// Code by Dangptpt_
#include<bits/stdc++.h>

using namespace std;

// Định nghĩa một số tên gọi để giúp mã ngắn gọn hơn
#define fi first
#define se second
#define pb push_back

typedef long long LL;      // Định nghĩa kiểu dữ liệu số nguyên dài
typedef unsigned long long ULL;  // Định nghĩa kiểu dữ liệu số nguyên dài không dấu
typedef pair<int, int> II; // Định nghĩa kiểu dữ liệu cặp số nguyên
typedef pair<int, II> III; // Định nghĩa kiểu dữ liệu cặp bao gồm một số nguyên và một cặp số nguyên

// Hàm đọc dữ liệu vào một biến số nguyên
template <typename T> void read(T &t) {
    t = 0; char ch = getchar(); int f = 1;
    while (!isdigit(ch)) { 
        if (ch == '-') f = -1; 
        ch = getchar(); 
    }
    do { 
        (t *= 10) += ch - '0'; 
        ch = getchar(); 
    } while (isdigit(ch)); 
    t *= f;
}

const int MAXN = 1 + 1e6;  // Định nghĩa kích thước tối đa cho một số mảng
const int mod = 1e9 + 7;   // Định nghĩa giá trị mô-đun lớn
const int inf = 0x3f3f3f3f; // Định nghĩa giá trị vô cực

// Khai báo các biến toàn cục
int n, m, M, max_day, res, mark[MAXN];
LL bit[MAXN], harvest[MAXN];
III p[MAXN]; // Mảng chứa các thông tin về các cánh đồng

// Hàm so sánh để sắp xếp các cánh đồng
bool cmp(III a, III b) {
    if (a.se.fi == b.se.fi) {
        if (a.se.se == b.se.se)
            return a.fi < b.fi;
        else return a.se.se < b.se.se;
    } else return a.se.fi < b.se.fi;
}

// Hàm thiết lập đầu vào và đầu ra
void InOut() {
    #define TASK "../Test/test5000_5000" // Đường dẫn tệp
    freopen(TASK ".inp", "r", stdin);  // Mở tệp đầu vào
    //freopen(TASK ".out", "w", stdout); // Mở tệp đầu ra (nếu cần)
}

// Hàm kiểm tra xem cánh đồng i có thể thu hoạch vào ngày day không
bool check(int i, int sum, int day) {
    if (mark[i] != 0) // Kiểm tra xem cánh đồng đã được thu hoạch chưa
        return 0;
    if (sum > M) // Kiểm tra xem tổng sản lượng có vượt quá M không
        return 0;
    if (day < p[i].se.fi || day > p[i].se.se) // Kiểm tra xem ngày thu hoạch có nằm trong khoảng cho phép không
        return 0;
    return 1;  
}

// Hàm giải quyết bài toán
void Solve() {
    // Đọc dữ liệu đầu vào
    cin >> n >> m >> M;
    for (int i = 1; i <= n; ++i) {
        cin >> p[i].fi >> p[i].se.fi >> p[i].se.se;
        max_day = max(max_day, p[i].se.se); // Cập nhật ngày lớn nhất có thể thu hoạch
        mark[i] = 0; // Khởi tạo trạng thái chưa thu hoạch cho cánh đồng i
    }

    // Sắp xếp các cánh đồng theo thứ tự ưu tiên
    sort(p + 1, p + n + 1, cmp);
    
    // for (int i = 1; i <= n; ++i) cout << p[i].fi << " " << p[i].se.fi << " " << p[i].se.se << '\n';
    
    // Duyệt qua từng ngày từ max_day đến 1
    for (int day = max_day; day > 0; --day) {
        int sum = 0;
        vector<int> tmp; // Lưu trữ các cánh đồng có thể thu hoạch trong ngày
        for (int i = n; i > 0; --i) {
            if (check(i, sum + p[i].fi, day) == 1) {
                mark[i] = day; // Đánh dấu ngày thu hoạch cho cánh đồng i
                sum += p[i].fi; // Cập nhật tổng sản lượng thu hoạch trong ngày
                tmp.push_back(i); // Thêm cánh đồng vào danh sách tạm
            }       
        }
        if (sum < m) { // Nếu tổng sản lượng trong ngày nhỏ hơn m
            for (int i = 0; i < tmp.size(); ++i) 
                mark[tmp[i]] = 0; // Huỷ thu hoạch các cánh đồng trong danh sách tạm
        }
    } 

    int total = 0;
    for (int i = 1; i <= n; ++i) {
        if (mark[i] != 0) { // Đếm số cánh đồng được thu hoạch
            res++;
            total += p[i].fi; // Tính tổng sản lượng thu hoạch
        }
    }

    // In kết quả
    cout << "Total harvested: " << res << '\n' << "Num of fields: " << total;
    // for (int i = 1; i <= n; ++i) {
    //     if (mark[i] != 0) 
    //         cout << i << ' ' << mark[i] << '\n';
    // }
}

// Hàm main
int main() {
    InOut(); // Thiết lập đầu vào và đầu ra
    ios_base::sync_with_stdio(false); // Tối ưu hoá nhập xuất
    cin.tie(0); // Tắt đồng bộ hoá đầu vào với đầu ra
    cout.tie(0); // Tắt đồng bộ hoá đầu ra với đầu vào
    Solve(); // Gọi hàm giải quyết bài toán
    return 0;
}
