from tkinter import*
from tkinter import messagebox,filedialog
from email.message import EmailMessage
import smtplib
import pandas
import imghdr
import os
GUI=Tk()
GUI.title("Mail Sender App")
GUI.geometry('800x690')
GUI.config(bg="blue")
GUI.resizable(0,0)

check=False 
def Browse_CSV():
   global final_emails
   path=filedialog.askopenfilename(initialdir="c:/",title="Upload CSV File")
   if path=="":
        messagebox.showerror("Error","Please select a csv file")
   else:
        data=pandas.read_csv(path)
        if "ID"in data:
            emails=list(data["ID"])
            final_emails=[]
            for j in emails:
                if pandas.isnull(j)==False:
                    final_emails.append(j)
            if len(final_emails)==0:
                messagebox.showerror("Error","file doesnot contain any email address")
            else:
                AddressEntry.config(state=NORMAL)
                AddressEntry.insert(0,os.path.basename(path))
                AddressEntry.config(state="readonly")
                TotalLevel.config(text="Total "+str(len(final_emails)))
                SentLevel.config(text="Sent ")
                FailedLevel.config(text="Fail ")
                LeftLevel.config(text="Left ")

def Attachment():
    global filename,filetype,filepath,check
    check=True
    filepath=filedialog.askopenfilename(initialdir="c:/",title="Select File")
    filetype=filepath.split(".")
    filetype=filetype[1]
    filename=os.path.basename(filepath)
    TextArea.insert(END,f"\n{filename}]n")
                
def Check_button():
    if (Choice.get()=="Multiple"):
        B2.config(state=NORMAL)
        AddressEntry.config(state="readonly")

    if (Choice.get()=="Single"):
        B2.config(state=DISABLED)
        AddressEntry.config(state=NORMAL)
    
def SENDINGEMAIL(subject,toadress,body):
    file=open('credential.txt',"r")
    for i in file:
        Credential=(i.split(","))
    
    message=EmailMessage()
    message["subject"]=subject
    message["to"]=toadress
    message["from"]=Credential[0]
    message.set_content(body)
    
    if check:
        if filetype=="png" or filetype=="jpg" or filetype=="jpeg":
            f=open(filepath,"rb")
            file_data=f.read()
            subtype=imghdr.what(filepath)
            message.add_attachment(file_data,maintype="image",subtype=subtype,filename=filename)
             
        else:
            f=open(filepath,"rb")
            file_data=f.read()
            message.add_attachment(file_data,maintype="appplication",subtype="octet-stream",filename=filename)

   
        
    
    server=smtplib.SMTP("smtp.gmail.com",587)
    server.starttls()
    server.login(Credential[0],Credential[1])
    server.send_message(message)
    x=server.ehlo()
    if x[0]==250: 
        return "sent"
    else: 
        return "fail"
    
    
    messagebox.showinfo("Information", "Email is sent Succesfully")       
    
def SEND_EMAIL():
    if SubjectEntry.get()=="" or AddressEntry.get()=="" or TextArea.get(1.0,END)=="\n":
        messagebox.showerror("Error","All files are required",parent=GUI)
    else:
        if(Choice.get()=="Single"):
            result=SENDINGEMAIL(SubjectEntry.get(), AddressEntry.get(),TextArea.get(1.0,END))
            if result=="sent":
                messagebox.showinfo("Succesfull","Message has been sent succesfully")
            else:
                if result=="fail":
                    messagebox.showerror("Error","Message has been failed")
                    

        if(Choice.get()=="Multiple"):
            sent=0
            fail=0
            for a in final_emails:
                result=SENDINGEMAIL(SubjectEntry.get(),a,TextArea.get(1.0,END))
                if result=="sent":
                    sent+=1
                if result=="fail":
                    fail+=1
                TotalLevel.config(text="")
                SentLevel.config(text="Sent "+str(sent))
                FailedLevel.config(text="Fail "+str(fail))
                LeftLevel.config(text="Left "+str(len(final_emails)-(sent+fail)))

                TotalLevel.update()
                SentLevel.update()
                FailedLevel.update()
                LeftLevel.update()
                
        messagebox.showinfo("Succesfu ll","Message has been sent succesfully")
         
            
            
         
           


        
def EXIT():
    result=messagebox.askyesno("Do you want to Exit")
    if result:
        GUI.destroy()
    else:
        pass
    
def CLEAR():
    SubjectEntry.delete(0,END)
    AddressEntry.delete(0,END)
    TextArea.delete(1.0,END)


def LOGIN():
    def CLEAR1():
        SenderEntry.delete(0,END)
        PasswordEntry.delete(0,END)

    def SAVE1():
        if SenderEntry.get()=="" or PasswordEntry.get()=="":
            messagebox.showerror("Error","All fields are required",parent=GUI1)
        else:
            file=open("Credential.txt","w")
            file.write(SenderEntry.get()+","+PasswordEntry.get())
            file.close()
            messagebox.showinfo("Information","Credential Saved Succesfully",parent=GUI1)
        
    GUI1=Toplevel()
    GUI1.title("Login")
    GUI1.geometry("600x400")
    GUI1.resizable(0,0)
    GUI1.config(bg="blue")
    CL=Label(GUI1,text="Credential ",image=LogoImage,compound=LEFT,font=("Time New Roman",20,"bold"),bg="white",fg="black")
    CL.grid(row=0,column=0,padx=50)
    
    SenderLevelFrame=LabelFrame(GUI1,text="Sender Email", font=("Time New Roman",20,"bold"),bd=5,bg="deeppink",fg="blue")
    SenderLevelFrame.grid(row=1,column=0,padx=50,pady=5)
    SenderEntry=Entry(SenderLevelFrame, font=("Time New Roman",20,"bold"),width=30)
    SenderEntry.grid(row=0,column=0)

    PasswordLevelFrame=LabelFrame(GUI1,text="Passwordl", font=("Time New Roman",20,"bold"),bd=5,bg="deeppink",fg="blue")
    PasswordLevelFrame.grid(row=2,column=0,padx=50,pady=5)
    PasswordEntry=Entry(PasswordLevelFrame, font=("Time New Roman",20,"bold"),width=30,show=".")
    PasswordEntry.grid(row=0,column=0)

    BT1=Button(GUI1,text="Save",font=("Time New Roman",20, "bold"),cursor="hand2",bg="deeppink",fg="Black",command=SAVE1)
    BT1.place(x=180,y=350)

    BT2=Button(GUI1,text="Clear",font=("Time New Roman",20, "bold"),cursor="hand2",bg="deeppink",fg="Black",command=CLEAR1)
    BT2.place(x=320,y=350)
                  
    GUI1.mainloop()
        
        
            
