## 1063 Data Structures
***Test 1***

- Use only pencil
- Write answers on this sheet
- Write neatly
- Don't get caught up on any single question, use your time wisely.


### 1: List or Array
-----

- ____________________ Grow and shrink dynamically
- ____________________ Give access each element directly
- ____________________ Inserting and Deleting elements is easy
- ____________________ Doesn't have as much overhead
- ____________________ Has easier of implementation


### 2: Pointers
-----

Use the following memory snapshot to answer the questions. Write in the address, the value, or error.

| Memory Snapshot |
|:-------------:|
| ![](https://d3vv6lp55qjaqc.cloudfront.net/items/1s0J3A0J2T3i1l0p2g2b/pointer_memory.png?X-CloudApp-Visitor-Id=1094421) |

| Command           | Result |
|:-----------------:|:------:|
|  `cout<<&D`       |        |
|  `cout<<&E`       |        |
|  `cout<<*D`       |        |
|  `cout<<*F`       |        |
|  `cout<<F`        |        |
|  `cout<<A`        |        |
|  `cout<<*E`       |        |
| `cout<<&G`        |        |
| `C = &A; cout<<*C`|        |
|  `*F=*D; cout<<*F`|        |

### 3: 2D Arrays
-----

This wasn't on the study guide, but you should know this from your program. Write a snippet of code that would generate the array below. Assume that the array is declared and filled with zero's:

```cpp
int A[5][5] = {{0}}; 
```
| 1  | 2  | 3  | 4  | 5  |
|----|----|----|----|----|
| 6  | 7  | 8  | 9  | 10 |
| 11 | 12 | 13 | 14 | 15 |
| 16 | 17 | 18 | 19 | 20 |

### 4: Class Syntax
-----

Write a class definition for a class called CharManip. It doesn’t have any private members. It will have 4 member functions (just write the class definitions, not all the code for the functions):

1. ***UpperCase*** (changes all the characters in a character array from lower to uppercase.)
1. ***LowerCase*** (changes all the characters in a character array from upper to lowercase)
1. ***RetInt*** (returns the ascii (integer) value of a single character)
1. ***Reverse*** (returns the character array reversed)

### 5: List Function
-----

Write a function that receives a `Head` Node pointer and returns `True` if each of the values in the list is even and `Odd` otherwise.

### 6: List Creation
-----

Create an entirely new linked list from the following commands (remember it may not turn out perfect):

```cpp
Node * nhead;
Node * CurrentNode;
Node * PreviousNode;
CurrentNode = new Node;
nhead = CurrentNode;
CurrentNode->Next = NULL;
CurrentNode->Data = 10;
PreviousNode = CurrentNode;
CurrentNode = new Node;
CurrentNode->Next = NULL;
CurrentNode->Data = 8;
PreviousNode->Next = CurrentNode;
CurrentNode = new Node;
CurrentNode->Next = NULL;
CurrentNode->Data = 12;
PreviousNode->Next = CurrentNode;
CurrentNode = new Node;
CurrentNode->Next = NULL;
CurrentNode->Data = nhead->data+4;
PreviousNode->Next = CurrentNode;
Node* Temp = new Node;
Temp->Data = 99;
Temp->Next = nHead;
Nhead = Temp;
```

```
        
        
```

![](https://d3vv6lp55qjaqc.cloudfront.net/items/2b3b2A1U3l3E1a32000u/dupes.png?X-CloudApp-Visitor-Id=1094421)


```
          nHead               PreviousNode              CurrentNode           Temp
```


### 7: List Manipulation
-----

| Linked List Example |
|:-------------:|
| ![](https://d3vv6lp55qjaqc.cloudfront.net/items/020M2443090H3x1O0M2K/Screen%20Shot%202017-02-10%20at%2012.01.07%20PM.png) |
| For each question involving this list, assume a fresh list. |

Given: 

```cpp
struct Node{
    int Data;
    Node* Next;
};
```

Write an update linked list after the following snippet is run:

```cpp
CurPtr = head;
while(CurPtr->Data < 32){
    CurPtr=CurPtr->Next;
}
head=CurPtr;
```

![](https://d3vv6lp55qjaqc.cloudfront.net/items/3k3A1A3Q3X3m1s0M290k/listhelp.png?X-CloudApp-Visitor-Id=1094421)
-----

Write an updated linked list after the following commands get executed:

```cpp
CurPtr = head;
while(CurPtr->next != NULL){
    if(CurPtr->data == 42){
        Node* Temp = CurPtr;
        CurPtr = CurPtr->next;
        delete Temp; 
    }
    CurPtr=CurPtr->next;
}
```
![](https://d3vv6lp55qjaqc.cloudfront.net/items/3k3A1A3Q3X3m1s0M290k/listhelp.png?X-CloudApp-Visitor-Id=1094421)

