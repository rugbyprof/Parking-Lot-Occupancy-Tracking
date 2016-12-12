## Final Exam 

### Name _____________________________________
1. Use pencil to answer all questions
2. Do not cram too many answers on a sheet of paper.
- Draw a line between each answer.
- Write neatly and legibly.
- Place your name on all pages turned in.
- Your test should be in ascending order when turned in. 
- Failure to comply with these instructions WILL result in a loss of 1 letter grade.
- Complete the mini assessment at the end of the final.

### Question 1
(25 pts)

Match the following words, with the definition below. Not all definitions will be used. Write your answers on your answer sheet like so: 

- 1: X
- 2: Y
- 3: Z

|  Ans   |       Word                    |   Ans   |       Word                |
|:---:|:-------------------------|:-----:|----------------------|
|  1   | Attributes                 |   7   | Constructor  |
|  2   |     Overloading           |   8   | Class  |
|  3   | Data Member             |    9  | Encapsulation  |
|  4   | Immutable              |   10   | Information Hiding  |
|  5   | Inheritance           |    11  | Instance Variable  |
|  6   | Method                 |   12   | Mutable  |


<div style="page-break-after: always;"></div>

### Question 2
(15 pts)
Given the following fraction class and usage in "main":
```python
def gcd(a, b):
    """Return greatest common divisor using Euclid's Algorithm."""
    while b:      
        a, b = b, a % b
    return a
def lcm(a, b):
    """Return lowest common multiple."""
    return a * b // gcd(a, b)

class Fraction(object):
    def __init__(self,n=1,d=1):
        self.num = n
        self.den = d
        self.reduce()
    def __str__(self):
        return "%d / %d" % (self.num,self.den)
    def reduce(self):
        thegcd = gcd(self.num,self.den)
        self.num /= thegcd
        self.den /= thegcd
      
if __name__=="__main__":
    f1 = Fraction(12,36)
    f2 = Fraction(5,8)
    f3 = f1 + f2
    f4 = f1 * f1
```
Complete the necessary methods needed to overload the specified operators.

<div style="page-break-after: always;"></div>

### Question 3
(20 pts)

Given the following dictionary:

```python
books = [
{"Author":"Pratchett", "Title":"Nightwatch", "Genre":"fantasy"},
{"Author":"Pratchett", "Title":"Thief Of Time", "Genre":"fantasy"},
{"Author":"Le Guin", "Title":"The Dispossessed", "Genre":"scifi"},
{"Author":"Le Guin", "Title":"A Wizard Of Earthsea", "Genre":"fantasy"},
{"Author":"Turner", "Title":"The Thief", "Genre":"fantasy"},
{"Author":"Phillips", "Title":"Preston Diamond", "Genre":"western"},
{"Author":"Phillips", "Title":"Twice Upon A Time", "Genre":"scifi"}
]
```

- **3A)** Print out the "Author" of the first book.
- **3B)** Print out all the "Titles" in the dictionary.
- **3C)** Print out all the books that are not "scifi".
- **3D)** Add the following book to the `books` dictionary:
    - Author: Scott Meyer
    - Title: Off to Be the Wizard
    - Genre scifi

<div style="page-break-after: always;"></div>

### Question 4
(10 pts)

Using the book dictionary as a guide, write a `book class` that has the same items in each book (author,title,genre) as data members of your class. 


<div style="page-break-after: always;"></div>


### Question 5
(10 pts)

If you were to write a class called `library`, would you `inherit` from your `book` class or would you use `composition`? Explain your choice. Make sure you define (in layman's terms) `inheritance` and `composition`. 

<div style="page-break-after: always;"></div>

### Question 6
(15 pts)

Write a class called `library` that will store a list of books. It should contain the following methods:

- add: lets you add a book
- delete: lets you delete a book but also return an instance of the book
- print_lib: prints the library out in a nice readable format.

<div style="page-break-after: always;"></div>

### Question 7 
(10 pts)

Median Trickery

Find the median value in a list of values. 
    
```python
def myMedian(L):
""" 
@Description: Return the median of the numbers in L.
@Params: L (list)
@Returns: median (int)
"""





```




<div style="page-break-after: always;"></div>

#### Assessment:

Failure to complete assessment  will result in failure on the final exam.

|    |  Question                                             |        Answer                  |
|----|-------------------------------------------------------|--------------------------|
| 1 | What is your expected grade in this course:?  | A - B - C - D - F      |
| 2 | What did you earn in CS 1?	 (A,B,C) | A - B - C   |
| 3 | On a scale of 1-10 (10 being the hardest), on average, how hard were the programs? |  1 2 3 4 5 6 7 8 9 10     |
| 4 | On a scale of 1-10 (10 being the hardest), on average, how hard was the course? | 1 2 3 4 5 6 7 8 9 10    |
| 5 | Did you turn in all your programs? | Yes - No   |
| 6 | Did all your programs run (of the ones turned in)? | Yes - No  | 
| 7 | Are you taking advanced structures and algorithms next semester?  | Yes - No    | 
| 8 | Are you a Computer Science Major?  | Yes - No  | 
| 9 | If you answered no to number 8, what is your major? | "__________________________ "   | 

<div style="page-break-after: always;"></div>

| #    |    Definition                                          |
|:---:|----------------------------------------------|
| A | The transfer of the characteristics of a class to other classes that are derived from it. |
| B | An individual object of a certain class. `x = some_class` x is now an __________________ of `some_class` |
| C | The creation of an instance of a class. |
| D | A special kind of function that is defined in a class definition. |
| E | Is a feature of some object-oriented computer programming languages in which an object or class can inherit characteristics and features from more than one parent object or parent class. It is distinct from single inheritance, where an object or class may only inherit from one particular object or class. |
| F | An object which can be modified after it is created. |
| G | A unique instance of a data structure that's defined by its class and is comprised of both data members and methods. |
| H | The assignment of more than one function to a particular operator. |
|I | The data within an object. This data represents the objects "state" and is typically the subject of an objects methods. | 
| J | A user-defined prototype that contains data and methods to alter said data. |
| K | It is a special type of subroutine called to create an object. It prepares the new object for use, often accepting arguments used to set required member variables. |
| L | A class variable or instance variable that holds data associated with a class and its objects. |
| M | A method which is automatically invoked when the object is destroyed. |
| N | A language mechanism for restricting access to some of the object's components, also a language construct that facilitates the bundling of data with the methods (or other functions) operating on that data. | 
| O | Is an object whose state cannot be modified after it is created. | 
