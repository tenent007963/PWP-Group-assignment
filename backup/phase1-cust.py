# Miyoko Pang Zi Xuan / Tai Eason
# TP067553 / TP060486

# Default return status code:
# 0: Task failed, 1: Task completed, 2: Return to menu, 3: Not ready

import os

# Main UI, for guest access (not logged in)
def mainui():
    u = 'guest'
    print('Home Page:')
    print('1. View all items\n')
    print('2. Login to system\n')
    print('3. Register as customer\n')
    print('0. Exit\n')
    opt = int(input('Please enter option:'))
    fnsorter(u, opt, u)

# Admin UI, restricted to admin only
# require username as variable
def adminui(usr):
    role = 'admin'
    print('Welcome ', usr, ' to Admin UI:')
    print('1. Add new Category\n')
    print('2. Manage Category\n')
    print('3. Add/Modify Item\n')
    print('4. Display all item details\n')
    print('5. Search customer order\n')
    print('6. Search customer payment history\n')
    print('7. Add/Modify/Delete Delivery Staffs\n')
    print('8. Search Delivery Staff\n')
    print('9. Assign order to Delivery Staff\n')
    print('0. Logout\n')
    opt = int(input('Please enter your choice:'))
    fnsorter(usr, opt, role)

# Delivery Staff / Man UI, for internal staff only 
# require username as variable
def staffui(usr):
    role = 'staff'
    print('Welcome ', usr, ' to Staff Index:')
    print('1. View/Select Order for Delivery\n')
    print('2. Update Delivery status\n')
    print('3. Take feedback on delivery\n')
    print('0. Logout\n')
    opt = int(input('Please enter your task:'))
    fnsorter(usr, opt, role)

# Customer Page, for customer only
# require username as variable
def custui(usr):
    role = 'cust'
    print('Welcome ', usr, ' to Customer Home Page:')
    print('1. View category details\n')
    print('2. View all items\n')
    print('3. View items by category\n')
    print('4. Place order\n')
    print('5. Make payment\n')
    print('0. Logout\n')
    opt = int(input('Please enter the menu index:'))
    fnsorter(usr, opt, role)

# Tiering function
# To determine the logged in user's role(admin/staff)
# Return to main UI if tier not defined/unclear
def tiering(r, n):
    if r == 'admin':
        adminui(n)
    if r == 'staff':
        staffui(n)
    print('No tier specified. Returning to main page.\n')
    mainui()

# Login Page
# Check role and pass to login
# opt value: 1 for customers, 2 for internal staffs   
def login(opt):
    print('AOSM Login Checkpoint\n')
    if opt == 1 :
        udb = 'customers.txt'
    elif opt == 2 :
        udb = 'users.txt'
    else:
        print('No role defined. Returning to Main UI')
        return 0
    uName = dettol(input('Please enter your username:\n'))
    print('Checking database... Please Wait...\n')
    try:
        uid = getcolumn(udb, 0).index(uName)
        udt = getrow(udb, uid)
        uPwd = dettol(input('Please enter your password:\n'))
    except:
        print('Invalid username. Please check your input and try again later.\n')
        return 0
    if (uid != '') and (uPwd != ''):
        if uPwd == udt[1]:
            try: 
                tiering(udt[8], uName)
            except:
                custui(uName)
        else:
            print('Invalid username or password. Please check your input and try again later.\nReturning to Main UI\n')
            return 0
    else:
        print('Empty input. Returning to Main UI.\n')
        return 0

# Login function handler, must be called instead of direct login() usage
# To return user to mainUI in the event of failed login
# x value: to be passed into login() for role pre-identifying
def loginhandler():
    x = input('Press 1 for customer, press 2 for staff:\n')
    try:
        x = int(x)
    except:
        print('Invalid input. Please try again')
        loginhandler()
    if login(x) == 0:
        mainui()

