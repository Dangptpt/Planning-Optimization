# TỐI ƯU LẬP KẾ HOẠCH: HARVERST PLANNING

## **Input**:
* N: số cánh đồng
* m: số lượng sản phẩm tối thiểu để nhà máy hoạt động 
* M: số lượng sản phẩm tối đa nhà máy có thể hoạt động
* d(i): Sản lượng của cánh đồng thứ i
* s(i): ngày bắt đầu có thể thu hoạch cánh đồng i  (i =1,2, … N)
* e(i): ngày cuối cùng có thể thu hoạch cánh đồng i (i =1,2, … N)
* min_day: min s(i) (i =1,2, … N)
* max_day: max e(i) (i =1,2, … N)
##### 1 <= N <= 10000, 1 <= m <= M <= 10000 
##### 1 <= d(i) <= 100, 1 <= s(i) <= e(i) <= 10000

## Gennerate test case

Folder Test chứa các test case được sinh ngẫu nhiên:

Filename test{x}_{y}: 
* x: số lượng cánh đồng
* y: max_day

## Algorithm
* Branch & Bound
* Constraint Programming, Interger Programing
* Greedy
* Local Search
* Tabu Search
* Genetic Algorithm