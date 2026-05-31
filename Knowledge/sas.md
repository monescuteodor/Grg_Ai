# SAS Complete Reference


---

# CHAPTER 1: GETTING STARTED WITH SAS


## Remarks

SAS (Statistical Analysis System) is a software suite for advanced analytics, business intelligence, data management, and predictive analytics. Originally developed at NC State University (1966-1976), SAS Institute has maintained it commercially. Widely used in pharmaceuticals, finance, and government. SAS programs consist of DATA steps and PROC steps.

Tools: SAS Studio (browser-based), SAS University Edition (free for academics), SAS OnDemand for Academics.


## Hello World

```sas
/* hello.sas */
data _null_;
    put "Hello, World!";
    put "Hello, SAS!";
run;
```

```bash
sas hello.sas           /* run batch mode */
/* Or open SAS Studio and run interactively */
```

### Basic Structure

```sas
/* SAS programs consist of:
   1. DATA steps - read, create, modify datasets
   2. PROC steps - analyze and process datasets
   3. Global statements - apply throughout program
*/

/* Comments: slash-asterisk style */
* This is also a comment ;

/* Libname: define a library (folder) */
libname mylib '/path/to/data';

/* Options */
options nodate nonumber ls=120;

/* Title */
title 'My SAS Analysis';
```


---

# CHAPTER 2: DATA STEP BASICS


## Reading and Creating Data

```sas
/* === CREATING A DATASET FROM SCRATCH === */
data work.students;
    input name $ age score gpa;
    datalines;
Alice 20 85 3.5
Bob 22 92 3.8
Carol 21 78 3.2
Dave 23 95 3.9
Eve 20 88 3.6
;
run;

/* === VARIABLES === */
data work.demo;
    /* Numeric variable */
    x = 42;
    y = 3.14;
    
    /* Character variable ($ suffix declares length) */
    name = 'Alice';
    
    /* Date/time */
    today = today();           /* today's date (numeric) */
    now = datetime();          /* current datetime */
    
    /* Formatted display */
    put today date9.;          /* 25MAY2026 */
    put now datetime20.;
    
    /* Arithmetic */
    z = (x + y) ** 2;         /* ** is power */
    z2 = sqrt(x);
    z3 = abs(-10);
    z4 = log(x);              /* natural log */
    z5 = log10(x);
    z6 = exp(1);              /* e */
    
    /* Integer operations */
    r = mod(10, 3);           /* remainder: 1 */
    f = floor(3.7);           /* 3 */
    c = ceil(3.2);            /* 4 */
    rn = round(3.567, 0.01);  /* 3.57 */
    
    /* Random numbers */
    u = ranuni(0);            /* uniform 0-1 */
    n = rannor(0);            /* standard normal */
run;

/* === LENGTH DECLARATION === */
data work.lengths;
    length name $ 20 city $ 30 score 8;
    name = 'Alice';
    city = 'New York';
    score = 95.5;
run;

/* === READING EXTERNAL DATA === */
data work.fromfile;
    infile '/path/to/data.csv' dlm=',' firstobs=2;
    input id name $ age score;
run;

/* === PROC IMPORT (easier) === */
proc import datafile='/path/to/data.csv'
    out=work.imported
    dbms=csv
    replace;
    getnames=yes;
run;
```


---

# CHAPTER 3: DATA STEP PROGRAMMING


## Data Manipulation

```sas
/* === CONDITIONAL LOGIC === */
data work.classified;
    set work.students;
    
    /* if-then-else */
    if score >= 90 then grade = 'A';
    else if score >= 80 then grade = 'B';
    else if score >= 70 then grade = 'C';
    else grade = 'F';
    
    /* select (case) */
    select (grade);
        when ('A') honor = 'Dean''s List';  /* quote escape: '' */
        when ('B') honor = 'Good Standing';
        otherwise honor = 'Academic Probation';
    end;
    
    /* Conditional output */
    if score >= 85 then output work.honors;
    else output work.regular;
    
run;

/* === LOOPS === */
data work.loops;
    /* DO loop */
    total = 0;
    do i = 1 to 10;
        total = total + i;
    end;
    put total=;   /* total=55 */
    
    /* DO WHILE */
    n = 1;
    do while (n < 100);
        n = n * 2;
    end;
    put n=;       /* n=128 */
    
    /* DO UNTIL */
    m = 0;
    do until (m >= 50);
        m = m + 7;
    end;
    put m=;       /* m=56 */
    
    /* Nested loops */
    do i = 1 to 3;
        do j = 1 to 3;
            cell = i * j;
            output;
        end;
    end;
run;

/* === STRING FUNCTIONS === */
data work.strings;
    s = 'Hello, World!';
    
    len = length(s);              /* 13 */
    up = upcase(s);               /* HELLO, WORLD! */
    lo = lowcase(s);              /* hello, world! */
    sub = substr(s, 1, 5);        /* Hello */
    pos = index(s, 'World');      /* 8 */
    rep = compress(s, ',!');      /* remove chars */
    trm = strip(s);               /* remove leading/trailing spaces */
    cat = cats('Hello', 'World'); /* HelloWorld (no separator) */
    cat2 = catx(' ', 'Hello', 'World'); /* Hello World */
    
    /* Numeric to string */
    n = 42;
    ns = put(n, best12.);         /* '          42' */
    ns2 = strip(put(n, best12.)); /* '42' */
    
    /* String to numeric */
    ns3 = '3.14';
    num = input(ns3, best12.);    /* 3.14 */
    
    put sub= pos= cat2=;
run;
```