# Register Page for customer
def custreg():
    baseStr = 'Please enter your '
    print('Join now as our customer to enjoy more benefits!\n')
    regname = input('Please enter your desired username:\n')
    while regname:
        print('Please wait while we check the username availability...\n')
        try:
            getcolumn('customers.txt', 0).index(regname)
            print('Username already exist! Please proceed to login. Returning to Main UI now.')
            return 0
        except ValueError:
            print('Username available. Please proceed for next step.')        
        pwd = baseStr + 'preferred password:'
        email = baseStr + 'email address:'
        fname = baseStr + 'full name:'
        phone = baseStr + 'phone number in international format, eg +60123456789:'
        addr = baseStr + 'delivery address:'
        gender = baseStr + 'biological gender (M/F):'
        plh = '0'
        bStr = [regname, pwd, email, fname, phone, addr, gender, plh]    #username;password;fullname;phone number;address;email;gender;placeholder.
        details = theMagic(bStr)
        if (e := writeto('customers.txt', details)) == 1:
            print('User "', regname, '" has successfully created!\n')
            custui(regname)
        else:
            print('User unable to create.', e)
            print("Please check if special symbols exists or the database file has been modified. Returning to Main UI.\n")
            return 0
    print("No input has been entered. Returning to Main UI\n")
    return 0

# Customer register handler
# Return to main UI on 0 result code
def custreghandler():
    if custreg() == 0:
        mainui()

# Staff Management sub-menu
# Would you like to have a cup of coffee before hiring/firing someone?
def delmanSubMenu():
    staffname = input('Please enter username of the staff/delivery man:\n')
    while staffname:
        print('Checking in staff database...\n')
        try:
            uid = getcolumn('users.txt', 0).index(staffname)
        except ValueError:
            print('Username not found! Please make sure you entered the correct username, username are capital sensitive.\n')
            d = int(input('Do you want to create a new user or retry input username?\n1. Create new user\n2. Retry username\3. Return to Admin UI\n'))
            if d == 1:
                delmanNew(staffname)
            elif d == 2:
                delmanSubMenu()
            elif d == 3:
                return 2
            else:
                print('No input detected. Returning to Admin UI')
                return 0
    if uid:
        print('User ', staffname, ' found. Do you want to modify or delete record?\n')
        c = int(input("1. Modify\n2. Delete\n3. Back to Admin Menu\n"))
        if c == 1:
            delmanManage(uid, staffname)
            return 1
        elif c == 2:
            delmanByebye(uid, staffname)
            return 1
        elif c == 3:
            return 2
        else:
            print('No input detected. Returning to Admin UI')
            return 0
    return 2
    
# Add staff user by Admin
def delmanNew(x):
    print('Creating new user with username "', x, '".')
    baseStr = 'Please enter the '
    pwd = baseStr + 'preferred password:'
    email = baseStr + 'email address:'
    fname = baseStr + 'full name:'
    phone = baseStr + 'phone number in international format, eg +60123456789:'
    addr = baseStr + 'delivery address:'
    role = baseStr + 'role for user(admin/staff):'
    plh = '0'
    bStr = [x, pwd, fname, phone, addr, email, plh, plh, role] #username;password;fullname;phone number;address;email;placeholder;placeholder;role.
    details = theMagic(bStr)
    if (e := writeto('users.txt', details)) is True:
        print('User "', x, '"has successfully created!')
        return 1
    else:
        print('User unable to create.', e)
        print("Please check if special symbols exists or the database file has been modified. Returning to Main UI.")
        return 0

# Modify staff user by Admin
def delmanManage(x, y):
    print('Editing data of "',y,'".')
    dt = getrow('users.txt', x)
    u = input('Current username: ', dt[0], ', Enter new username:') or dt[0]
    p = input('Current password: ', dt[1], ', Enter new password:') or dt[1]
    f = input('Current name: ', dt[2], ', Enter new name:') or dt[2]
    n = input('Current phone number: ', dt[3], ', Enter new phone number:') or dt[3]
    a = input('Current address: ', dt[4], ', Enter new address:') or dt[4]
    e = input('Current email: ', dt[5], ', Enter new email:') or dt[5] 
    r = input('Current role: ', dt[8], ', Enter new role(admin/staff):') or dt[8]
    lst = [u,p,f,n,a,e,'0','0',r,"\n"]
    confirm = input('Are you sure you want to update entry of "', y, '"?(Y/n)\n')
    if confirm == 'Y':
        try:
            updaterow('users.txt', x, lst)
            print('User "', y,'" has been successfully modified with new details.')
            return 1
        except:
            print("An error occurred, please try again later, or check your permission settings.")
            return 0
    else:
        print('Action aborted due to incorrect confirmation. Returning to Admin UI.')
        return 0

