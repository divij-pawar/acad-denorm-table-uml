import pandas as pd

"""
Converted Access Query to python.
"""
# Required files
all_grad_students = pd.read_excel("01_All_Graduating_Students.xlsx")
academic_plans_df = pd.read_excel('Academic_Plans.xlsx')
academic_subplans_df = pd.read_excel('Academic_Sub-Plans.xlsx')
commonwealth_honors_df = pd.read_excel('Commonwealth Honors.xlsx')
external_degrees_df = pd.read_excel('EXTERNAL_DEGREES.xlsx')
hood_colors_df = pd.read_excel("Hood Colors.xlsx")


# Perform LEFT JOINs 
merged_df = all_grad_students.merge(academic_plans_df,left_on='PLAN',right_on='Academic Plan',how='left',suffixes=('', '_academic_plans'))
merged_df = merged_df.drop(columns=["DISSERTATION"])
merged_df = merged_df.merge(academic_subplans_df,left_on=['PLAN', 'SUB PLAN'],right_on=['ACAD_PLAN', 'ACAD_SUB_PLAN'],how='left',suffixes=('', '_academic_subplans'))
merged_df = merged_df.merge(external_degrees_df,on='ID',how='left',suffixes=('', '_external'))
merged_df = merged_df.merge(hood_colors_df,left_on=['PROGRAM', 'DEGREE'],right_on=['PROGRAM', 'DEGREE'],how='left',suffixes=('', '_hood_colors'))
merged_df = merged_df.merge(commonwealth_honors_df[['UMS NUMBER']],left_on='ID',right_on='UMS NUMBER',how='left')

# Apply filters
filtered_df = merged_df[merged_df['CHECKOUT STATUS'] != 'DN']

#Rename Columns
filtered_df = filtered_df.rename(columns={'DIPLOMA_DESCR': 'SUB PLAN DIPLOMA DESCR','ACAD_SUB_PLAN': 'ASP','Academic Plan': 'AP'})

# Compute custom fields
college_to_bbso = {'ED': 5, 'SCI': 3, 'A&S': 1, 'EN': 4, 'MG': 6, 'HP': 2, 'GS': 7}
filtered_df['BBSO'] = filtered_df['College'].map(college_to_bbso)
filtered_df['UKEY'] = filtered_df['ID'].astype(str) + filtered_df['DEGREE'].astype(str)
filtered_df['COMM_HONORS'] = filtered_df['UMS NUMBER'].apply(lambda x: 'Commonwealth Honors' if pd.notnull(x) else '')
filtered_df['CSO'] = ""
# Select and order columns 

final_columns = ["SUB PLAN DIPLOMA DESCR","ID","GRAD_UNIQUE_ID","PLAN TYPE","PLAN SEQUENCE","SUB PLAN DESCR","SUBPLAN TYPE",
"FERPA","DECEASED_FLG","DIPLOMA_NAME","DEGREE","BBSO","NAME","FIRST NAME","MIDDLE NAME","LAST NAME","College","ADDRESS1",
"ADDRESS2","CITY","STATE","ZIP","COUNTRY","COUNTRY DESCR","PERS_EMAIL","UML_EMAIL","PERS_PHONE","CAREER","PROGRAM",
"PROGRAM DESCR","PLAN","PLAN DESCR","DIPLOMA PLAN DESCR","SUB PLAN","CHECKOUT STATUS","CHECKOUT STATUS DESCR",
"EXP GRAD TERM","EXP GRAD TERM DESCR","STRUC_TRNSCR_DESCR","DEGREE DESCR","LATIN HONORS","LEVEL_CD","LEVEL_DESC",
"CUM GPA","UNIV_CREDITS","TOT_CREDITS","TRANSFER EARNED CREDITS","TOT TEST CREDIT","TOT_NOGPA","CUR TOT CUM",
"FINAL TOT CUM","TOT PASSED GPA","TOT PASSED NOGPA","TOT INPROG GPA","TOT_INPROG_NOGPA","TOT_OTHER","TOT TRANSFER CREDIT",
"DATA_DT","EXT_DEGREE1","EXT_DEGREE2","EXT_DEGREE3","EXT_DEGREE4","DISSERTATION","PROBLEMS","THESIS ADVISOR","AP","ASP",
"Hood_Band_Color","COMM_HONORS","CSO","COLLEGE_ABBREV","Ceremony","International","Honors Flag","CMNC Exceptions",
"STUDENT TYPE","DEGREE TYPE","Cbook_XFlag","Term Code","Address Type","ADMIT_TERM_SPP","ADMIT_TERM_SPP_DESCR",
"DocType","Degree First Name","Degree Middle Name","Degree Last Name","Degree Name"]

result_df = filtered_df[final_columns].sort_values(by=['ID', 'PLAN TYPE', 'PLAN SEQUENCE', 'SUB PLAN DESCR'], ascending=[True, False, True, True])

result_df.to_excel('output.xlsx', index=False)