---

# CHAPTER 4: PROC STEPS


## Statistical Procedures

```sas
/* === PROC PRINT === */
proc print data=work.students;
    title 'Student Data';
    var name age score gpa;
run;

/* === PROC MEANS === */
proc means data=work.students n mean std min max;
    var score gpa age;
    title 'Descriptive Statistics';
run;

/* === PROC FREQ === */
proc freq data=work.students;
    tables grade / nocum nopercent;
    tables grade * honor / chisq;
run;

/* === PROC SORT === */
proc sort data=work.students out=work.sorted;
    by descending score;
run;

/* === PROC UNIVARIATE === */
proc univariate data=work.students normal;
    var score;
    histogram / normal;
    qqplot / normal;
run;

/* === PROC CORR === */
proc corr data=work.students;
    var score gpa age;
run;

/* === PROC REG === */
proc reg data=work.students;
    model score = age gpa;
    output out=work.predicted predicted=pred residual=resid;
run;

/* === PROC GLM === */
proc glm data=work.students;
    class grade;
    model score = grade;
    means grade / tukey;
    lsmeans grade / pdiff;
run;

/* === PROC LOGISTIC === */
proc logistic data=work.students;
    model pass(event='1') = score gpa;
    output out=work.logpred predicted=prob;
run;

/* === PROC TTEST === */
proc ttest data=work.students;
    class gender;
    var score;
run;

/* === PROC NPAR1WAY (nonparametric) === */
proc npar1way data=work.students wilcoxon;
    class gender;
    var score;
run;
```


---

# CHAPTER 5: DATA MANIPULATION AND MERGING


## Advanced Data Step

```sas
/* === MERGE DATASETS === */

/* Sort both before merging */
proc sort data=work.students; by name; run;
proc sort data=work.scores;   by name; run;

data work.merged;
    merge work.students (in=a)
          work.scores   (in=b);
    by name;
    if a and b;      /* inner join */
    /* if a;         left join */
    /* if b;         right join */
    /* (no filter) = full outer join */
run;

/* === APPEND === */
proc append base=work.all data=work.new force;
run;

/* === WHERE CLAUSE === */
data work.filtered;
    set work.students;
    where score >= 80 and gpa > 3.0;
run;

/* === RENAME AND DROP/KEEP === */
data work.clean;
    set work.students (rename=(score=test_score));
    drop age;          /* remove column */
    /* keep name gpa; */
run;

/* === ARRAYS === */
data work.arrays;
    set work.scores_wide;
    array scores{5} score1-score5;
    
    total = 0;
    do i = 1 to 5;
        total = total + scores{i};
    end;
    avg = total / 5;
    
    /* Boolean array: recode */
    array pass{5};
    do i = 1 to 5;
        pass{i} = (scores{i} >= 70);
    end;
run;

/* === RETAIN === */
data work.cumsum;
    set work.students;
    retain running_total 0;
    running_total = running_total + score;
run;

/* === FIRST. AND LAST. (BY-group processing) === */
proc sort data=work.students; by grade; run;

data work.bygrade;
    set work.students;
    by grade;
    if first.grade then count = 0;
    retain count;
    count + 1;
    if last.grade then output;
run;

/* === LAG FUNCTION === */
data work.lagged;
    set work.timeseries;
    prev_value = lag(value);
    change = value - lag(value);
    pct_change = (value / lag(value) - 1) * 100;
run;
```


---

# CHAPTER 6: MACROS


## SAS Macro Language