# Delete staff user by Admin
def delmanByebye(x, y):
    confirm = input('Are you sure you want to delete "', y, '"?(Y/n)\n')
    if confirm == 'Y':
        try:
            with open('users.txt', 'r') as file:
                lines = file.readlines()
                ln = 0
                with open('users.txt', 'w') as f:
                    for line in lines:
                        if ln != x:
                            f.write(line)
                        ln += 1
            print('User "', y,'" has been successfully deleted.')
            return 1
        except:
            print("An error occurred, please try again later, or check your permission settings.")
            return 0
    else: 
        print('Action aborted due to incorrect confirmation. Returning to Admin UI.')
        return 0

# Search Delivery Man by Admin
def delmanSearch():
    query = input('Please enter the username of delivery staff to start search, query must be at least 4 characters:')
    while len(query)>=4:
        try:
            uid = getcolumn('users.txt', 0).index(query)
            info = getrow('users.txt', uid)
            print('Details of user:', query)
            print('Full Name:', info[2])
            print('Phone Number:', info[3])
            print('Address:', info[4])
            print('Email address:', info[5])
            print("User's: role:", info[8])
            print('Search complete. Returning to Admin UI.')
            return 1
        except ValueError:
            print('Username not found! Please make sure you entered the correct username, username are capital sensitive.\n')
            return 0
    print('Queried username is too short! Please input query keyword with more than 4 characters. Returning to Admin UI.')
    return 0

# Assign Delivery Man to order(s) by Admin
def delmanAssign():
    odb = 'orders.txt'
    udb = 'users.txt'
    print('Assigning staff to order(s)...')
    order = int(input('Please enter the Order ID to be assigned:'))
    delman = input('Please enter the username of staff to be assigned to the order ', order, ':')
    odt = getcolumn(odb, 0)
    udt = getcolumn(udb, 0)
    try:
        oid = odt.index(order)
        if oid & udt.index(delman):
            confirm = input('Confirm assigning ', order, 'to ', delman,'?\n')
            if confirm == 'Y':
                dt = getrow(odb, oid)
                dt[9] = delman
                updaterow(odb, oid, dt)
                print('Update successful. Returning to Admin UI.')
                return 1
            else:
                print('No valid confirmation. Returning to Admin UI')
                return 0
        else:
            print('Cannot find the order ID or staff username. Please ensure both inputs are correct.\nReturning to Admin UI')
            return 0
    except:
        print('Something went wrong. Please try again later.\nReturning to Admin UI')
        return 0

# Add new category function by Admin
# Will check against existing data before creation
def addCat():
    cfile = 'category.txt'
    newCat = input('Please enter new category name:')
    try:
        catID = [cat.lower() for cat in getcolumn(cfile, 1)].index(newCat.lower())
        print('Category "', newCat, '" already exist with Category ID "', catID, '", please use the existing category.\n Returning to Admin UI.')
        return 0
    except ValueError:
        print('Category name available, please proceed to enter details for new category.')
    catDes = input('Enter description for new category (Not more than 50 words):')
    newcatID = int(getcolumn(cfile, 0)[-1]) + 1
    plh = 0
    catList = [newcatID, newCat, catDes, plh] #categoryID;category name;description;placeholder.
    if (e := writeto(cfile, catList)) is True:
        print('Category "', newCat, '"has successfully created!\nCategory ID:', newcatID)
        return 1
    else:
        print('Category unable to create.', e)
        print("Please check if special symbols exists or the database file has been modified. Returning to Main UI.")
        return 0

# Modify category function by Admin
def modCat():
    cfile = 'category.txt'
    catname = input('Please enter category name:')
    print('Please wait while system is retrieving data...')
    while catname:
        try:
            cid = getcolumn(cfile, 1).index(catname)
        except ValueError:
            print('Category not found! Make sure you have entered the exact same name of the category.\nReturning to Admin UI.')
            return 0
    try:
        dt = getrow(cfile, cid)
    except:
        print('An error occurred when trying to retrieve data. Please try again later.\nReturning to Admin UI')
        return 0
    n = input('Current category name: ', dt[1], ', Enter new category name:') or dt[1]
    d = input('Current category description: ', dt[2], ', Enter new category description:') or dt[2]
    lst = [cid,n,d,0,"\n"]
    confirm = input('Are you sure you want to update entry of "', catname, '"?(Y/n)\n')
    if confirm == 'Y':
        try:
            updaterow(cfile, cid, lst)
            print('Category "', n,'" has been successfully modified with new data.')
            return 1
        except:
            print("An error occurred, please try again later, or check your permission settings.")
            return 0
    else:
        print('Action aborted due to incorrect confirmation. Returning to Admin UI.')
        return 2

