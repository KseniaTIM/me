#include <iostream>
#include <fstream>
#include <string>
#include <windows.h>

using namespace std;

bool check_int(string s) {
    bool f = 1;
    for (int i = 0; i < s.length(); i++) {
        if (s[i] < '0' || s[i] > '9') {
            f = 0;
            break;
        }
    }
    return f;
}

class Storage {
public:
    string name, location;
    int day_price, quantity;
};

class Node {
public:
    Node* next = NULL;
    Node* previous = NULL;
    Storage storage;

};

class List {
public:
    Node* Head;
    Node* End ;
    Node* where;
    Node* new_elem;

    List() {
        Head = NULL;
        End = NULL;
    }

    void push_everywhere(Storage storage, int position = INT_MAX) {
        if (Head == NULL) {
            Head = new Node;
            Head->storage = storage;
            End = Head;
            return;
        }

        where = Head;
        while (where != NULL) {
            if (storage.name == where->storage.name and storage.location == where->storage.location) {
                where->storage.quantity += storage.quantity;
                return;
            }
            where = where->next;
        }

        int counter = 1;
        new_elem = new Node;
        new_elem->storage = storage;
        where = Head;
        while (counter != position and where != NULL) {
            where = where->next;
            counter++;
        }

        if (where == Head) {
            new_elem->next = Head;
            Head->previous = new_elem;
            Head = new_elem;
            return;
        }
        if (where == NULL) {
            End->next = new_elem;
            new_elem->previous = End;
            End = new_elem;
            return;
            }

        where->previous->next = new_elem;
        new_elem->previous = where->previous;
        new_elem->next = where;
        where->previous = new_elem;

    }

    void print_list(int choose) {
        if (Head == NULL) {
            cout << "������ ����!\n";
            return;
        }


        int start = 0, end = 0, count;
        string s;
        while (1) {
            cout << "������� �������� ������:(0 - ����� �� ������ ������)\n";
            cin >> s;
            while (!check_int(s)) {
                cout << "�������� ����!\n";
                cout << "������� �������� ������:(0 - ����� �� ������ ������)\n";
                cin >> s;
            }
            if (s == "0")
                return;
            count = 1;
            start = stoi(s)*5 - 4;
            end = start + 4;
            cout << "��������         ����� ��������    ���������� �������    ���������� ��������\n";
            if (choose == 1) {
                where = Head;
            }
            else {
                where = End;
            }
            while (where != NULL) {
                if (count >= start and count <= end) {
                    cout.setf(ios::left);
                    cout.width(17);
                    cout << where->storage.name;
                    cout.setf(ios::left);
                    cout.width(18);
                    cout << where->storage.location;
                    cout.setf(ios::left);
                    cout.width(22);
                    cout << where->storage.day_price;

                    cout << where->storage.quantity;
                    cout << endl;
                }
                if (choose == 1)
                    where = where->next;
                else
                    where = where->previous;
                count++;
            }
            cout << endl << "�������� �������� " << stoi(s) << endl << endl;
        }
    }

    void remove(int location) {
        if (Head == End) {
            Head = NULL;
            End = NULL;
            return;
        }

        int counter = 1;
        where = Head;
        while (counter != location and where->next != NULL) {
            where = where->next;
            counter++;
        }

        if (where == Head) {
            Head = where->next;
            Head->previous = NULL;
            delete where;
            return;
        }
        if (where == End) {
            End = where->previous;
            End->next = NULL;
            delete where;
            return;
        }

        where->previous->next = where->next;
        where->next->previous = where->previous;
        delete where;
    }


    void print_location(string location) {
        if (Head == NULL) {
            cout << "������ ����!\n";
            return;
        }

        where = Head;
        cout << "��������       ����� ��������    ���������� �������    ���������� ��������\n";
        while (where != NULL) {
            if (where->storage.location == location) {
                cout.setf(ios::left);
                cout.width(17);
                cout << where->storage.name;
                cout.setf(ios::left);
                cout.width(18);
                cout << where->storage.location;
                cout.setf(ios::left);
                cout.width(22);
                cout << where->storage.day_price;
                cout << where->storage.quantity;
                cout << endl;
            }
            where = where->next;
        }
        cout << endl;
    }

