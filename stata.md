# Stata Complete Reference


---

# CHAPTER 1: GETTING STARTED WITH STATA


## Remarks

Stata is a general-purpose statistical software package created by StataCorp in 1985. It is widely used in economics, epidemiology, sociology, and political science. Stata provides data management, statistical analysis, graphics, and programming capabilities. Commands are entered in a command window or do-files.

Tools: Stata (commercial, versions IC/SE/MP), free alternatives: gretl (partial compatibility).


## Hello World

```stata
* hello.do
display "Hello, World!"
display "Hello, Stata!"

* This is a single-line comment
/* This is a multi-line
   comment */
```

```stata
* Run a do-file
do hello.do

* Or type commands directly in the Command window
. display "Hello!"
Hello!
```

### Basic Workflow

```stata
* 1. Start a log file
log using "my_analysis.log", replace

* 2. Load data
use "my_data.dta", clear
* or: import delimited "data.csv", clear

* 3. Explore data
describe
summarize
list in 1/10

* 4. Analyze
regress y x1 x2 x3

* 5. Save results
estimates save "model1.ster", replace

* 6. Close log
log close
```


---

# CHAPTER 2: DATA MANAGEMENT


## Working with Datasets

```stata
* === LOADING DATA ===
use "dataset.dta", clear               // load Stata format
import delimited "data.csv", clear     // import CSV
import excel "data.xlsx", firstrow clear  // import Excel
import excel "data.xlsx", sheet("Sheet2") firstrow clear

* === SAVING DATA ===
save "output.dta", replace
export delimited "output.csv", replace
export excel "output.xlsx", firstrow(variables) replace

* === EXAMINING DATA ===
describe                   // variable names, types, labels
describe var1 var2
summarize                  // statistics for all vars
summarize income age educ
list                       // show all observations
list in 1/20               // first 20 rows
list name age if age > 30  // conditional list
count                      // number of observations
count if income > 50000

* === VARIABLE TYPES ===
* byte, int, long   : integers (8,16,32-bit)
* float, double     : floating point
* str1-str2045      : strings
* strL              : long strings

* Check types
codebook age
codebook, compact

* === GENERATE AND REPLACE ===
generate income_log = log(income)
generate high_inc = (income > 50000)         // boolean
generate age_sq = age^2
generate name_len = strlen(name)

replace income = . if income < 0             // set to missing
replace income = 0 if income == .            // replace missing

* === LABELS ===
label variable income "Annual income (USD)"
label define genderl 0 "Male" 1 "Female"
label values gender genderl
label list genderl

* === RENAME AND DROP ===
rename oldname newname
rename (old1 old2) (new1 new2)
drop if income < 0
drop var1 var2
keep id income age gender
```


---

# CHAPTER 3: DATA MANIPULATION


## Transforming Data

```stata
* === SORTING ===
sort age                          // ascending
gsort -age                        // descending
gsort -income age                 // multiple vars

* === DUPLICATES ===
duplicates report id
duplicates drop id, force         // drop duplicates (keep first)
duplicates drop                   // drop exact duplicates

* === MISSING VALUES ===
count if missing(income)          // count missings
count if income == .
list if missing(income)
drop if missing(income, age)      // drop if any missing

* Fill missing:
replace income = 0 if income == .
ipolate income time, gen(income_interp)  // interpolate

* === MERGE ===
* Sort both datasets by key first
sort id
merge 1:1 id using "other_data.dta"
* merge types: 1:1, m:1, 1:m, m:m

* After merge, _merge variable:
* 1=master only, 2=using only, 3=matched
tab _merge
keep if _merge == 3               // keep matched only
drop _merge

* === APPEND ===
append using "more_data.dta"

* === RESHAPE ===
* Wide to long:
reshape long score, i(id) j(time)

* Long to wide:
reshape wide score, i(id) j(time)

* === COLLAPSE (aggregate) ===
collapse (mean) income (sum) sales (count) n=id, by(region year)

* === EXPAND ===
expand 2                          // duplicate each observation

* === ENCODE/DECODE ===
encode string_var, gen(numeric_var)    // string to numeric
decode numeric_var, gen(string_var2)   // numeric to string
```


---

# CHAPTER 4: STATISTICS


## Statistical Analysis