# Add new product function by Admin
# Will be given selection of existing categories
def addItem():
    pfile = 'products.txt'
    cfile = 'category.txt'
    newItem = input('Please enter new item name:')
    try:
        productID = [i.lower() for i in getcolumn(pfile, 1)].index(newItem.lower())
        print('Product "', newItem, '" already exist with Category ID "', productID, '", please choose other name or use the existing entry.\n Returning to Admin UI.')
        return 0
    except ValueError:
        print('Product name available. Please proceed to choose the relevant category from list below.')
    catName = getcolumn(cfile, 1)
    catID = getcolumn(cfile, 0)
    i = 1
    for namae in catName:
        print(int(catID[i]), '. ', namae)
        i += 1
    selCat = int(input('Please select the category of the new item:'))
    itemDes = input('Enter description for new item (Not more than 100 words):')
    itemStk = int(input('Enter available stock for item:'))
    itemRM = int(input('Enter retail price for item:'))
    newitemID = int(getcolumn(pfile, 0)[-1]) + 1
    itemList = [newitemID, newItem, itemDes, itemStk, 0, itemRM, selCat] #productID;product title;product description;stock quantity;sold quantity;retail price;categoryID.
    if (e := writeto(pfile, itemList)) is True:
        print('New product "', newItem, '"has successfully created!\nCategory ID:', newitemID)
        return 1
    else:
        print('Product unable to create.', e)
        print("Please check if special symbols exists or the database file has been modified. Returning to Admin UI.")
        return 0

# Modify item details function by Admin
def modItem():
    pfile = 'products.txt'
    itemname = input('Please enter item name:')
    print('Please wait while system is retrieving data...')
    while itemname:
        try:
            iid = getcolumn(pfile, 1).index(itemname)
        except ValueError:
            print('Item not found! Make sure you have entered the exact same name of the product.\nReturning to Admin UI.')
            return 0
    try:
        dt = getrow(pfile, iid)
    except:
        print('An error occurred when trying to retrieve data. Please try again later.\nReturning to Admin UI')
        return 0
    n = input('Current product name: ', dt[1], ', Enter new product name:') or dt[1]
    d = input('Current product description: ', dt[2], ', Enter new product description:') or dt[2]
    s = input('Current product stock: ', dt[3], ', Enter new stock quantity:') or dt[3]
    p = input('Current product retail price: ', dt[5], ', Enter new retail price:') or dt[5]
    c = input('Current product category: ', dt[6], ', Enter new product category:') or dt[6]
    lst = [iid,n,d,s,dt[4],p,c,"\n"]
    confirm = input('Are you sure you want to update entry of "', itemname, '"?(Y/n)\n')
    if confirm == 'Y':
        try:
            updaterow(pfile, iid, lst)
            print('Product "', n,'" has been successfully modified with new data.')
            return 1
        except:
            print("An error occurred, please try again later, or check your permission settings.")
            return 0
    else:
        print('Action aborted due to incorrect confirmation. Returning to Admin UI.')
        return 2

# Diplay all record of category function
def listCat():
    cfile = 'category.txt'
    print('Listing all the available categories:')
    try:
        clist = getcolumn(cfile, 0)
        for cid in clist:
            dt = getrow(cfile, (int(cid)-1))
            print('Category ID: ', cid)
            print('Category name: ', dt[1])
            print('Category description: ', dt[2])
        print('Successfully retrieved all data for ', cfile, '.\n')
        return 1    
    except:
        print("An error occurred, please try again later, or check the files integrity.")
        return 0

# Display products based on category function
def listItembyCat():
    pfile = 'products.txt'
    try:
        listCat()
    except:
        return 0
    catChoice = input('Please enter the choice of category using its Category ID:')
    tmplist = getcolumn(pfile,6)
    i = 0
    iList = []
    for item in tmplist:
        if item == catChoice:
            iList.append(i)
        i += 1   
    try: 
        print('Products under category ', catChoice)
        for index in iList:
            dt = getrow(pfile, index)
            print('Product ID: ', dt[0]) 
            print('Product name: ', dt[1])
            print('Product description: ', dt[2])
            print('Product stock quantity: ', dt[3])
            print('Product sold quantity: ', dt[4])
            print('Product retail price: ', dt[5])
        print('End of database. Returning to Admin UI')
        return 1
    except:
        print('An error occurred. Please check file permission or restart the program. Returning to Admin UI')
        return 0

