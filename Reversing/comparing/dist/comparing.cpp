#include <iostream>
#include <algorithm>
#include <vector>
#include <string>
#include <numeric>
#include <map>
#include <cmath>
#include <set>
#include <fstream>
#include <queue>
#include <unordered_map>
#include <cstring>
#include <list>
#include <cassert>
#include <tuple>
using namespace std;

class Compare {
public:
    bool operator()(tuple<char, char, int> a, tuple<char, char, int> b) {
        return static_cast<int>(get<0>(a)) + static_cast<int>(get<1>(a)) > static_cast<int>(get<0>(b)) + static_cast<int>(get<1>(b));
    }
};

string even(int val1, int val3, int ii) {
    string out = to_string(val1) + to_string(val3) + to_string(ii);
    string x = to_string(val1) + to_string(val3);
    for (int i = x.size() - 1; i >= 0; i--) {
        out += x[i];
    }
    return out;
}

string odd(int val1, int val3, int ii) {
    int out = stoi(to_string(val1) + to_string(val3) + to_string(ii));
    int i = 0;
    int addend = 0;
    while (i < 100) { addend += i; i++; }
    i--;
    while (i >= 0) { addend -= i; i--; }
    return to_string(out + addend);
}

int main()
{
    string flag = "REDACTED";
    priority_queue<tuple<char, char, int>, vector<tuple<char, char, int>>, Compare> pq;
    for (int i = 0; i < flag.size() / 2; i++) {
        tuple<char, char, int> x = { flag[i * 2],flag[i * 2 + 1],i };
        pq.push(x);
    }
    vector<string> out;
    while (!pq.empty()) {
        int val1 = static_cast<int>(get<0>(pq.top()));
        int val2 = static_cast<int>(get<1>(pq.top()));
        int i1 = get<2>(pq.top());
        pq.pop();
        int val3 = static_cast<int>(get<0>(pq.top()));
        int val4 = static_cast<int>(get<1>(pq.top()));
        int i2 = get<2>(pq.top());
        pq.pop();
        if (i1 % 2 == 0) { out.push_back(even(val1, val3, i1)); }
        else { out.push_back(odd(val1, val3, i1)); }
        if (i2 % 2 == 0) { out.push_back(even(val2, val4, i2)); }
        else { out.push_back(odd(val2, val4, i2)); }
    }
    for (int i = 0; i < out.size(); i++) {
        cout << out[i] << endl;
    }
}