```stata
* === DESCRIPTIVE STATISTICS ===
summarize income, detail          // includes percentiles
tabstat income age, stat(n mean sd min p25 median p75 max)
tabulate gender                   // frequency table
tabulate gender educ              // cross-tabulation
tabulate gender, chi2             // chi-square test

* === T-TESTS ===
ttest income == 50000             // one-sample
ttest income, by(gender)          // two-sample (independent)
ttest pre == post                 // paired t-test

* === ANOVA ===
oneway income region
anova income region
anova income region##gender       // two-way with interaction

* Post-hoc:
pwmean income, over(region) mcompare(tukey) effects

* === CORRELATION ===
correlate income age educ
pwcorr income age educ, sig       // with p-values
spearman income age               // Spearman rank correlation

* === LINEAR REGRESSION ===
regress income age educ experience gender
* View results:
display r(r2)                     // R-squared
display e(r2)                     // after estimation
ereturn list                      // all stored estimates

* Robust standard errors:
regress income age educ, robust

* Clustered SE:
regress income age educ, cluster(firm_id)

* === DIAGNOSTICS ===
predict yhat, xb                  // fitted values
predict resid, residuals          // residuals
predict leverage, leverage        // hat values
rvfplot                           // residual vs fitted plot
hettest                           // Breusch-Pagan test
estat vif                         // variance inflation factors
dwstat                            // Durbin-Watson

* === LOGISTIC REGRESSION ===
logit employed age educ income
logistic employed age educ        // displays odds ratios
probit employed age educ          // probit model

* Marginal effects:
margins, dydx(*)                  // average marginal effects
margins, at(age=(20(5)65))        // predicted prob at ages

* === INSTRUMENTAL VARIABLES ===
ivregress 2sls income (educ = parent_educ), robust
```


---

# CHAPTER 5: PANEL DATA


## Longitudinal and Panel Analysis

```stata
* === DECLARE PANEL DATA ===
xtset firm_id year               // panel id and time vars
xtset id time, delta(1)          // declare with time increment

* === PANEL SUMMARY ===
xtdescribe
xtsum income age                 // between/within variation

* === FIXED EFFECTS ===
xtreg income age educ, fe        // within estimator
xtreg income age educ, fe robust // with robust SE

* === RANDOM EFFECTS ===
xtreg income age educ, re        // GLS estimator
xtreg income age educ, re robust

* Hausman test (FE vs RE):
xtreg income age educ, fe
estimates store fixed
xtreg income age educ, re
hausman fixed .

* === FIRST DIFFERENCES ===
xtreg D.income D.age, nocons

* === DYNAMIC PANEL ===
xtabond income age educ, lag(1)  // Arellano-Bond
xtdpd income L.income age, dgmmiv(income) lgmmiv(age)

* === SURVIVAL ANALYSIS ===
stset time, failure(died)
stsum
sts graph                        // Kaplan-Meier curve
stcox age gender treatment       // Cox proportional hazards
streg age gender, dist(weibull)  // parametric

* === TIME SERIES ===
tsset date
tssmooth ma ma_income = income, window(3)  // moving average
ac income, lags(20)              // autocorrelogram
pac income, lags(20)             // partial autocorrelogram

arima income, ar(1) ma(1)        // ARIMA(1,1,1): add d() for I
arima D.income, ar(1) ma(1)
predict forecast, dynamic(2026)
```


---

# CHAPTER 6: GRAPHICS


## Stata Plots

```stata
* === BASIC PLOTS ===
histogram income
histogram income, bin(20) normal

twoway scatter income age
scatter income age

twoway line gdp year
line gdp year

* === CUSTOMIZATION ===
scatter income age, ///
    title("Income vs Age") ///
    xtitle("Age") ytitle("Income (USD)") ///
    msymbol(circle) mcolor(blue) ///
    legend(off)

* === MULTIPLE GRAPHS ===
twoway (scatter income age) (lfit income age), ///
    legend(label(1 "Data") label(2 "Fitted"))

twoway (scatter income age if gender==0, mcolor(blue)) ///
       (scatter income age if gender==1, mcolor(red)), ///
       legend(label(1 "Male") label(2 "Female"))

* === GRAPH TYPES ===
bar income, over(region)
graph bar income, over(region) over(year)

graph pie, over(region) plabel(_all percent)

graph box income, over(gender)
graph hbox income, over(region) nooutside

* Kernel density:
kdensity income
kdensity income, normal bw(5000)

* === REGRESSION PLOTS ===
avplot age                        // added variable plot
rvfplot                           // residual vs fitted
rvpplot age                       // residual vs predictor

* Marginal effects plot:
margins gender, at(age=(20(5)65))
marginsplot

* === SAVING GRAPHS ===
graph export "scatter.png", replace width(1200)
graph export "plot.pdf", replace
graph save "myplot.gph", replace
```