# Display all items
def listallItem():
    pfile = 'products.txt'
    print('Listing all the available products:')
    try:
        plist = getcolumn(pfile, 0)
        for pid in plist:
            dt = getrow(pfile, (int(pid)-1))
            print('Product ID: ', dt[0]) 
            print('Product name: ', dt[1])
            print('Product description: ', dt[2])
            print('Product stock quantity: ', dt[3])
            print('Product sold quantity: ', dt[4])
            print('Product retail price: ', dt[5])
        print('Successfully retrieved all data for', pfile, '.\n')
        return 1    
    except:
        print("An error occurred, please try again later, or check the files integrity.")
        return 0
    #list all item

# Item sub menu by Admin
# send user to correct item function
def itemSubMenu(u):
    opt = int(input('Press 1 to add new item, press 2 to modify item:'))
    if opt == 1:
        addItem()
        adminui(u)
    elif opt == 2:
        modItem()
        adminui(u)
    else:
        print('An case error occurred. Please try again later. Returning to Admin UI')
        adminui(u)
    adminui(u)

# Place order function by Customer
# Takes in usr, item lists, cart total, for use of helper function 
def placeOrder(u, items = [], trm = 0):
    listallItem()
    pdb = 'products.txt'
    sel = input('Select your item using product ID:')
    try:
        pdt = getrow(pdb, (int(sel) -1) )
        if pdt:
            qtt = input('Please enter order quantity for this product:')
            if int(qtt) <= int(pdt[3]):
                rm = round(float(pdt[5]) * int(qtt), 2)
                print('Item total will be RM', rm)
                addtoCart(u, sel, qtt, rm, items, trm)
                return 1
            else:
                print('Quantity cannot be more than available stock! Return to customer page.')
                return 0
    except:
        print('An error occurred. Please make you have entered correct input. Returning to Customer page.')
        return 0

# Add to cart/checkout helper function for placeOrder() by Customer
# Takes in usr, pid, quantity, item total, item lists, cart total, option and compile it write into file
def addtoCart(usr, pid, qtt, rm, items, trm, opt = 0):
    odb = 'orders.txt'
    tlst = [pid, qtt]
    try:
        opt = int(input('Do you want to checkout now or continue shopping?\n1. Continue\n2. Checkout\n3. Discard cart\n')) if opt == 0 else opt
        if opt == 1:
            lst = items.append(tlst)
            ttl = int(trm) + int(rm)
            placeOrder(usr, lst, ttl)
        elif opt == 2:
            oid = int(getcolumn(odb, 0)[-1]) + 1
            odt = gettime()
            po = items.append(tlst)
            tpp = int(rm) + int(trm)
            des = 00
            cid = ded = rat = deu = plh = 0
            lst = [oid, odt, po, cid, usr, tpp, des, ded, rat, deu, plh]
            writeto(odb, lst)
            print('Order created. Your order number is:', oid)
            return 1
        elif opt == 3:
            confirm = input('Are you sure to discard cart? Once done no revert can be done(Y/n)):')
            if confirm == "Y":
                print('Discarding cart. Will return to customer home page')
                return 2
            else:
                print('Invalid confirmation, will return back to order page without new item added.')
                placeOrder(usr, items, trm)
        else:
            print('No valid options. Returning to order page with existing cart items.')
            placeOrder(usr, items, trm)
    except:
        print('An error occurred, Please try again later. Saving current cart as unpaid order.')
        addtoCart(usr, 0, 0, 0, items, trm, 2)