TitleFrame=Frame(GUI,bg="white")
TitleFrame.grid(row=0,column=0,pady=2)

LogoImage=PhotoImage(file="email.png")
TitleLabel1=Label(TitleFrame,image=LogoImage,bg="white",bd=0)
TitleLabel1.grid(row=0,column=0)

TitleLabel2=Label(TitleFrame,text="Email Sender",font=("Time New Roman",30,"bold"),bg="white",fg="blue",padx=20)
TitleLabel2.grid(row=0,column=1)
LoginImage=PhotoImage(file="settingimage.png")

b1=Button(TitleFrame,image=LoginImage,bd=0,padx=20 ,command=LOGIN)
b1.grid(row=0,column=2)

ChoiceFrame=Frame(GUI,bg="deeppink",pady=5)
ChoiceFrame.grid(row=1,column=0)

Choice=StringVar()
Choice.set("Single")
Single_radio=Radiobutton(ChoiceFrame,text="Single",font=("Time New Roman",20,"bold"),
                         variable=Choice, value="Single",bg="deeppink",activebackground="deeppink",padx=20,command=Check_button)
Single_radio.grid(row=0,column=0)

Multiple_radio=Radiobutton(ChoiceFrame,text="Multiple",font=("Time New Roman",20,"bold"),
                           variable=Choice, value="Multiple",bg="deeppink",activebackground="deeppink",padx=20,command=Check_button)
Multiple_radio.grid(row=0,column=1)


AddressLevelFrame=LabelFrame(GUI,text="To(Email Address)", font=("Time New Roman",20,"bold"),bd=5,bg="deeppink",fg="black")
AddressLevelFrame.grid(row=2,column=0,padx=100,pady=5)
AddressEntry=Entry(AddressLevelFrame, font=("Time New Roman",20,"bold"),width=30)
AddressEntry.grid(row=0,column=0)

BrowseImage=PhotoImage(file="search.png")
B2=Button(AddressLevelFrame,image=BrowseImage,width=100,bd=0,bg="deeppink",
          activebackground="deeppink",state=DISABLED,command=Browse_CSV)
B2.grid(row=0,column=1)

SubjectLevelFrame=LabelFrame(GUI,text="Subject", font=("Time New Roman",20,"bold"),
                             bd=5,bg="deeppink",fg="black")
SubjectLevelFrame.grid(row=3,column=0,pady=5)
SubjectEntry=Entry(SubjectLevelFrame, font=("Time New Roman",20,"bold"),width=30)
SubjectEntry.grid(row=0,column=0)

EmailLevelFrame=LabelFrame(GUI,text="Compose Email", font=("Time New Roman",20,"bold"),
                             bd=5,bg="deeppink",fg="black")
EmailLevelFrame.grid(row=4,column=0,pady=10)


AttachmentImage=PhotoImage(file="attachment.png")
B4=Button(EmailLevelFrame,text="Attachment",image=AttachmentImage, compound=LEFT,font=("Time New Roman",20, "bold"),cursor="hand2",
          bd=0,bg="deeppink",activebackground="deeppink",command=Attachment)
B4.grid(row=0,column=0)

TextArea=Text(EmailLevelFrame,font=("Time New Roman",20,"bold"),height=6,width=50)
TextArea.grid(row=1,column=0,padx=20)

SendImage=PhotoImage(file=("send.png"))
B5=Button(GUI,image=SendImage,bd=0,bg="white", cursor="hand2",
           activebackground="white",command=SEND_EMAIL)
B5.place(x=500,y=620)

ClearImage=PhotoImage(file=("clear.png"))
B6=Button(GUI,image=ClearImage,bd=0,bg="white", cursor="hand2",
           activebackground="white",height=65,command=CLEAR)
B6.place(x=600,y=620)

ExitImage=PhotoImage(file=("exit.png"))
B7=Button(GUI,image=ExitImage,bd=0,bg="white", cursor="hand2",
           activebackground="white",height=65,command=EXIT)
B7.place(x=700,y=620)

TotalLevel=Label(GUI,font=("Time New Roman",20, "bold"), bg="blue",fg="black",)
TotalLevel.place(x=10,y=620)

SentLevel=Label(GUI,font=("Time New Roman",20, "bold"), bg="blue",fg="black",)
SentLevel.place(x=140,y=620)

LeftLevel=Label(GUI,font=("Time New Roman",20, "bold"), bg="blue",fg="black",)
LeftLevel.place(x=240,y=620)

FailedLevel=Label(GUI,font=("Time New Roman",20, "bold"), bg="blue",fg="black",)
FailedLevel.place(x=330,y=620)

GUI.mainloop()