---

# CHAPTER 7: PROGRAMMING


## Stata Programming

```stata
* === LOCALS AND GLOBALS ===
local x = 42
display `x'                       // Note: backtick+quote

global dataset "mydata"
use "$dataset.dta", clear

* String locals:
local name "Alice"
display "Hello, `name'!"

* Computed locals:
local n = _N                      // number of observations
local mean_inc = r(mean)          // from summarize

* === LOOPS ===
* forvalues (numeric):
forvalues i = 1/10 {
    display `i'
}

forvalues y = 2000(1)2026 {
    use "data_`y'.dta", clear
    save "clean_`y'.dta", replace
}

* foreach (list):
foreach var in income age educ {
    summarize `var'
}

foreach file in "data1" "data2" "data3" {
    use "`file'.dta", clear
    * process...
}

* foreach (varlist):
foreach var of varlist income-gpa {
    replace `var' = 0 if `var' == .
}

* === PROGRAMS (user-defined commands) ===
program define mystat
    syntax varlist [if] [in] [, Level(real 95)]
    marksample touse
    foreach v of varlist `varlist' {
        summarize `v' if `touse'
        display "Mean of `v': " r(mean)
    }
end

mystat income age
mystat income if gender==1

* === FRAMES (Stata 16+) ===
frame create myframe
frame myframe: use "data.dta", clear
frame myframe: summarize income
frame copy myframe backup

* === MATA (Matrix language) ===
mata:
    A = (1,2,3 \ 4,5,6 \ 7,8,9)
    b = (1\2\3)
    x = lusolve(A, b)
    x
    eigenvalues(A, 0)
end
```


---

# CHAPTER 8: ADVANCED ANALYSIS


## Advanced Stata Features

```stata
* === MULTIPLE IMPUTATION ===
mi set wide
mi register imputed income educ
mi impute regress income age educ gender, add(20) rseed(42)
mi estimate: regress y income age educ

* === SURVEY DATA ===
svyset psu [pw=weight], strata(strata)
svy: mean income
svy: regress income age educ

* === BOOTSTRAP ===
bootstrap r(mean), reps(1000) seed(42): summarize income
bootstrap _b, reps(500): regress income age educ

* === SIMULATION ===
clear
set obs 1000
set seed 42
generate x = rnormal(0, 1)
generate epsilon = rnormal(0, 0.5)
generate y = 2 + 3*x + epsilon
regress y x

* === DIFFERENCE-IN-DIFFERENCES ===
generate post = (year >= 2020)
generate treated = (group == 1)
generate dd = post * treated

regress outcome post treated dd, robust cluster(id)

* === REGRESSION DISCONTINUITY ===
rdrobust outcome forcing_var, c(0)
rdplot outcome forcing_var, c(0)

* === QUANTILE REGRESSION ===
qreg income age educ, quantile(0.5)   // median regression
sqreg income age educ, quantile(.25 .5 .75)  // simultaneous

* === FACTOR ANALYSIS ===
factor var1 var2 var3 var4 var5, pcf factors(2)
rotate, varimax

* === CLUSTER ANALYSIS ===
cluster kmeans var1-var5, k(3) start(krandom) gen(cluster_id)
cluster dendrogram

* === POSTESTIMATION ===
estimates store model1
regress income age educ i.region
estimates store model2
estimates table model1 model2, star stats(N r2)

* AIC/BIC:
estat ic

* Predictions:
predict xb_m1, xb
predict se_m1, stdp

* Coefficient table to dataset:
regsave using "coefs.dta", replace tstat pval

* === EXPORTING RESULTS ===
* outreg2 (user-written):
ssc install outreg2
regress income age educ
outreg2 using "results.doc", replace

* esttab/estout:
ssc install estout
esttab model1 model2 using "table.tex", ///
    cells(b(star fmt(3)) se(par fmt(3))) ///
    stats(N r2) replace
```
