from abc import ABC, abstractmethod

class Bank:
    accounts = []
    def __init__(self,name, email, password, accountType) -> None:
        self.name=name
        self.email=email
        self.password=password
        self.accountType = accountType

     

class User(ABC,Bank):
        def __init__(self, name, email, password, accountType,userAccountNumber) -> None:
            super().__init__(name, email, password, accountType)
            self.userAccountNumber = userAccountNumber
            self.userBalance=0
            self.bankLoan = 0
            self.history=[]
            
            
            
            
            
            Bank.accounts.append(self)


        def __repr__(self) -> str:
            return f"{self.email},{self.accountType},{self.userBalance},{self.bankLoan},{self.name},{self.userAccountNumber}"
        
        def deposit(self, amount):
            
            if amount >=0 :
                self.history.append(("Deposit", amount))
                self.userBalance +=amount
                    
            else:
                print("\n Invalid Amount")
            

        def withdraw(self, amount):
            
            if amount >=0 and amount<=self.userBalance :
                self.history.append(("withdraw", amount))
                self.userBalance -=amount
                    
            else:
                print("\nWithdrawal amount exceeded")
            
    
        

        def transferAmount(self,amount, emailId,  sendUser):
            if sendUser.userBalance !=0:
                result = next((obj for obj in Bank.accounts if obj.email == emailId),None)
                if result :
                    sendUser.userBalance -=amount
                    result.userBalance = result.userBalance + amount
                    print("Money transfer: ",result.userBalance) 
                else:
                    print("Account does not exist")
            else:
                print("Your balance is 0, Deposit and try again!!")


            

        

        
        @abstractmethod
        def checkUserBalance(self):
            pass
        @abstractmethod
        def showInfo(self):
            pass
       
        

class SavingsAccount(User):

    def __init__(self, name, email, password, accountType, userAccountNumber, interestRate) -> None:
        super().__init__(name, email, password, accountType, userAccountNumber)
        self.interestRate = interestRate

    def checkUserBalance(self):
        print(f"\nBalance: {self.userBalance}")
        print("interest rate: ", self.interestRate)

    def applyInterest(self):
        interest = self.userBalance*(self.interestRate/100)
        print(f"\nApplied interest of {interest}")
        self.deposit(interest)

    def showInfo(self):
        print("\nName: ", self.name)
        print("Email: ", self.email)
        print(f"Account Number {self.userAccountNumber}")
        print(f"Account Type: {self.accountType}")
        print(f"Balance: {self.userBalance}")




class CurrentAccount(User):
    def __init__(self, name, email, password, accountType, userAccountNumber, loanLimit, loanTime) -> None:
        super().__init__(name, email, password, accountType, userAccountNumber)
        self.loanLimit = loanLimit
        self.loanTime = loanTime



    def checkUserBalance(self):
        print(f"\nBalance: {self.userBalance}")
        print(f"Loan limit: ", self.loanLimit)
        print(f"Loan Time: ", self.loanTime)

    def showInfo(self):
        print("\nName: ", self.name)
        print("Email: ", self.email)
        print(f"Account Number {self.userAccountNumber}")
        print(f"Account Type: {self.accountType}")
        print(f"Balance: {self.userBalance}")

    def takeLoan(self, amount):
        if self.loanTime > 0:
            if amount >=0 and amount<=self.loanLimit:
                self.history.append(("Loan", amount))
                self.userBalance +=amount
                self.bankLoan +=amount
                self.loanTime -=1
                print("Successfully loan!!")
            else:
                print("\n Invalid Amount")
        else:
            print("Your Loan time expired")




class Admin(Bank):
    def __init__(self, name, email, password, accountType, adminAccountNumber) -> None:
        super().__init__(name, email, password, accountType)
        self.accountType = accountType
        self.adminAccountNumber = adminAccountNumber

        Bank.accounts.append(self)
    
    def __repr__(self) -> str:
        return f"{self.email},{self.accountType},{self.name},{self.adminAccountNumber}"

    
    
        
    def deleteUserAnyAccount(self, emailId):
        flag = False
        if not Bank.accounts:
            print("There are no user account yet!!\n")
        else:
            for user in Bank.accounts:
                if emailId == str(user).split(",")[0] and str(user).split(",")[1]!="admin":
                    Bank.accounts.remove(user)
                    print("\nDeleted user: ", emailId)
                    flag = True
            if flag==False:
                print(emailId," is not exist")
        

    def checkAllUsersAccountList(self):
        print("\n Total User List: ")
        if len(Bank.accounts)==0:
            print("There are no user account yet!!\n")
        else:
            for user in Bank.accounts:
                if str(user).split(",")[1]!="admin":
                    print(user)
        
    def checkBankBalance(self):
        sumBank = 0
        print("Total Bank balance: ",end="")
        for user in Bank.accounts:
            if str(user).split(",")[1]!="admin":
                sumBank = sumBank + float(str(user).split(",")[2])
        print(sumBank)
        
    def checkBankLoan(self):
        sumLoan = 0
        print("Total Bank Loan: ", end="")
        for user in Bank.accounts:
            if str(user).split(",")[1]!="admin":
                sumLoan = sumLoan + float(str(user).split(",")[3])
        print(sumLoan)

    


