# -*- coding: utf-8 -*-
"""
Created on Wed Nov 20 18:14 2019
@author: Gourav Pattnaik

Multiple Linear Regression for N variable
"""

def GvEqn_Prm1_Val(i,n,input_list):
    return str(sum(list(map(mul,input_list[i-1],input_list[n-1]))))

def GvEqn_Prm2_Val(i,input_list):
    return str(sum(input_list[i-1]))

def GvEqn_Prm3_Val(i,input_list):
    return str(sum(map(lambda x:x*x,input_list[i-1])))

def GvEqn_Prm4_Val(i,j,input_list):
    return str(sum(list(map(mul,input_list[i-1],input_list[j-1]))))

def Reg_Cff_List(input_str,n):
    from operator import mul
    SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
    SUP = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")
    reg_cff = []
    
    for i in range(0,n):
        #Capturing regression variable
        reg_var = 'M'+ str(i).translate(SUB)
        gov_eqn_r = str(input_str.split('= ')[1]).split('+')
        for ele in gov_eqn_r:
            if reg_var in ele:
                reg_cff.append(float(ele.split(reg_var)[1]))
    return reg_cff

def print_matrices(Action, Title1, M1, Title2, M2):
    #print(Action)
    #print(Title1, '\t'*int(len(M1)/2)+"\t"*len(M1), Title2)
    for i in range(len(M1)):
        row1 = ['{0:+7.3f}'.format(x) for x in M1[i]]
        row2 = ['{0:+7.3f}'.format(x) for x in M2[i]]
        #print(row1,'\t', row2)
        
def zeros_matrix(rows, cols):
    A = []
    for i in range(rows):
        A.append([])
        for j in range(cols):
            A[-1].append(0.0)

    return A

def copy_matrix(M):
    rows = len(M)
    cols = len(M[0])

    MC = zeros_matrix(rows, cols)

    for i in range(rows):
        for j in range(cols):
            MC[i][j] = M[i][j]

    return MC

def matrices(X,Y):
    AM = copy_matrix(X)
    n = len(X)
    BM = copy_matrix(Y)

    print_matrices('Starting Matrices are:', 'AM Matrix', AM, 
                   'IM Matrix', BM)
    print()

    indices = list(range(n)) # allow flexible row referencing ***
    for fd in range(n): # fd stands for focus diagonal
        fdScaler = 1.0 / AM[fd][fd]
        # FIRST: scale fd row with fd inverse. 
        for j in range(n): # Use j to indicate column looping.
            AM[fd][j] *= fdScaler
        BM[fd][0] *= fdScaler

        # Section to print out current actions:
        string1  = '\nUsing the matrices above, '
        string1 += 'Scale row-{} of AM and BM by '
        string2  = 'diagonal element {} of AM, '
        string2 += 'which is 1/{:+.3f}.\n'
        stringsum = string1 + string2
        val1 = fd+1; val2 = fd+1
        Action = stringsum.format(val1,val2,round(1./fdScaler,3))
        print_matrices(Action, 'AM Matrix', AM, 'BM Matrix', BM)
        print()

        # SECOND: operate on all rows except fd row.
        for i in indices[0:fd] + indices[fd+1:]: # *** skip fd row.
            crScaler = AM[i][fd] # cr stands for "current row".
            for j in range(n): # cr - crScaler*fdRow.
                AM[i][j] = AM[i][j] - crScaler * AM[fd][j]
            BM[i][0] = BM[i][0] - crScaler * BM[fd][0]

            # Section to print out current actions:
            string1  = 'Using matrices above, subtract {:+.3f} *'
            string1 += 'row-{} of AM from row-{} of AM, and '
            string2 = 'subtract {:+.3f} * row-{} of BM '
            string2 += 'from row-{} of BM\n'
            val1 = i+1; val2 = fd+1
            stringsum = string1 + string2
            Action = stringsum.format(crScaler, val2, val1, 
                                      crScaler, val2, val1)
            print_matrices(Action, 'AM Matrix', AM, 
                                   'BM Matrix', BM)
    return BM

from operator import mul
import re