# Make payment function by Customer
# Takes in only usr to search for unpaid order, return 2 if no order found
def makePayment(u):
    pdb = 'payments.txt'
    odb = 'orders.txt'
    tlist = []
    print('Searching for unpaid order for user ',u ,'...')
    try:
        dt = getcolumn(odb, 3)    #paymentID
        dt1 = getcolumn(odb, 4)   #cust username
        c = 0
        for i in dt:
            if (i == '0') & (dt1[c] == u):
                tlist.append(c)
                c += 1
            else:
                c += 1
                continue
        for t in tlist:
            displayOrder(getrow(odb, t))
        opt = input('Please enter orderID to select order and pay:')
        if opt:
            dt2 = getrow(odb, opt)
            tpc = input('Please enter your TPCard number:')
            confirm = input('Amount ', dt2[5], 'will be charged from card ', tpc, '.\nPlease confirm (Y/n):')
            if (len(tpc) == 8) & (confirm == 'Y'):
                pid = int(getcolumn(pdb, 0)[-1]) + 1
                pmd = 'tpcard:' + tpc 
                pmt = dt2[5]
                cc = hash(tpc+pmt)
                pdt = gettime()
                plh = 0
                lst = [pid,pmd,pmt,cc,pdt,plh]
                writeto(pdb, lst)
                print('Payment successful! Returning to home page.')
                return 1
    except:
        print('Error occurred. Please try again later.')
        return 0

# List out all assigned delivery order by Staff
# Takes in only usr to get assigned orders, return 2 if no order found
def listallDelOrder(u):
    odb = 'orders.txt'
    lst = []
    c = 0
    print('Fetching list of delivery order for ', u, ':')
    try:
        ols = getcolumn(odb, 9)
        for i in ols:
            if i == u:
                lst.append(c)
                c += 1
            else:
                c += 1
                continue
        if len(lst) > 0:
            for o in lst:
                dt = getrow(odb, o)
                print('Order ID: ', dt[0])
                print('Order delivery status: ', dt[6])
                print('Order delivered date: ', dt[7])
                print('Order feedback: ', dt[8])
                print('Staff in charger: ', dt[9])
        else:
            print('No order found. Returning to Staff UI.')
            return 2
        print('Delivery order query completed. Returning to Staff UI.')
        return 1
    except:
        print('An error occurred, please try again later. Returning to Staff UI.')
        return 0

# Update order delivery status by Staff
# 10: pending, 11: delivering, 12: completed(need datetime())
def orderUpdate(u):
    odb = 'orders.txt'
    listallDelOrder(u)
    query = input('Please input the order ID to update:')
    if query:
        try:
            dt = getrow(odb, query)
        except:
            print('Order not found, please check your input. Returning to Staff UI.')
            return 0
    else:
        print('No input detected. Returning to Staff UI')
        return 2
    if dt[7] != '0':
        print('Order already completed, no further update required. Returning to Staff UI')
        return 2
    action = int(input('Please enter the current status for the order:\n1. pending\n2. delivering\n3. completed'))
    if action == 1:
        dt[6] = '10'
    elif action == 2:
        dt[6] = '11'
    elif action == 3:
        dt[6] = '12'
        dt[7] = gettime()
    try:
        updaterow(odb, query, dt)
        print('Order ', query, 'successfully updated. Returning to Staff UI')
        return 1
    except:
        print('An error occurred, please try again later. Returning to Staff UI.')
        return 0    

# Update order feedback by Staff
# Any staff is agent to give feedback on orders: when original PIC is gone, other agent can take over
def orderFeedback():
    odb = 'orders.txt'
    oid = int(input('Please input the order ID to give feedback:'))
    if oid:
        try:
            dt = getrow(odb, oid)
            print('Please input the rating number:')
        except:
            print('Invalid Order ID. Please check the input and try again. Returning to Staff UI.')
            return 0
    else:
        print('Invalid order ID. Returning to Staff UI.')
        return 0
    if dt & (dt[8] != 0):
        fb = int(input('1. Very bad\n2. Bad\n3. Neutral\4. Good\n5. Very good'))
        if 0 < fb < 6 :
            dt[8] = fb
            return writeto(odb, dt)
        else:
            print('Invalid input. Make sure its within the given range. Returning to Staff UI')
            return 0
    else:
        print('You are not allowed to give feedback on this order, Returning to Staff UI.')   
        return 0 

# Search for customer order by Admin
def custOrderQuery():
    odb = 'orders.txt'
    query = int(input('Please enter customer order ID to start search:'))
    if query:
        try:
            displayOrder(getrow(odb, query))
            print('Query completed. Returning to Admin UI.')
            return 1
        except ValueError:
            print('Order not found! Please make sure you entered the correct order ID with numbers only.\n')
            return 0
    print('No query detected. Returning to Admin UI.')
    return 0

