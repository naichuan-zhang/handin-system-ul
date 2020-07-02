// Naichuan Zhang
// 18111521

#include <iostream>
#include <cstring>
#include <cstdlib>
#include <iomanip>
#include <sstream>
#include <string>
#include <cmath>
#include <vector>

using namespace std;

class nz {
  friend ostream &operator<<(ostream &, const nz &);
  
public:
  nz(int col, double val)
  {
    this->col = col;
    this->val = val;
  }

  int getCol() const { return col; }
  double getVal() const { return val; }
  void setCol(int col) { this->col = col; }
  void setVal(double val) { this->val = val; }
  
  int col;
  double val;
};

ostream& operator<<(ostream &output, const nz &a)
{
  output << a.col << " " << a.val << " ";
  return output;
}

int main(int argc, char *argv[])
{
    string line;
    vector< vector< nz > > matrixList;
    vector< nz > row;
    
    while (getline(cin, line))
    {
      std::istringstream lstream(line);
      int col;
      double val;

      row.erase(row.begin(), row.end());
      while (lstream >> col >> val)
      {
        nz next(col, val);
        row.push_back(next);
      }
      matrixList.push_back(row);
    }

    vector< vector< nz > >::iterator i;
    vector< nz >::iterator j;
    
    int leny = matrixList.size();
    int lenx = leny;
    
    vector< vector< nz > > newList(leny, vector< nz >());

    int hangshu = 0;
    for (i = matrixList.begin(); i != matrixList.end(); i++)
    {
      hangshu++;
      for (j = (*i).begin(); j != (*i).end(); j++)
      {
	nz next(hangshu, (*j).getVal());
	newList[(*j).getCol() - 1].push_back(next);
      }
    }
    
    for (i = newList.begin(); i != newList.end(); i++)
    {
      for (j = (*i).begin(); j != (*i).end(); j++)
      {
	cout << (*j) << " ";
      }
      cout << endl;
    }
    
    return 0;
}
