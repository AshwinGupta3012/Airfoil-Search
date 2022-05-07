from email import message
from email.mime import application
from re import search
from select import select
from tkinter import *
from tkinter import ttk
import tkinter.messagebox
from turtle import left
from urllib import robotparser
import pymysql
import sys
import random
import time

from sklearn import tree

class DataEntryForm:
    def __init__(self,root):
        self.root=root
        self.root.title=("Airfoil predicition System")
        self.root.geometry("1350x750+0+0")
        self.root.configure(background="gainsboro")
        
        Airfoil_Name= StringVar()
        Reynolds_No= StringVar()
        Ncrit=StringVar()
        Mach_No=StringVar()
        Cl_Cd_ratio=StringVar()
        Angle_at_Maximum_Cl_Cd=StringVar()
        Max_Thickness=StringVar()
        Location_of_Max_Thickness=StringVar()
        Max_Camber=StringVar()
        Location_of_Max_Camber=StringVar()
        Search= StringVar()

        Min_thickness=StringVar()
        Min_Camber=StringVar()
        Min_cl_cd=StringVar()

        MainFrame=Frame(self.root,bd=10,width=1000,height=700,relief=RIDGE)
        MainFrame.grid()
        #print("CONTROL1")

        TopFrame1=Frame(MainFrame, bd=5,width=1200, height=200,relief=RIDGE)
        TopFrame1.grid(row=0,column=0)
        TopFrame2=Frame(MainFrame, bd=5,width=1200, height=50,relief=RIDGE)
        TopFrame2.grid(row=1,column=0)
        TopFrame3=Frame(MainFrame, bd=5,width=1200, height=300,relief=RIDGE)
        TopFrame3.grid(row=2,column=0)

        InnerTopFrame1 =Frame(TopFrame1,bd=5,width=1100,height=190,relief=  RIDGE)
        InnerTopFrame1.grid()
        InnerTopFrame2 =Frame(TopFrame2,bd=5,width=1100,height=48,relief=  RIDGE)
        InnerTopFrame2.grid()
        InnerTopFrame3 =Frame(TopFrame3,bd=5,width=1100,height=280,relief=  RIDGE)
        InnerTopFrame3.grid()


        def Reset() :
            Airfoil_Name.set("")
            Reynolds_No.set("50000")
            Ncrit.set("")
            Mach_No.set("")
            Cl_Cd_ratio.set("")
            Angle_at_Maximum_Cl_Cd.set("")
            Max_Thickness.set("")
            Location_of_Max_Thickness.set("")
            Max_Camber.set("")
            Location_of_Max_Camber.set("")
            Min_thickness.set("")
            Min_Camber.set("")
            Min_cl_cd.set("")


        def iExit():
            iExit=tkinter.messagebox.askyesno("Airfoil predicition System", "Confirm if you want to exit")
            if iExit > 0:
                root.destroy()
                return
        

        def Searchdb():
            try: 
                sqlCon=pymysql.connect(host="localhost",user="root",password="Nopassword95",database="airfoil")
                cur=sqlCon.cursor()

                mac=100.0
                mat=100.0
                mic=0.0
                mit=0.0
                max_cl_cd=9999999
                min_cl_cd= -9999999

                #print("CONTROL \n")
                reyno=int(Reynolds_No.get())
                
                if(Cl_Cd_ratio.get()!=""):
                    max_cl_cd=float(Cl_Cd_ratio.get())
                
                  
                if(Min_cl_cd.get()!=""):
                    min_cl_cd=float(Min_cl_cd.get())

                if(Min_Camber.get()!=""):
                    mic=float(Min_Camber.get())
                
                if(Min_thickness.get()!= ""):
                    mit=float(Min_thickness.get())

                if(Max_Thickness.get() != ""):
                    mat=float(Max_Thickness.get())
                
                if(Max_Camber.get()!=""):
                    mac=float(Max_Camber.get())


                #print(mit)
                q = "select Name,reyno,cl_cd,angle_at_max_cl_cd,maxt,maxt_loc,maxc,maxc_loc from airfoildata where maxt<= %f AND maxt>= %f AND maxc<= %f AND maxc>= %f AND cl_cd<= %f AND cl_cd>= %f AND reyno= %d"%(mat,mit,mac,mic,max_cl_cd,min_cl_cd,reyno)
                #cur.execute()
                # q="select * from airfoildataselect * from airfoildata where maxt<="+mat+" AND maxt>="+mit+" AND maxc<="+mac+" AND maxc>="+mic+" AND cl_cd<= "+max_cl_cd+" AND cl_cd>= "+min_cl_cd+" AND reyno= "+reyno+""
                print(q)
                cur.execute(q)
                r=cur.fetchall()
                #print(type(r))

                if len(r)!=0:
                    tree_records.delete(*tree_records.get_children())
                    for row in r:
                        tree_records.insert('',END,values=row)
                        #print(row)
                else:
                    tkinter.messagebox.showinfo("Airfoil predicition System","No Record")
                    Reset()
                sqlCon.commit()
            except:
                tkinter.messagebox.showinfo("Airfoil predicition System","Error in connection")
                Reset()

                sqlCon.close()
        

        lblMaxt =Label(InnerTopFrame1,font=('arial',12,'bold'),text="Max. Thickness",bd=10)
        lblMaxt.grid(row=0,column=0,sticky=W)
        txtMaxt=Entry(InnerTopFrame1,font=('arial',12,'bold'),bd=5, width=28,justify='left',textvariable=Max_Thickness)
        txtMaxt.grid(row=0,column=1)

        lblMaxC=Label(InnerTopFrame1,font=('arial',12,'bold'),text="Max. Camber",bd=10)
        lblMaxC.grid(row=1,column=0,sticky=W)
        txtMaxC=Entry(InnerTopFrame1,font=('arial',12,'bold'),bd=5, width=28,justify='left',textvariable=Max_Camber)
        txtMaxC.grid(row=1,column=1)

        lblMaxR=Label(InnerTopFrame1,font=('arial',12,'bold'),text="Max. Cl/Cd ratio",bd=10)
        lblMaxR.grid(row=2,column=0,sticky=W)
        txtMaxR=Entry(InnerTopFrame1,font=('arial',12,'bold'),bd=5, width=28,justify='left',textvariable=Cl_Cd_ratio)
        txtMaxR.grid(row=2,column=1)

        self.lbMinT=Label(InnerTopFrame1,font=('arial',12,'bold'),text="Minimum Thickness",bd=10)
        self.lbMinT.grid(row=0,column=2,sticky=W)
        self.txtMinT=Entry(InnerTopFrame1,font=('arial',12,'bold'),bd=5, width=28,justify='left',textvariable=Min_thickness)
        self.txtMinT.grid(row=0,column=3)

        self.lbMinC=Label(InnerTopFrame1,font=('arial',12,'bold'),text="Minimum Camber",bd=10)
        self.lbMinC.grid(row=1,column=2,sticky=W)
        self.txtMinC=Entry(InnerTopFrame1,font=('arial',12,'bold'),bd=5, width=28,justify='left',textvariable=Min_Camber)
        self.txtMinC.grid(row=1,column=3)

        self.lbMinR=Label(InnerTopFrame1,font=('arial',12,'bold'),text="Minimum Cl/Cd ratio",bd=10,)
        self.lbMinR.grid(row=2,column=2,sticky=W)
        self.txtMinR=Entry(InnerTopFrame1,font=('arial',12,'bold'),bd=5, width=28,justify='left',textvariable=Min_cl_cd)
        self.txtMinR.grid(row=2,column=3)

        #self.lblocMT=Label(InnerTopFrame1,font=('arial',12,'bold'),text="Location Max. Thickness",bd=10)
        #self.lblocMT.grid(row=0,column=4,sticky=W)
        #self.txtlocMT=Entry(InnerTopFrame1,font=('arial',12,'bold'),bd=5, width=20,justify='left')
        #self.txtlocMT.grid(row=0,column=5)

        #self.lblocMC=Label(InnerTopFrame1,font=('arial',12,'bold'),text="Location Max. Camber",bd=10)
        #self.lblocMC.grid(row=1,column=4,sticky=W)
        #self.txtlocMC=Entry(InnerTopFrame1,font=('arial',12,'bold'),bd=5, width=20,justify='left')
        #self.txtlocMC.grid(row=1,column=5)

        self.lblReyNo=Label(InnerTopFrame1,font=('font',12,'bold'),text="Reynold's Number",bd=10)
        self.lblReyNo.grid(row=3,column=0,sticky=W)

        self.cboReyNo=ttk.Combobox(InnerTopFrame1,font=('font',12,'bold'),width=19, textvariable=Reynolds_No)
        self.cboReyNo['value']=('50000','100000','200000','1000000')
        self.cboReyNo.current(0)
        self.cboReyNo.grid(row=3,column=1)

        

        scroll_x=Scrollbar(InnerTopFrame3,orient=HORIZONTAL)
        scroll_y=Scrollbar(InnerTopFrame3, orient=VERTICAL)

        tree_records=ttk.Treeview(InnerTopFrame3,height=13,columns=("Airfoil_Name","Reynolds_No","Cl_Cd_ratio", "Angle_at_Maximum_Cl_Cd","Max_Thickness","Location_of_Max_Thickness","Max_Camber","Location_of_Max_Camber"),xscrollcommand=scroll_x.set,yscrollcommand=scroll_y.set)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_x.pack(side=BOTTOM, fill=Y)

        tree_records.heading("Airfoil_Name",text="Airfoil_Name")
        tree_records.heading("Reynolds_No",text="Reynolds_No")
        tree_records.heading("Cl_Cd_ratio",text="Cl_Cd_ratio")
        tree_records.heading("Angle_at_Maximum_Cl_Cd",text="Angle_at_Maximum_Cl_Cd")
        tree_records.heading("Max_Thickness",text="Max_Thickness")
        tree_records.heading("Location_of_Max_Thickness",text="Location_of_Max_Thickness")
        tree_records.heading("Max_Camber",text="Max_Camber")
        tree_records.heading("Location_of_Max_Camber",text="Location_of_Max_Camber")

        tree_records['show']='headings'

        tree_records.column("Airfoil_Name",width=150)
        tree_records.column("Reynolds_No",width=110)
        tree_records.column("Cl_Cd_ratio",width=80)
        tree_records.column("Angle_at_Maximum_Cl_Cd",width=150)
        tree_records.column("Max_Thickness",width=100)
        tree_records.column("Location_of_Max_Thickness",width=170)
        tree_records.column("Max_Camber",width=100)
        tree_records.column("Location_of_Max_Camber",width=150)

        tree_records.pack(fill=BOTH,expand=1)

        self.btnSr=Button(InnerTopFrame2,pady=1,bd=4,font=('font',12,'bold'),width=23,text="Search",command=Searchdb)
        self.btnSr.grid(row=0,column=1,padx=3)

        self.btnRt=Button(InnerTopFrame2,pady=1,bd=4,font=('font',12,'bold'),width=23,text="Reset", command=Reset)
        self.btnRt.grid(row=0,column=0,padx=3)

        self.btnEt=Button(InnerTopFrame2,pady=1,bd=4,font=('font',12,'bold'),width=23,text="Exit",command=iExit)
        self.btnEt.grid(row=0,column=2,padx=3)


if __name__=='__main__':
    root= Tk()
    application= DataEntryForm(root)
    root.mainloop()