# Search for customer payment by Admin
def custPaymentQuery():
    pdb = 'payments.txt'
    query = int(input('Please enter payment ID to start search:'))
    if query:
        try:
            displayPayment(getrow(pdb, query))
            print('Query completed. Returning to Admin UI.')
            return 1
        except ValueError:
            print('Payment record not found! Please make sure you entered the correct payment ID with numbers only.\n')
            return 0
    print('No query detected. Returning to Admin UI.')
    return 0

# List out all customer order by Admin
def listcustOrder():
    odb = 'orders.txt'
    print('Listing out all customer orders...')
    try:
        olist = getcolumn(odb, 0)
        for oid in olist:
            displayOrder(getrow(odb, oid))
        print('Listing completed. Returning to Main UI.')
        return 1
    except:
        print('An error occurred. Returning to Admin UI.')        
        return 0

# List out all customer order by Admin
def listcustPayment():
    pdb = 'payments.txt'
    print('Listing out all payment records...')
    try:
        plist = getcolumn(pdb, 0)
        for pid in plist:
            displayPayment(getrow(pdb, pid))
        print('Listing completed. Returning to Main UI.')
        return 1
    except:
        print('An error occurred. Returning to Admin UI.')        
        return 0

# Determine choices from each UI function
def fnsorter(u, o, r):
    r = r.lower()
    if r == 'admin':
        if o == 1:
            addCat()   # Add new category
            adminui(u)
        elif o == 2:
            modCat()   # modify category
            adminui(u)
        elif o == 3:
            itemSubMenu(u)  # Add/Modify Item
        elif o == 4:
            listallItem()   # Display all item details
            adminui(u)
        elif o == 5:
            custOrderQuery()  # Search customer order
            adminui(u)
        elif o == 6:
            custPaymentQuery()   # Search customer payment history
            adminui(u)
        elif o == 7:
            delmanSubMenu()    # Add/Modify/Delete Delivery Staffs
        elif o == 8:
            delmanSearch()    # Search Delivery Staff
            adminui(u)
        elif o == 9:
            delmanAssign()    # Assign order to Delivery Staff
            adminui(u)
        elif o == 0:
            logout()
        else:
            criterr()  
    elif r == 'staff':
        if o == 1:
            listallDelOrder(u)     # View/Select Order for Delivery
            staffui(u)
        elif o == 2:
            orderUpdate(u)     # Update Delivery status
            staffui(u)
        elif o == 3:
            orderFeedback()    # Take feedback on delivery
            staffui(u)
        elif o == 0:
            logout()
        else:
            criterr() 
    elif r == 'cust':
        if o == 1:
            listCat()   # View category details
            custui(u)
        elif o == 2:
            listallItem()   # View Item Details
            custui(u)
        elif o == 3:
            listItembyCat()   # View Item by Category
            custui(u)
        elif o == 4:
            placeOrder(u)   # Place order
            custui(u)
        elif o == 5:
            makePayment(u)   # Make order
            custui(u)
        elif o == 0:
            logout()
        else:
            criterr()
    elif r == 'guest':
        if o == 1:
            listallItem()
            mainui()
        elif o == 2:
            loginhandler()
        elif o == 3:
            custreghandler()
        elif o == 0:
            print('Have a nice day. Goodbye.')
            exit()
        else:
            criterr()   
    else:
        criterr()

# To print out order details
# Takes in list object, iterate and print it out with description
def displayOrder(l):
    c = 0
    column = ['Order ID: ', 'Order created time: ', 'Products: ','Associated payment ID: ', "Customer's username: ", 'Order total amount: ', "Order delivery status: ", "Order delivered date: ", "Order feedback: ", "Delivery info: ", "Placeholder: "]
    for i in l:
        print(column[c], i)
        c += 1
    return 1

# To print out payment details
# Takes in list object, iterate and print it out with description
def displayPayment(l):
    c = 0
    column = ['Payment ID: ', 'Payment method: ', 'Payment amount: ', 'Confirmation code: ', 'Payment time: ' ]
    for i in l:
        print(column[c], i)
        c += 1
    return 1

# To get current time
# Create a file, read created time and destroy it
def gettime(): 
    tfile = 'reow.txt'
    reow = os.open(tfile, os.O_RDWR)
    os.write(reow, "testline")
    os.close(reow)
    readtime = os.path.getmtime(tfile)
    os.remove(tfile)
    return readtime