def MulLnrRegression(n,input_list):
    print("No. of variables passed :",n)
    print("\nGoverning Equations for " + str(n) + " variables are as below - ")
    print("----------------------------------------------------------------\n")
    
    SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
    SUP = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")
    
    # AX = B, storing each equation coeffiecients in List A and storing results in List B
    A=[]
    B=[]
    # Forming The Governing Equations Based On Number Of Variables Passed
    for i in range(1,n):
        #print ('ΣX'+str(i).translate(SUB)+'Y =')
        eqn_param1 = 'ΣX'+str(i).translate(SUB)+'Y = '
        eqn_param1_val = GvEqn_Prm1_Val(i,n,input_list)
        #print(eqn_param1_val)
        
        cff_2=''
        cff_2_val=''
        cff_3_final=''
        cff_3_final_val=''
        for j in range(0,n):
            if j==0:
                cff_1 = 'M' + str(j).translate(SUB) + 'ΣX' + str(i).translate(SUB)
                cff_1_val = 'M' + str(j).translate(SUB) + GvEqn_Prm2_Val(i,input_list)
            elif j==i:
                cff_2 = 'M' + str(j).translate(SUB) + 'ΣX' + str(i).translate(SUB) + '2'.translate(SUP)
                cff_2_val = 'M' + str(j).translate(SUB) + GvEqn_Prm3_Val(i,input_list)
            else :
                cff_3='M' + str(j).translate(SUB) + 'ΣX'+str(i).translate(SUB) + 'X' + str(j).translate(SUB)
                cff_3_val = 'M' + str(j).translate(SUB) + GvEqn_Prm4_Val(i,j,input_list)
                cff_3_final = cff_3_final + '+' + cff_3
                cff_3_final_val = cff_3_final_val + cff_3_val

        gov_eqn_rem = eqn_param1 + cff_2 +  cff_3_final + '+' + cff_1
        print("\n")
        print(gov_eqn_rem)
        gov_eqn_rem_val = eqn_param1_val + ' = ' + cff_2_val + '+' + cff_3_final_val + '+' + cff_1_val
        print(gov_eqn_rem_val)
        gov_eqn_l = gov_eqn_rem_val.split('= ')[0]
                
        #Reading coefficients from the governing equations and storing in a list
        reg_cff = Reg_Cff_List(gov_eqn_rem_val,n)
        #print(reg_cff)

        A.append(reg_cff)
        B.append(gov_eqn_l)
    #print(A)
    
   
    ## Forming the First equation of ΣY
    final_eq1_r=''
    final_eq1_r_val=''
    for i in range(0,n):
        if i==0:
            eq_1_param_l = '  ΣY = '
            eq_1_param_l_val = sum(input_list[n-1])
            #print(eq_1_param_l_val)
        else :
            eq_1_param_r ='M' + str(i).translate(SUB) + 'ΣX'+str(i).translate(SUB)
            eq_1_param_r_val = 'M' + str(i).translate(SUB) + str(sum(input_list[i-1]))
            #print(eq_1_param_r_val)
            final_eq1_r = eq_1_param_r + '+' + final_eq1_r
            final_eq1_r_val = eq_1_param_r_val + '+' + final_eq1_r_val
            #print(final_eq1_r_val)
    
    #printing the final equation 1
    gov_eq1 = eq_1_param_l + final_eq1_r + 'M0'.translate(SUB) + 'n'
    gov_eq1_val = str(eq_1_param_l_val) + ' = ' + str(final_eq1_r_val) + 'M0'.translate(SUB) + str(len(input_list[n-1]))
    print("\n")
    print(gov_eq1)
    print(gov_eq1_val)
    
    gov_eqn_l_r = gov_eq1_val.split('= ')[0]
    #print(gov_eqn_l_r)
    
    #Reading coefficients from the governing equation-1 and storing in a list
    reg_cff_1 = Reg_Cff_List(gov_eq1_val,n)
    #print(reg_cff_1)
    
    A.append(reg_cff_1)

    print("\nCoefficients of the Governing Equations are as below - ")
    print("----------------------------------------------------------------\n")
    
    print(A)
    B.append(gov_eqn_l_r)
    #print(B)

    ## Converting elements to list inside a list for result set B
    res = [] 
    for el in B: 
        sub = el.split(', ') 
        res.append(sub) 
    listm = [[None] for i in range(len(res))]
    for i in range(len(res)):
        listm[i][0]=float(res[i][0])

    B = listm
    print(B)
 
    X = matrices(A,B)
    print(X)
	
# Driver Code for 3 variables
#MulLnrRegression(3,[[57,59,49,62,51,50,55,48,52,42,61,57],[8,10,6,11,8,7,10,9,10,6,12,9],[64,71,53,67,55,58,77,57,56,51,76,68]])

# Driver Code for 2 variables
#MulLnrRegression(2,[[7.9,7.92,7.91,7.96,7.98,8.01,8.05,8.06,8.06,8.07,8.09,8.11,8.14,8.17,8.19,8.23,8.27,8.29,8.3],[8.45,8.52,8.25,8.58,8.58,8.63,8.74,8.7,8.61,8.59,8.77,8.8,8.79,8.83,8.91,8.97,8.97,9.04,9.05]])