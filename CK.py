import numpy as np
# Dietary intake details (Kcal calculation)
Day = {};Sr_no = {};Food_item = {};Qty={};Diet_Timing={}
Diet = open('Diet_Input.txt',"r")  # Fetch the dietary input from notepad file
for x in Diet.readlines():
 y = x.split('\t')
 col1,col2,col3,col4,col5 = y
 Sr_no[int(col1)] = [int(col1)]
 Day[int(col1)] = [int(col2)]
 Food_item[int(col1)] = [col3]
 Qty[int(col1)] = [float(col4)]
 Diet_Timing[int(col1)] = [col5]
# Total number of days will be fetched from the notepad file itself
NOD = (Day[len(Day)][0])  # Converted to integer from list
# Food Database # Name of food items in database
No_of_items={};F_Food_item={};F_Qty={};Composition={}

# Fetch the food database
Database = open('Food_Database.txt',"r")  
for x in Database.readlines():
 z = x.split('\t')
 col1,col2,col3,col4,col5,col6= z
 No_of_items[int(col1)] = [int(col1)]
 F_Food_item[int(col1)] = [col2]
 F_Qty[int(col1)] = [float(col3)]
 Composition[float(col1)] = [float(col4),float(col5),float(col6)]
# Col4-> Carb, Col5-> Fat, Col6-> Protein
print
a= 1; Not_Found = []; Found = 0
count_np = 0
# Loop for matching the item in food database
while a < len(Food_item)+1:
  if str(Food_item[a]).upper() in str(F_Food_item.values()).upper():
       Found = Found+1
       #print('found',Food_item[a])
       a=a+1
       continue
  else:
   count_np = count_np+1
   Not_Found.append(Food_item[a])
#print ('not found',Food_item[a])
   a=a+1
#print (count_np,'items not found')
#print (str(Not_Found).upper())

# Preallocating carb, fat, protein for every new day
Day_carb =np.zeros((NOD+1,5));Day_fat=np.zeros((NOD+1,5));Day_prot=np.zeros((NOD+1,5));
Day_Total=np.zeros((NOD+1,5))
BF_Total = np.zeros((NOD+1,1)); Lunch_Total = np.zeros((NOD+1,1));
Snacks_Total= np.zeros((NOD+1,1));Dinner_Total = np.zeros((NOD+1,1));
Others_Total = np.zeros((NOD+1,1)); Total_kcal_Tim = np.zeros((NOD+1,1)); 
DC=0;DF=0;DP=0
Carb={}; Fat={}; Prot={}; Total={} # In an item
C=0;F=0;P=0;T=0
Item_not = []

# Loop for dietary intake (i) [Choose an item from dietary intake (DI)]
for i in range(1,len(Sr_no)+1):
 # import pdb
 # pdb.set_trace() 
  # Find pahar (timing)
 Tim = ["Breakfast\n", "Lunch\n", "Snacks\n", "Dinner\n", "Others\n"]
 for k in range(5):
    if Diet_Timing[i][0] == Tim[k]:
     Time_of_eating = k
     break
# Loop for food database (j)  [Compare the food item chosen from DI to food database]
 for j in range(1,len(No_of_items)+1):
   #print (len(No_of_items))
    #if Food_item[i] not in F_Food_item:
    #print (Food_item)
    #print (Food_item[i])
#    print Time_of_eating
   # Calculating caloric composition of food item in DI
   if str(Food_item[i]).upper() == str(F_Food_item[j]).upper():
    Carb[i] = (Composition[j][0])*(Qty[i][0]/F_Qty[j][0])
    Fat[i]  =  (Composition[j][1])*(Qty[i][0]/F_Qty[j][0])
    Prot[i] =  (Composition[j][2])*(Qty[i][0]/F_Qty[j][0])
    Total[i]=  Carb[i]+Fat[i]+Prot[i]   
    
    # Composition of food in a day
    # Macronutrient(Day, Timing)
    Day_carb[Day[i][0]][Time_of_eating] = Day_carb[Day[i][0]][Time_of_eating] + Carb[i]
    Day_fat[Day[i][0]][Time_of_eating]  = Day_fat[Day[i][0]][Time_of_eating] + Fat[i]
    Day_prot[Day[i][0]][Time_of_eating] = Day_prot[Day[i][0]][Time_of_eating] + Prot[i]
    
    
    
    # Calculating total macronutrient in a day (sum of rows of an array)
    Total_Carb = (Day_carb).sum(axis=1)
    Total_Fat = (Day_fat).sum(axis=1)
    Total_Prot = (Day_prot).sum(axis=1)
    Comp_day_wise = np.vstack((Total_Carb,Total_Fat,Total_Prot)).T
    Totalt =  Total_Carb +  Total_Fat +  Total_Prot
    BF_Total[Day[i][0]]     = BF_Total[Day[i][0]]     + Day_carb[Day[i][0]][0] + Day_fat[Day[i][0]][0]+Day_prot[Day[i][0]][0]
    Lunch_Total[Day[i][0]]  = Lunch_Total[Day[i][0]]  + Day_carb[Day[i][0]][1]+Day_fat[Day[i][0]][1]+Day_prot[Day[i][0]][1]
    Snacks_Total[Day[i][0]] = Snacks_Total[Day[i][0]] + Day_carb[Day[i][0]][2]+Day_fat[Day[i][0]][2]+Day_prot[Day[i][0]][2]
    Dinner_Total[Day[i][0]] = Dinner_Total[Day[i][0]] + Day_carb[Day[i][0]][3]+Day_fat[Day[i][0]][3]+Day_prot[Day[i][0]][3]
    Others_Total[Day[i][0]] = Others_Total[Day[i][0]] + Day_carb[Day[i][0]][4]+Day_fat[Day[i][0]][4]+Day_prot[Day[i][0]][4]
    Total_kcal_Tim[Day[i][0]] = BF_Total[Day[i][0]]+Lunch_Total[Day[i][0]]+Snacks_Total[Day[i][0]]+Dinner_Total[Day[i][0]]+Others_Total[Day[i][0]]
    
    BLSD = [np.mean(BF_Total)/ np.mean(Total_kcal_Tim)*100, np.mean(Lunch_Total)/ np.mean(Total_kcal_Tim)*100, np.mean(Snacks_Total)/ np.mean(Total_kcal_Tim)*100, np.mean(Dinner_Total)/ np.mean(Total_kcal_Tim)*100]
    C_P_F = [np.mean(Total_Carb)/np.mean(Totalt)*100, np.mean(Total_Fat)/np.mean(Totalt)*100, np.mean(Total_Prot)/np.mean(Totalt)*100]
    break
#print (C_P_F)
#print (Total_Carb[0])
with open("Health_Report.txt","w") as HR:
 HR.write("Cabohydrate: {0} Fat: {1} Protein: {2}\n".format(int(C_P_F[0]),int(C_P_F[1]),(int(C_P_F[2]))))
 HR.write("Breakfast: {0} Lunch: {1}  Snacks: {2} Dinner: {3}\n".format(int(BLSD[0]),int(BLSD[1]),(int(BLSD[2])),int(BLSD[3])))

#print'Add these items in your database\n', Not_Found
#print len(Not_Found), 'items not found in database'
# print Time_of_eating