# Column processing function
# To get a whole list of specific column from the desired file
def getcolumn(filename, co):
    cdict = []
    with open(filename, 'r') as file:
        #for line in linesanitize(file.readlines()):
        for line in file.readlines():
            cdict.append(line.split(";")[co])    
    file.close()
    return cdict

# Row processing function
# Require filename and row id(line number), return data of row as dict
def getrow(filename, ro):
    with open(filename, 'r') as file:
        #data = linesanitize(file.readlines())
        data = file.readlines()
        cdict = data[ro].split(";")
    return cdict

# Write file function
# Write/append lines(lists) into specified file
# Note: This function can ONLY do write only tasks, file open with write only permission
def writeto(f, dt):
    try:
        with open(f, 'w') as file:
            file.write(";".join(dt))
        return 1
    except BaseException as e:
        print('An error occurred:', e)
        return e

# Update row function
# Update only one row with defined row number
def updaterow(file, row, data):
    try:
        with open(file, 'r+') as filestream:
            lines = filestream.readlines()
            ln = 0
            for line in lines:
                if ln == row:
                    filestream.write(';'.join(data))
                else:
                    filestream.write(line)
                ln += 1
            filestream.writelines(data)
        return 1
    except BaseException as e:
        print('An error occurred: ', e)
        return 0

# Iterate function to go through all basestring and capture with data
def theMagic(bstring):
    c = 0
    lst = []
    for item in bstring:
        if item.find(':') != -1:
            if item.find('full') != -1:
                titem = input(item)
                lst.append(titem) if datavalidate(titem, 1) != 0 else lst.append(input('Please enter valid FULL NAME:'))
                c += 1
                continue
            if item.find('email') != -1:
                titem = input(item)
                lst.append(titem) if datavalidate(titem, 2) != 0 else lst.append(input('Please enter valid EMAIL:'))
                c += 1
                continue
            if item.find('phone') != -1:
                titem = input(item)
                lst.append(titem) if datavalidate(titem, 3) != 0 else lst.append(input('Please enter valid PHONE NUMBER:'))
                c += 1
                continue
            if item.find('address') != -1:
                titem = input(item)
                lst.append(titem) if datavalidate(titem, 4) != 0 else lst.append(input('Please enter valid ADDRESS:'))
                c += 1
                continue
            lst.append(input(item))
            c += 1
        else:
            lst.append(bstring[c])
            c += 1
    return lst

# Lines/Entry sanitizing function
# Clear off all unexpected spaces and/or special symbols when read from file
# Should be called in line processing, return a full line and only one line
def linesanitize(x): return x.rstrip(".\n").strip()

# User input sanitizing function
# Remove sensitive symbol(;) with others and unwanted spaces from user input
def dettol(x): return x.rstrip("\:;").strip()

# Logout function
# Return user to main UI, simple and eazy
def logout(): mainui() 

# Handle unexpected errors function
# Print contact help message, then force close the app
def criterr():
    print('Unexpected error: Invalid argument. Please follow the instructions given, or contact software support.')
    exit()

# Data Validation function for custom data type checks
# 1: Name, 2: Email, 3: Phone, 4: Addres, else: just return
def datavalidate(dt, param):
    if param == 1:
        return dt if list(filter(lambda c: c.isupper(), dt)) != [] else  0
    elif param == 2:
        return dt if (dt.find('.') != -1) and (dt.find('@') != -1) else 0
    elif param == 3:
        return int(''.join(c for c in dt if c.isdigit())) if dt.find('+') != -1 else 0
    elif param == 4:
        return dt if dt.find(',') != -1 else 0
    else:
        return dt

# Initialize & start program
# Display welcome message, check files & environment
# Must stay at most bottom
def init():
    print('Welcome to APU Online Shopping Mall(AOSM)!\n\n')
    fileList = ['users.txt', 'orders.txt', 'products.txt', 'customers.txt', 'category.txt', 'payments.txt']
    for f in fileList:
        try: 
            fs = os.open(f, os.O_RDWR)
            os.close(fs)
        except OSError as e:
            print('An error occurred. Please try to create "', f, '" manually\n')
            raise e
        except:
            print('Environment check failed. Please contact support.')
            exit()
    mainui() 

init()