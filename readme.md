This script works for simple quiz with questions of type numerical or multi as
described in the documentation of moodle package for latex.


Warning: in our example setup we actually use an alternate version of moodle.sty (moodlept.sty, as suggested by D. Smania) designed to work better with portuguese language
The moodle package is documented and available in its original version at https://ctan.org/pkg/moodle.



0) check the example source calcquiz.tex
1) compile your quiz (eg calcquiz.tex) with lualatex and the moodle.sty package
(eg in our case, in the terminal:  
$ cd /path/to/calcquiz.tex  
$ lualatex -interaction=nonstopmode calcquiz.tex  
)
2) run the python script calc_hack with input  your tex file name
(eg in our case, in the terminal:  
$ cd /path/to/calc_hack.py  
$ python3 calc_hack.py 'calcquiz.tex'  
)
(using python 2 should work too, please inform me if it is not the case)
3) import the output (in our case calcquiz-moodle-calc.xml) to your moodle platform.

observation:
in the calculated questions, you cannot use latex in the answers.


 after the questions for which you use parameters you must add the
 following lines

 params\\\\  
 a: sa  
 b: sb  

 and so on where a,b,... are the letters used for the parameters
 and sa,sb,... determine the set in which the values are randomly taken (uniformly).

 sa,sb,... can be lists of values like 1,3,7
 or an expression range(m,n), meaning the integer interval [m,n-1]

 after the parameters description you must also add two lines:


 digits\\\\  
 value  

 where value determines both the number of digits calculated in the proposed answers
 and the tolerance when the answer is entered; in this latter case, the tolerance is 10^(-value)

The script will build a calculated question together with datasets of size 100, sampled among the selected values for each
for the parameters.

extra info:  
As of the moodle.sty documentation, one can use the command   \moodleset{feedback={put here your feedback}} within the question text
to add a general feedback to a question. In our experience, a bug appears: the feedback text appears also in the question text.
Since Nov. 2020 the 7th, this is compensated by our script, which removes it from the question text.

more advanced features:
instead of range(m,n) in the description params\\ of the parameters, you can actually use
any python command that returns an iterable (e.g. range(m,n,2))
To enrich the options in this direction, you can add the flag  -n when calling calc_hack (eg  
$ python3 calc_hack.py calcquiz.tex -n  
)

It will import numpy in the beginning of
the script (provided it is installed on your system) and hence allow to use commands
such as numpy.arange(1,5,0.1) or numpy.linspace(0.2,15.9,18) for lists of evenly spaced non necessarily
integer numbers (check https://numpy.org/ for details)