    void print_cost(string name) {
        if (Head == NULL) {
            cout << "������ ����!\n";
            return;
        }

        where = Head;
        int count = 0;
        bool flag = 0;
        
        while (where != NULL) {
            if (where->storage.name == name) {
                count += where->storage.day_price * where->storage.quantity;
                flag = 1;
            } 
            where = where->next;
        }
        if (flag) {
            cout << "������� �� ��������� � �����:\n";
            cout << count * 30;
        }
        else
            cout << "������ ��������� ���!";
        cout << endl;
    }

    void save() {
        ofstream fout("text.txt");
        where = Head;
        if (where != NULL) {
            while (where != End) {
                fout << where->storage.name << " " << where->storage.location << " " << where->storage.day_price << " " << where->storage.quantity << endl;
                where = where->next;
            }
            fout << where->storage.name << " " << where->storage.location << " " << where->storage.day_price << " " << where->storage.quantity;
            cout << "���� ��������!\n";
        }
        else {
            cout << "������ ����!\n";
        }
        fout.close();
    }


    void download() {
        Head = NULL;
        End = NULL;
        Storage storage;
        ifstream fin("text.txt");

        if (!fin.is_open()) {
            fin.close();
            ofstream fout("text.txt");
            fout.close();
            ifstream fin("text.txt");
        }

        while (!fin.eof()) {
            int counter = 1;
            fin >> storage.name;
            if (storage.name != "") {
                fin >> storage.location >> storage.day_price >> storage.quantity;
                push_everywhere(storage, counter);
                counter++;
            }
            else
                break;
        }
        cout << "���� ��������!\n";
        fin.close();
    }
};

Storage input(Storage storage) {
    string s, st;
    cout << "������� ��������, ����� �������� � ���������� ������� �� ���� � ���������� ��������:\n";
    cin >> storage.name >> storage.location >> s >> st;
    while (!check_int(s)) {
        cout << "�������� ���� � �������� �����!\n";
        cout << "������� ���������� ����� ������ �����:\n";
        cin >> s;
    }

    while (!check_int(st)) {
        cout << "�������� ���� � ���������� ��������!\n";
        cout << "������� ���������� ����� ���������� ��������:\n";
        cin >> st;
    }
    storage.day_price = stoi(s);
    storage.quantity = stoi(st);
    return storage;
}

void table() {
    cout << "0. �����\n1. ���� ��������\n2. ����� ������\n3. ������� �������\n";
    cout << "4. ����� �������� ������������ ����\n5. ����� ������ �� ������������� ���������\n";
    cout << "6. ���������� � ����\n7. �������� �� �����\n";
}


int main(){
    SetConsoleCP(1251);
    SetConsoleOutputCP(1251);
    List A;
    Storage storage;
    string s,ch = "1";
    int pos,choose;
    string location,name;
   
    while (ch != "0") {
        //system("CLS");
        table();
        cin >> ch;
        while (ch.length() > 1) {
            cout << "������� ������������ ��������\n���������� �����\n";
            table();
            cin >> ch;
        }
        switch (ch[0]) {
        case '0':
            break;
        case '1':
            cout << "������� ������� ������ ��������:\n";
            cin >> s;
            while (!check_int(s)) {
                cout << "�������� ����!\n";
                cout << "������� ������� ������ ��������:\n";
                cin >> s;
            }
            pos = stoi(s);
            A.push_everywhere(input(storage), pos);
            break;
        case '2':
            cout << "1. � ������� �������\n2. � �������� �������\n";
            cin >> s;
            while (!check_int(s)) {
                cout << "�������� ����!\n";
                cout << "1. � ������� �������\n2. � �������� �������\n";
                cin >> s;
            }
            choose = stoi(s);
            A.print_list(choose);
            break;
        case '3':
            cout << "������� ������� ��������:\n";
            cin >> s;
            while (!check_int(s)) {
                cout << "�������� ����!\n";
                cout << "������� ������� ��������:\n";
                cin >> s;
            }
            pos = stoi(s);
            A.remove(pos);
            break;
        case '4':
            cout << "������� ��������� ����:\n";
            cin >> location;
            A.print_location(location);
            break;
        case '5':
            cout << "������� ��� ���������:\n";
            cin >> name;
            A.print_cost(name);
            break;
        case '6':
            A.save();
            break;
        case '7':
            A.download();
            break;
        }
    }
    return 0;
}