loan_time=0
loan_limit=0
irate=0
cond= 1
currentUser = None
while True:
    if currentUser == None:
        print("No user Logged in!")
        ch = input("Register or Login? (R/L) : ")
        if ch=="R":
            name = input("Name: ")
            email = input("Email: ")
            password = input("Password: ")
            chUser = input("Admin or Savings or Current? (A/S/C) : ")
            if chUser == "A":
                currentUser = Admin(name, email, password, "admin",f"{name}_{email}")
                
            elif chUser=="S":
                
                currentUser = SavingsAccount(name, email, password, "savings",f"{name}_{email}",irate)
                
                
            elif chUser == "C":
                
                currentUser = CurrentAccount(name, email, password, "current", f"{name}_{email}", loan_limit, loan_time)
                
            else:
                print("Invalid choice, choose A or S or C")

        elif ch=="L":
            accnum = input("Account email: ")
            for acc in Bank.accounts:
                num = str(acc).split(",")[0]
                if accnum == num:
                    currentUser = acc
                    break
            if(currentUser==None):
                print("invalid user")
        else:
            print("Please choose R or L keyword!!")
        

    else:
        print(f"\n---------Welcome {currentUser.name}----------")
        if currentUser.accountType=="admin":
            print("1. See All User Accounts List")
            print("2. Delete Any User Account")
            print("3. Check the Total Balance of Bank")
            print("4. Check the Total Loan Amount")
            print("5. Interest Rate")
            print("6. Loan Limit")
            print("7. Loan Time")
            print("8. Bank ON/OFF")
            print("9.Logout\n")
            op = int(input("Choose Option: "))

            if op == 1:
                currentUser.checkAllUsersAccountList()
            elif op == 2:
                emailId = input("Email Id: ")
                currentUser.deleteUserAnyAccount(emailId)
            elif op == 3:
                currentUser.checkBankBalance()
            elif op == 4:
                currentUser.checkBankLoan()
            elif op==5:
                irate = int(input("Interest Rate: "))
                currentUser.interestRate = irate
            elif op==6:
                loan_limit = int(input("Loan limit: "))
                currentUser.loanLimit = loan_limit
            elif op==7:
                loan_time = int(input("Loan Time: "))
                currentUser.loanTime = loan_time
            elif op == 8:
                if cond == 1:
                    print("Bank is ON")
                else:
                    print("Bank is OFF")
                con = input("Type: ON/OFF : ")
                if con == "ON":
                    cond = 1
                else:
                    cond = 0
            
            elif op == 9:
                currentUser = None

        elif currentUser.accountType=="savings":
            print("1. Show info")
            print("2. Check Balance")
            print("3. Deposit")
            print("4. Withdraw")
            print("5. Apply Interest")
            print("6.Logout\n")
            if cond == 1:
                op = int(input("Choose Option: "))
                if op==1:
                    currentUser.showInfo()
                elif op==2:
                    currentUser.checkUserBalance()
                elif op==3:
                    amount = int(input("Amount: "))
                    currentUser.deposit(amount)
                elif op==4:
                    amount = int(input("Amount: "))
                    currentUser.withdraw(amount)
                elif op==5:
                    currentUser.applyInterest()
                elif op == 6:
                    currentUser = None
            elif cond==0:
                currentUser = None
                print("Bank is bankrupt!!\n")
        elif currentUser.accountType=="current":
            print("1. Show info")
            print("2. Check Balance")
            print("3. Deposit")
            print("4. Withdraw")
            print("5. Check Transaction History")
            print("6. Take Loan")
            print("7. Transfer the Amount")
            print("8. Logout\n")
            if cond == 1:
                op = int(input("Choose Option: "))

                if op==1:
                    currentUser.showInfo()
                elif op==2:
                    currentUser.checkUserBalance()
                elif op==3:
                    amount = int(input("Amount: "))
                    currentUser.deposit(amount)
                elif op==4:
                    amount = int(input("Amount: "))
                    currentUser.withdraw(amount)
                elif op==5:
                    if not currentUser.history:
                        print("Empty history")
                    else:
                        for hist in currentUser.history:
                            print(hist)
                elif op==6:
                    amount = int(input("Amount: "))
                    currentUser.takeLoan(amount)
                elif op==7:
                    amount = int(input("Amount: "))
                    emailId = input("Email: ")
                    currentUser.transferAmount(amount, emailId, currentUser)
                elif op == 8:
                    currentUser = None
            elif cond == 0:
                currentUser = None
                print("Bank is bankrupt!!\n")
