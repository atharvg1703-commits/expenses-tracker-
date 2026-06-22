import sys
import time
import json
import os
import datetime

try:
    import colors
    GREEN = colors.green
    BLUE = colors.blue
    YELLOW = colors.yellow
    RED = colors.red
    CYAN = colors.cyan
    OFF = colors.off
except:
    GREEN = "\033[92m"
    BLUE = "\033[94m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    CYAN = "\033[96m"
    OFF = "\033[0m"

DATA_FILE = "expenses.json"

def slow_print(text, speed=0.025):          # Adjust speed as needed (lower is faster)
    index = 0
    length = len(text)
    while index < length:
        char = text[index]                   # btw this is slowprint
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(speed)
        index = index + 1
    print()


def fast_print(text, speed=0.01):
    index = 0
    length = len(text)
    while index < length:                       # this is fast print
        char = text[index]
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(speed)
        index = index + 1
    print()


def load_data():
    file_exists = os.path.exists(DATA_FILE)     # load data from json file, if it doesn't exist or is corrupted, start with empty data
    if file_exists == False:
        return {"next_id": 1, "items": {}}
    file = open(DATA_FILE, "r")
    content = file.read()
    file.close()
    if content == "":
        return {"next_id": 1, "items": {}}
    try:
        loaded = json.loads(content)
    except json.JSONDecodeError:
        print(f"{RED}Warning: expenses.json was corrupted. Starting with a fresh list.{OFF}")
        return {"next_id": 1, "items": {}}
    if "items" not in loaded:
        loaded["items"] = {}
    if "next_id" not in loaded:
        loaded["next_id"] = 1
    return loaded


def save_data(data):
    file = open(DATA_FILE, "w")     # save data to json file
    json.dump(data, file)
    file.close()


def get_valid_amount():
    while True:
        amount = input("Enter expense amount: ")    # keep asking until user enters a valid number
        try:
            float(amount)
            return amount
        except ValueError:
            print(f"{RED}That doesn't look like a number. Try again (e.g. 12.50).{OFF}")


def auto_categorize(name):
    text = name.lower()

    categories = {
        "Food": "food,pizza,burger,burgers,cheeseburger,restaurant,cafe,diner,eatery,lunch,dinner,breakfast,brunch,snack,coffee,grocery,groceries,supermarket,rice,pasta,noodles,bread,naan,tortilla,fries,potatoes,pho,pad thai,nasi goreng,poutine,arepas,polenta,couscous,croissant,pierogi,taco,tacos,sushi,banh mi,shawarma,gyro,falafel,kebab,hot dog,burrito,dim sum,empanada,samosa,spring roll,satay,fried chicken,steak,tikka masala,wings,rendang,duck,schnitzel,meatloaf,ribs,yakitori,kung pao,lamb,goulash,fish and chips,paella,ceviche,lobster,poke,shrimp,salmon,chowder,gumbo,tom yum,miso,minestrone,salad,hummus,guacamole,chana masala,tofu,mozzarella,cheese,chips,popcorn,nachos,pretzel,jamon,prosciutto,cookie,ice cream,brownie,donut,doughnut,pancake,pie,churro,cheesecake,macaron,mcdonald,subway,starbucks,kfc,luckin,domino,pizza hut,burger king,dunkin,taco bell,wendy,dairy queen,papa john,little caesar,baskin,sonic,chipotle,chick-fil-a,popeyes,arby,tim hortons,panera,panda express,jimmy john,jersey mike,hardee,carl's jr,applebee,wallace,ubereats,doordash,grubhub,deliveroo,postmates,seamless,bbq,barbecue",

        "Transportation": "gas,fuel,uber,lyft,bus,train,metro,car,parking,toll,taxi,cab,rideshare,auto repair,oil change,tire,dmv,registration,insurance car,amtrak,flight,airline,airfare,rental car,bike,scooter,ferry,shuttle,carpool,ev charging,charging station",

        "Entertainment": "game,gaming,movie,cinema,theater,theatre,netflix,spotify,hulu,disney+,hbo,concert,ticket,tickets,steam,xbox,playstation,nintendo,twitch,youtube premium,amusement park,bowling,arcade,festival,show,comedy,museum,zoo,aquarium,amusement,vinyl,music,podcast,app store",

        "School": "book,books,school,supplies,tuition,pencil,notebook,textbook,binder,backpack,college,university,exam fee,course,class fee,tutoring,lab fee,student loan,scholarship,library fine,printer,calculator,highlighter,folder,laptop school,fafsa,campus",

        "Bills": "rent,mortgage,electric,electricity,water bill,internet,wifi,phone bill,utility,utilities,gas bill,trash,sewer,cable,streaming bill,insurance,hoa,subscription,lease,loan payment,credit card payment,cell phone,heating,cooling,property tax",

        "Shopping": "clothes,clothing,shoes,shirt,pants,dress,jacket,amazon,mall,target,walmart,costco,online order,purchase,accessories,jewelry,handbag,sneakers,makeup,cosmetics,electronics,gadget,furniture,decor,gift,best buy,ebay,etsy,ikea",

        "Health": "doctor,medicine,pharmacy,dentist,hospital,clinic,prescription,therapy,therapist,checkup,vitamins,copay,insurance health,dental,orthodontist,optometrist,glasses,contacts,gym,vaccine,urgent care,physical therapy,counseling,mental health,x-ray,surgery",
    }

    for category, keywords in categories.items():
        if any(k in text for k in keywords.split(",")):
            return category

    return "Uncategorized"


def add_expense(data):
    name = input("Enter expense name: ").strip()
    if name == "":
        print(f"{RED}Expense name can't be empty. Cancelled.{OFF}")  # your expense needs to :
        return
    amount = get_valid_amount()                                             # -have a name and an amount 
    category = auto_categorize(name)                #-category is now auto-detected from the name
    date = datetime.datetime.now().isoformat()
    expense = {
        "name": name,
        "amount": amount,
        "category": category,
        "date": date
    }
    expense_id = data["next_id"]
    data["items"][str(expense_id)] = expense
    data["next_id"] = expense_id + 1
    save_data(data)
    print(f"{GREEN}Expense added successfully! (ID: {expense_id}, Category: {category}){OFF}")


def delete_expense(data):
    if len(data["items"]) == 0:
        print(f"{YELLOW}No expenses to delete!{OFF}")
        return
    expense_id = input("Enter expense ID to delete: ").strip()
    if expense_id in data["items"]:                                 #incase you want to delete
        name = data["items"][expense_id]["name"]                       # will ask for confirmation before deleting, just to be safe
        confirm = input(f"Delete '{name}' (ID {expense_id})? (y/n): ").strip().lower()      # and an ID
        if confirm == "y":
            del data["items"][expense_id]
            save_data(data)
            print(f"{GREEN}Expense deleted successfully!{OFF}")
        else:
            print(f"{YELLOW}Cancelled. Nothing was deleted.{OFF}")
    else:
        print(f"{RED}Expense ID not found!{OFF}")


def view_expenses(data):
    if len(data["items"]) == 0:                 # pretty straight forward just for viewing
        print(f"{YELLOW}No expenses found!{OFF}")
    else:
        for expense_id, expense in data["items"].items():
            name = expense.get("name", "Unknown")
            amount = expense.get("amount", "0")
            category = expense.get("category", "Uncategorized") #hashbrow. or is it hashtag 
            date = expense.get("date", "Unknown")
            fast_print(f"{BLUE}ID: {expense_id}{OFF}")
            fast_print(f"{RED}  Name: {name}{OFF}")
            fast_print(f"{GREEN}  Amount: {amount}{OFF}")
            fast_print(f"{YELLOW}  Category: {category}{OFF}")
            fast_print(f"{CYAN}  Date: {date}{OFF}")
            print()


def view_summary(data):
    if len(data["items"]) == 0:         #summary by category and month just loops through expenses and adds up totals, then prints them out. If there are no expenses, it tells you.
        print(f"{YELLOW}No expenses found!{OFF}")
    else:
        category_totals = {}
        for expense in data["items"].values():
            category = expense.get("category", "Uncategorized")
            try:
                amount = float(expense.get("amount", 0))
            except (ValueError, TypeError):
                amount = 0.0
            if category in category_totals:
                category_totals[category] += amount
            else:
                category_totals[category] = amount
        print(f"{CYAN}Expense Summary by Category:{OFF}")
        for category, total in category_totals.items():
            fast_print(f"{GREEN}  {category}: {round(total, 2)}{OFF}")


def summary_by_month(data):
    if len(data["items"]) == 0:             # if you want it by month
        print(f"{YELLOW}No expenses found!{OFF}")
    else:
        month_totals = {}
        for expense in data["items"].values():
            date_text = expense.get("date", "")
            try:
                date = datetime.datetime.fromisoformat(date_text)
                month = date.strftime("%Y-%m")
            except (ValueError, TypeError):
                month = "Unknown"
            try:
                amount = float(expense.get("amount", 0))
            except (ValueError, TypeError):
                amount = 0.0
            if month in month_totals:
                month_totals[month] += amount       #does anyone read these?
            else:
                month_totals[month] = amount
        print(f"{CYAN}Expense Summary by Month:{OFF}")
        for month, total in month_totals.items():
            fast_print(f"{GREEN}  {month}: {round(total, 2)}{OFF}")


def total_expenses(data):
    if len(data["items"]) == 0:                 #can get more straight forward than this
        print(f"{YELLOW}No expenses found!{OFF}")   # just all the money you spend
        return 0
    total = 0
    for expense in data["items"].values():
        try:
            amount = float(expense.get("amount", 0))
        except (ValueError, TypeError):
            amount = 0.0
        total += amount
        name = expense.get("name", "Unknown")
        category = expense.get("category", "Uncategorized")
        title = name + " (" + category + ")"
        fast_print(f"{BLUE}  {title}: {expense.get('amount', 0)}{OFF}")
    return total


def restart_program():                      # incase your want to restart
    confirm = input("Are you sure you want to restart the program? (y/n): ").strip().lower()
    if confirm == "y":
        if os.path.exists(DATA_FILE):
            os.remove(DATA_FILE)            # wipes the saved expenses before relaunching
        python = sys.executable
        os.execl(python, python, *sys.argv)
    else:
        print(f"{GREEN}Program will continue...{OFF}")


def skip_animation(): # the animation only looks cool the first 100 times
    confirm = input("Skip animations? (y/n): ").strip().lower()
    if confirm == "y":
        print(f"{GREEN}Animations skipped!{OFF}")
        return True
    else:
        print(f"{GREEN}Animations enabled!{OFF}")
        return False


def print_menu_one():                   # this is the main menu for people who are sick of the animations
    print(f"{CYAN}╔══════════════════════╗{OFF}")
    print(f"{CYAN}  EXPENSE TRACKER{OFF}")
    print(f"{CYAN}╚══════════════════════╝{OFF}")
    print(f"{GREEN}  1) Add an expense{OFF}")
    print(f"{RED}  2) Delete an expense{OFF}")
    print(f"{YELLOW}  3) View all expenses{OFF}")
    print(f"{CYAN}  4) Summary by category{OFF}")
    print(f"{GREEN}  5) Summary by month{OFF}")
    print(f"{YELLOW}  6) Show total spent{OFF}")
    print(f"{RED}  7) Restart program{OFF}")
    print(f"{RED}  8) Exit{OFF}")
    print(f"{CYAN}  9) Toggle animations{OFF}")
    print()
        


def print_menu():           # this is the main menu with animations, it uses slow_print to print each line with a delay, 
    slow_print(f"{CYAN}╔══════════════════════╗{OFF}")
    slow_print(f"{CYAN}  EXPENSE TRACKER{OFF}")
    slow_print(f"{CYAN}╚══════════════════════╝{OFF}")
    slow_print(f"{GREEN}  1) Add an expense{OFF}")
    slow_print(f"{RED}  2) Delete an expense{OFF}")
    slow_print(f"{YELLOW}  3) View all expenses{OFF}")
    slow_print(f"{CYAN}  4) Summary by category{OFF}")
    slow_print(f"{GREEN}  5) Summary by month{OFF}")
    slow_print(f"{YELLOW}  6) Show total spent{OFF}")
    slow_print(f"{RED}  7) Restart program{OFF}")
    slow_print(f"{RED}  8) Exit{OFF}")
    slow_print(f"{CYAN}  9) Toggle animations{OFF}")
    print()


def main():                     # main program loop
    data = load_data()
    animations_off = False
    while True:
        if animations_off == True:
            print_menu_one()
        else:
            print_menu()

        choice = input("Enter your choice: ").strip()
        if choice == "1":
            add_expense(data)
        elif choice == "2":
            delete_expense(data)
        elif choice == "3":
            view_expenses(data)
        elif choice == "4":
            view_summary(data)
        elif choice == "5":
            summary_by_month(data)
        elif choice == "6":
            total = total_expenses(data)
            print(f"{GREEN}Total Expenses: {round(total, 2)}{OFF}")
        elif choice == "7":
            restart_program()
        elif choice == "8":
            print(f"{GREEN}Goodbye!{OFF}")
            break
        elif choice == "9":
            animations_off = skip_animation()
        else:
            print(f"{RED}Invalid choice! Please try again.{OFF}")
        print()


if __name__ == "__main__": #and this just runs the main function when you run the program, which starts the whole thing
    main()
# Expense Tracker by Atharv Garg - https://github.com/atharvg1703-commits
# I want to hit 300 lines 
# the animations are very nice also the category auto-detection is pretty cool
# happy spending! (or not spending, whatever you prefer)
# I hope you like it it was a lot of work
# 300 lines yipee
# last update: 2026-06-22
# well know its a lot more than 300 lines but I added a lot of features so I hope you don't mind
