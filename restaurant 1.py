def restaurant():
    from datetime import datetime
    import random
    import csv
    import segno
    fh=open("restro.csv","a+")
    print("\t\t\t\t\t\t","="*32)
    print("\t\t\t\t\t\t WELCOME TO THE CS TRIPLET EATERY","\n")
    print("\t\t\t\t\t\t","="*32,"\n")
    name=input("enter your name:")
    dob = int(input("enter your birth date: "))
    while dob > 31 or dob < 1:
        dob=int(input("enter correct birth date:"))
    if dob==31:
        ob =int(input("enter your birth month in numerals: "))
        while ob==2 or ob==4 or ob==6 or ob==9 or ob==11 or ob>12 or ob<1:
            ob=int(input("enter your correct month in numerals: "))
    elif dob==30:
        ob =int(input("enter your birth month in numerals: "))
        while ob==2 or ob>12 or ob<1:
            ob=int(input("enter your correct month in numerals: "))
    else:
        ob =int(input("enter your birth month in numerals: "))
        while ob>12 or ob<1:
            ob =int(input("enter correct birth month in numerals: "))
    yob=int(input("enter your birth year: "))
    while len(str(yob))>4 or len(str(yob))<4 or yob>2018 or yob<1900:
        yob=int(input("enter correct birth year: "))
    date = [dob, ob, yob]
    bday = " {0}/{1}/{2}".format(date[0], date[1], date[2])
    print("Your birthday is on:",bday)
    mob=str(int(input("enter mobile number:")))
    while len(mob)>10 or len(mob)<10:
        mob=str(int(input("enter correct number:")))
    def menu():
        print("\t\t\t\t","_"*60)
        print("\t\t\t\t|\t\t\t   Here's the menu\t\t     |")
        print("\t\t\t\t|\tFast Food           |\t\tRegular              |")
        print("\t\t\t\t| 1.Pasta:         Rs 200   |\t11.Butter Paneer:      Rs300 |")
        print("\t\t\t\t| 2.Pizza:         Rs 250   |\t12.Mix Vegetable:      Rs150 |")
        print("\t\t\t\t| 3.Burger:        Rs 50    |\t13.Chilly Paneer:      Rs200 |")
        print("\t\t\t\t| 4.FriedRice:     Rs 180   |\t14.Channa Masala:      Rs155 |")
        print("\t\t\t\t| 5.Manchurian:    Rs 150   |\t15.Egg Curry:          Rs180 |")
        print("\t\t\t\t| 6.Sandwich:      Rs 40    |\t16.Butter Chicken:     Rs350 |")
        print("\t\t\t\t| 7.Momos:         Rs 30    |\t17.Dal Fry:            Rs120 |")
        print("\t\t\t\t| 8.Cold Coffee:   Rs 80    |\t18.Rice:               Rs60  |")
        print("\t\t\t\t| 9.VegRoll:       Rs 120   |\t19.Tawa Roti:          Rs 8  |")
        print("\t\t\t\t|10.FrenchFries:   Rs 40    |\t20.Tandoori Roti:      Rs12  |")
        print("\t\t\t\t|"+"_"*27+"|"+"_"*32+"|")
        print()
        print("="*131)
    menu()
    l=[]
    i=1
    g=0
    z=int(input("do you want to order?(1 for yes or 2 for no):"))
    while z>2 or z<1:
        z=int(input("enter correct value:"))
    if z==2:
        print("thanks for visiting")
    elif z==1:
        while i==1:
            ab=int(input("To order the item please enter no. listed before the item:"))
            while ab>20 or ab<1:
                ab=int(input("Enter valid number:"))
            if ab==1:
                print("You choose Pasta")
                a=int(input("Enter no. of quantity:"))
                b=("Pasta             ")
                c=200
                d=a*c
            elif ab==2:
                print("You choose Pizza")
                a=int(input("Enter no. of quantity:"))
                b=("Pizza             ")
                c=250
                d=a*c
            elif ab==3:
                print("You choose burger")
                a=int(input("Enter no. of quantity:"))
                b=("Burger            ")
                c=50
                d=a*c
            elif ab==4:
                print("You choose FriedRice")
                a=int(input("Enter no. of quantity:"))
                b=("FriedRice         ")
                c=180
                d=a*c
            elif ab==5:
                print ("You choose Manchurian")
                a=int (input ("Eenter no. of quantity:"))
                b=("Manchurian        ")
                c=150
                d=a*c
            elif ab==6:
                print ("You choose Sandwich")
                a=int(input ("Enter no. of quantity:"))
                b=("Sandwich          ")
                c=40
                d=a*c
            elif ab==7:
                print ("You choose Momos")
                a=int (input ("Enter no. of quantity:"))
                b=("Momos             ")
                c=30
                d=a*c
            elif ab==8:
                print ("You choose Shakes")
                a=int (input ("Enter no. of quantity:"))
                b=("Cold Coffee       ")
                c=80
                d=a*c
            elif ab==9:
                print ("You choose VegRoll")
                a=int (input ("Enter no. of quantity:"))
                b=("VegRoll           ")
                c=120
                d=a*c
            elif ab==10:
                print ("You choose FrenchFries")
                a=int (input ("Enter no. of quantity:"))
                b=("FrenchFries       ")
                c=40
                d=a*c
            elif ab==11:
                print ("You choose Butter Paneer")
                a=int (input ("Enter no. of quantity:"))
                b=("Butter Paneer     ")
                c=300
                d=a*c
            elif ab==12:
                print ("You choose Mix Vegetable")
                a=int (input ("Enter no. of quantity:"))
                b=("Mix Vegetable     ")
                c=150
                d=a*c
            elif ab==13:
                print ("You choose Chilli Paneer")
                a=int (input ("Enter no. of quantity:"))
                b=("Chilli Paneer     ")
                c=200
                d=a*c
            elif ab==14:
                print ("You choose Chana Masala")
                a=int (input ("Enter no. of quantity:"))
                b=("Chana Masala      ")
                c=155
                d=a*c
            elif ab==15:
                print ("You choose Egg Curry")
                a=int (input ("Enter no. of quantity:"))
                b=("Egg Curry         ")
                c=180
                d=a*c
            elif ab==16:
                print ("You choose Butter Chicken")
                a=int (input ("Enter no. of quantity:"))
                b=("Butter Chicken    ")
                c=350
                d=a*c
            elif ab==17:
                print ("You choose Dal Fry")
                a=int (input ("Enter no. of quantity:"))
                b=("Dal Fry           ")
                c=120
                d=a*c
            elif ab==18:
                print ("You choose Rice")
                a=int (input ("Enter no. of quantity:"))
                b=("Rice              ")
                c=60
                d=a*c
            elif ab==19:
                print ("You choose Tawa Roti")
                a=int (input ("Enter no. of quantity:"))
                b=("Tawa Roti         ")
                c=8
                d=a*c
            elif ab==20:
                print ("You choose Tandoori Roti")
                a=int (input ("Enter no. of quantity:"))
                b=("Tandoori Roti     ")
                c=12
                d=a*c
            e=b+" "+"x"+" "+str(a)+" "+"="+" "+"Rs"+" "+str(d)
            g=g+d
            l.append(e)
            print("\n","YOUR ORDER IS:",*l,sep="\n")
            print()
            ad=int(input("If you want to order more press 1 if not press 2:" ))
            while ad>2 or ad<1:
                ad=int(input("Enter correct input:" ))
            if ad==1:
                menu()
                i=1
            if ad==2:
                print("_______________________________")
                print("YOUR ORDER IS:",*l,sep="\n")
                print("_______________________________")
                ac=int(input("To confirm your order press 1 or 2 to change your order press 3 to add more items:"))
                while ac>3 or ac<1:
                    print("Enter correct value:")
                if ac==1:
                    abc=int(input("press 1 for eating here and 2 for packing :"))
                    while abc>2 or abc<1:
                        abc=int(input("enter correct value:"))
                    if abc==1:
                        write=csv.writer(fh)
                        write.writerow(['Name','DOB','Mobile Number','Order'])
                        date_now = datetime.now().strftime("%d/%m/%y")
                        date=datetime.now().strftime("%d")
                        month=datetime.now().strftime("%m")
                        if dob==int(date) and ob==int(month):
                            orderno=random.randint(1,999)
                            seat=random.randint(1000,9999)
                            time_now = datetime.now().strftime("%H:%M:%S")
                            print("___________________________________")
                            print("              Receipt")
                            print("\n","Your order is confirmed")
                            print("Name:",name)
                            print("Mobile number:",mob)
                            print("Date and Time:",date_now,time_now)
                            print("Happy Birthday",name)
                            print("your order number is:",orderno)
                            print("your seat number is: ",seat,"\n")
                            print("YOUR ORDER IS:",*l,sep="\n")
                            print("birthday discount:               20% ")
                            print("YOUR BILL IS:            Rs",g)
                            print("YOUR FINAL BILL IS:       Rs",g-20*g/100)
                            print()
                            print("Thank You")
                            print("___________________________________")
                            print("choose your payment method:")
                            print("1.cash")
                            print("2.credit card/debit card")
                            print("3.UPI")
                            pay=int(input("enter payment method:"))
                            while pay>3 or pay<1 :
                                pay=int(input("enter correct input"))
                            if pay==3:
                                print("you choose UPI")
                                print("make a payment of Rs",g,"to given qr code")
                                bill='upi://pay?pa=8923548975@fam&pn=CS TRIPLET EATERY&am=',g,'&cu=INR'
                                qrcode = segno.make_qr(bill)
                                qrcode.show( scale=10)
                            elif pay==2:
                                print("You choose credit card/debit card")
                                print("Please make your paymnet at the reception")
                            elif pay==1:
                                print("You choose Cash")
                                print("Please make your paymnet at the reception")
                            rec=[name,bday,mob,*l]
                            write.writerow(rec)
                            fh.close()
                        else:
                            orderno=random.randint(1,999)
                            seat=random.randint(1000,9999)
                            time_now = datetime.now().strftime("%H:%M:%S")
                            date_now = datetime.now().strftime("%d/%m/%y")
                            print("___________________________________")
                            print("              Receipt")
                            print("\n","Your order is confirmed")
                            print("Name:",name)
                            print("Mobile number:",mob)
                            print("Date and Time:",date_now,time_now)
                            print("your order number is:",orderno,"\n")
                            print("your seat number is: ",seat,"\n")
                            print("YOUR ORDER IS:",*l,sep="\n")
                            print("YOUR BILL IS:            Rs",g)
                            print()
                            print("Thank You")
                            print("___________________________________")
                            print("1.cash")
                            print("2.credit card/debit card")
                            print("3.UPI")
                            pay=int(input("enter payment method:"))
                            while pay>3 or pay<1 :
                                pay=int(input("enter correct input"))
                            if pay==3:
                                print("you choose UPI")
                                print("make a payment of Rs",g,"to given qr code")
                                bill='upi://pay?pa=8923548975@fam&pn=CS TRIPLET EATERY&am=',g,'&cu=INR'
                                qrcode = segno.make_qr(bill)
                                qrcode.show( scale=10)
                            elif pay==2:
                                print("You choose credit card/debit card")
                                print("Please make your paymnet at the reception")
                            elif pay==1:
                                print("You choose Cash")
                                print("Please make your paymnet at the reception")
                            rec=[name,bday,mob,*l]
                            write.writerow(rec)
                            fh.close()
                    elif abc==2:
                        write=csv.writer(fh)
                        write.writerow(['Name','DOB','Mobile Number','Order'])
                        date_now = datetime.now().strftime("%d/%m/%y")
                        date=datetime.now().strftime("%d")
                        month=datetime.now().strftime("%m")
                        if dob==int(date) and ob==int(month):
                            orderno=random.randint(1,999)
                            time_now = datetime.now().strftime("%H:%M:%S")
                            print("___________________________________")
                            print("              Receipt")
                            print("\n","Your order is confirmed")
                            print("Name:",name)
                            print("Mobile number:",mob)
                            print("Date and Time:",date_now,time_now)
                            print("Happy Birthday",name)
                            print("your order number is:",orderno,"\n")
                            print("YOUR ORDER IS:",*l,sep="\n")
                            print("birthday discount:               20% ")
                            print("YOUR BILL IS:            Rs",g)
                            print("YOUR FINAL BILL IS:       Rs",g-20*g/100)
                            print()
                            print("Thank You")
                            print("___________________________________")
                            print("1.cash")
                            print("2.credit card/debit card")
                            print("3.UPI")
                            pay=int(input("enter payment method:"))
                            while pay>3 or pay<1 :
                                pay=int(input("enter correct input"))
                            if pay==3:
                                print("you choose UPI")
                                print("make a payment of Rs",g,"to given qr code")
                                bill='upi://pay?pa=8923548975@fam&pn=CS TRIPLET EATERY&am=',g,'&cu=INR'
                                qrcode = segno.make_qr(bill)
                                qrcode.show( scale=10)
                            elif pay==2:
                                print("You choose credit card/debit card")
                                print("Please make your paymnet at the reception")
                            elif pay==1:
                                print("You choose Cash")
                                print("Please make your paymnet at the reception")
                            rec=[name,bday,mob,*l]
                            write.writerow(rec)
                            fh.close()
                        else:
                            date_now = datetime.now().strftime("%d/%m/%y")
                            orderno=random.randint(1,999)
                            time_now = datetime.now().strftime("%H:%M:%S")
                            print("___________________________________")
                            print("              Receipt")
                            print("\n","Your order is confirmed")
                            print("Name:",name)
                            print("Mobile number:",mob)
                            print("Date and Time:",date_now,time_now)
                            print("your order number is:",orderno,"\n")
                            print("YOUR ORDER IS:",*l,sep="\n")
                            print("YOUR BILL IS:            Rs",g)
                            print()
                            print("Thank You")
                            print("___________________________________")
                            print("1.cash")
                            print("2.credit card/debit card")
                            print("3.UPI")
                            pay=int(input("enter payment method:"))
                            while pay>3 or pay<1 :
                                pay=int(input("enter correct input"))
                            if pay==3:
                                print("you choose UPI")
                                print("make a payment of Rs",g,"to given qr code")
                                bill='upi://pay?pa=8923548975@fam&pn=CS TRIPLET EATERY&am=',g,'&cu=INR'
                                qrcode = segno.make_qr(bill)
                                qrcode.show( scale=10)
                            elif pay==2:
                                print("You choose credit card/debit card")
                                print("Please make your paymnet at the reception")
                            elif pay==1:
                                print("You choose Cash")
                                print("Please make your paymnet at the reception")
                            rec=[name,bday,mob,*l]
                            write.writerow(rec)
                            fh.close()
                    i=0
                elif ac==2:
                    print()
                    l.clear()
                    g=0
                    i=1
                elif ac==3:
                    print()
                    i=1
    input()
restaurant()