```sas
/* === MACRO VARIABLES === */
%let year = 2026;
%let cutoff = 80;
%put The year is &year;          /* prints to log */
%put Cutoff is &cutoff;

/* Use in SQL */
proc sql;
    select * from work.students
    where score >= &cutoff;
quit;

/* === MACROS === */
%macro analyze(dataset=, var=, alpha=0.05);
    proc means data=&dataset;
        var &var;
        title "Analysis of &var in &dataset";
    run;
    
    proc univariate data=&dataset;
        var &var;
        histogram / normal(alpha=&alpha);
    run;
%mend analyze;

/* Invoke macro */
%analyze(dataset=work.students, var=score)
%analyze(dataset=work.students, var=gpa, alpha=0.01)

/* === CONDITIONAL MACRO === */
%macro check(n);
    %if &n > 100 %then %do;
        %put Large N: &n;
    %end;
    %else %do;
        %put Small N: &n;
    %end;
%mend;
%check(50)
%check(200)

/* === MACRO DO LOOP === */
%macro multireg;
    %do i = 1 %to 5;
        proc reg data=work.data&i;
            model y = x1 x2;
        run;
    %end;
%mend;
%multireg

/* === MACRO FUNCTIONS === */
%let str = Hello World;
%put %upcase(&str);      /* HELLO WORLD */
%put %length(&str);      /* 11 */
%put %substr(&str,1,5);  /* Hello */
%put %scan(&str,2);      /* World */

/* === SYMPUT/SYMGET === */
data _null_;
    n = 42;
    call symput('myval', n);       /* data -> macro var */
run;
%put myval = &myval;

data _null_;
    x = symget('myval');           /* macro var -> data */
    put x=;
run;
```


---

# CHAPTER 7: PROC SQL


## SQL in SAS

```sas
/* === BASIC SELECT === */
proc sql;
    select name, age, score
    from work.students
    where score >= 80
    order by score desc;
quit;

/* === AGGREGATION === */
proc sql;
    select grade,
           count(*) as n,
           mean(score) as avg_score,
           std(score) as std_score,
           min(score) as min_score,
           max(score) as max_score
    from work.students
    group by grade
    having count(*) >= 2
    order by grade;
quit;

/* === JOINS === */
proc sql;
    /* Inner join */
    select a.name, a.score, b.department
    from work.students a
    inner join work.departments b
    on a.dept_id = b.dept_id;

    /* Left join */
    select a.*, b.bonus
    from work.employees a
    left join work.bonuses b
    on a.id = b.emp_id;
quit;

/* === CREATE TABLE === */
proc sql;
    create table work.summary as
    select grade,
           count(*) as n,
           mean(score) as avg_score format=8.2
    from work.students
    group by grade;
    
    /* Insert */
    insert into work.students
    values ('Frank', 24, 88, 3.4);
    
    /* Update */
    update work.students
    set gpa = gpa + 0.1
    where score >= 90;
    
    /* Delete */
    delete from work.students
    where score < 60;
quit;

/* === SUBQUERIES === */
proc sql;
    select name, score
    from work.students
    where score > (select mean(score) from work.students);
quit;

/* === INTO MACRO VARIABLE === */
proc sql noprint;
    select mean(score)
    into :avg_score
    from work.students;
quit;
%put Average score: &avg_score;
```


---

# CHAPTER 8: OUTPUT AND ADVANCED FEATURES


## Reporting and ODS

```sas
/* === ODS (OUTPUT DELIVERY SYSTEM) === */

/* HTML output */
ods html file='/output/report.html' style=HTMLBlue;
proc means data=work.students;
    var score gpa;
run;
ods html close;

/* PDF output */
ods pdf file='/output/report.pdf';
title 'Student Analysis Report';
proc print data=work.students; run;
proc freq data=work.students; tables grade; run;
ods pdf close;

/* Excel output */
ods excel file='/output/results.xlsx';
proc print data=work.students; run;
ods excel close;

/* RTF output */
ods rtf file='/output/report.rtf';
proc means data=work.students; run;
ods rtf close;

/* === PROC FORMAT === */
proc format;
    value gradefmt
        90 - 100 = 'A'
        80 -  89 = 'B'
        70 -  79 = 'C'
        60 -  69 = 'D'
              low - 59 = 'F';
    
    value $genderfmt
        'M' = 'Male'
        'F' = 'Female';
run;

data work.formatted;
    set work.students;
    format score gradefmt. gender $genderfmt.;
run;

/* === PROC REPORT === */
proc report data=work.students nowindows;
    column name age score gpa grade;
    define name / display 'Student Name';
    define age  / display 'Age' format=3.;
    define score / display 'Score' format=5.1;
    define gpa  / display 'GPA' format=4.2;
    define grade / display 'Grade';
    
    compute grade;
        if score >= 90 then call define(_col_, 'style',
            'style=[background=green]');
    endcomp;
run;

/* === PROC TABULATE === */
proc tabulate data=work.students;
    class grade;
    var score gpa;
    table grade, (score gpa)*(n mean std);
run;

/* === DEBUGGING === */
options mprint mlogic symbolgen;  /* macro debugging */
options obs=10;                    /* limit rows for testing */
options fullstimer;                /* timing info */

/* Check dataset */
proc contents data=work.students; run;
proc print data=work.students (obs=5); run;
```
