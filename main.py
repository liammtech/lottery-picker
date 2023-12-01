import random, sys, os, requests, bs4, re, datetime, pprint, pandas as pd, warnings, numpy

warnings.simplefilter(action='ignore')
pd.set_option('display.max_rows', None)

#####EUROMILLIONS JACKPOT
res_euromillions = requests.get("https://www.national-lottery.co.uk/games/euromillions")
euro_page = bs4.BeautifulSoup(res_euromillions.text, "html.parser")
euromillions_jackpot_selector = euro_page.select("#content > div > div:nth-child(1) > div.grid_4 > div > div > div > div:nth-child(2) > div > div > div.com_inner.clr > div > div > h2 > span.amount.amount_large")
try:
    euromillions_jackpot = "Current jackpot is " + euromillions_jackpot_selector[0].text.strip().replace("MM", " M").replace("*","")
except:
    euromillions_jackpot = "Next jackpot will show once next game opens"

#####EUROMILLIONS TICKET PRICE
try:
    euromillions_ticket_selector = euro_page.select(".game_price")
    euromillions_ticket = "Current price per ticket is " + euromillions_ticket_selector[0].text.strip()
except:
    euromillions_ticket = "Ticket price will be available when next game opens"

#####EUROMILLIONS NEXT DRAW
today = datetime.date.today()
tuesday = today + datetime.timedelta( (1-today.weekday()) % 7 )
friday = today + datetime.timedelta( (4-today.weekday()) % 7 )
tues_formatted = tuesday.strftime("%d %B %Y")
fri_formatted = friday.strftime("%d %B %Y")

if tuesday == datetime.date.today():
    euro_tuesday_message = "TONIGHT"
elif datetime.date.today() - tuesday == datetime.timedelta(days=-1):
    euro_tuesday_message = ("tomorrow, Tuesday " + str(tues_formatted))
else:
    euro_tuesday_message = ("on Tuesday " + str(tues_formatted))

if friday == datetime.date.today():
    euro_friday_message = "TONIGHT"
elif datetime.date.today() - friday == datetime.timedelta(days=-1):
    euro_friday_message = ("tomorrow, Friday " + str(fri_formatted))
else:
    euro_friday_message = ("on Friday " + str(fri_formatted))

if tuesday < friday:
    euro_next_draw = euro_tuesday_message
else:
    euro_next_draw = euro_friday_message

#####EUROMILLIONS COUNTDOWN
try:
    euromillions_days_selector = euro_page.select("span.unit:nth-child(1) > span:nth-child(1)")
    euromillions_hours_selector = euro_page.select("span.unit:nth-child(2) > span:nth-child(1)")
    euromillions_minutes_selector = euro_page.select("span.unit:nth-child(3) > span:nth-child(1)")
    euromillions_days = euromillions_days_selector[0].text.strip()
    euromillions_hours = euromillions_hours_selector[0].text.strip()
    euromillions_minutes = euromillions_minutes_selector[0].text.strip()
    euro_counts = [int(euromillions_days), int(euromillions_hours), int(euromillions_minutes)]
    if all(v == 0 for v in euro_counts):
        euro_countdown = "Tonight's game has already closed"
    else:
        euro_countdown = ("Game closes in " + str(euromillions_days) + " days, " + str(euromillions_hours) + " hours, and " + str(euromillions_minutes) + " minutes")
except:
    euro_countdown = "Tonight's game has already closed"

#####EUROMILLIONS RESULTS HISTORY
euro_history = pd.read_csv("https://www.national-lottery.co.uk/results/euromillions/draw-history/csv")
try:
    euro_history['European Millionaire Maker'].loc[euro_history['European Millionaire Maker'].str.len() > 10] = 'Multiple'
except:
    pass
euro_history['UK Millionaire Maker'].loc[euro_history['UK Millionaire Maker'].str.len() > 10] = 'Multiple'
try:
    euro_history['European Millionaire Maker'].loc[pd.isna(euro_history['European Millionaire Maker'])] = 'n/a'
    
except:
    pass
euro_history['UK Millionaire Maker'].loc[pd.isna(euro_history['UK Millionaire Maker'])] = 'n/a'

#####EUROMILLIONS LEAST COMMON BALLS
euro_least = euro_history[['Ball 1', 'Ball 2', 'Ball 3', 'Ball 4', 'Ball 5']].apply(pd.Series.value_counts).sum(axis='columns').sort_values(ascending=False).head(5).index.values
euro_bonus_least = euro_history[['Lucky Star 1', 'Lucky Star 2']].apply(pd.Series.value_counts).sum(axis='columns').sort_values(ascending=True).head(2).index.values
euro_least_sort = numpy.sort(euro_least)
euro_bonus_least_sort = numpy.sort(euro_bonus_least)

#####EUROMILLIONS MOST COMMON BALLS
euro_mode = euro_history[['Ball 1', 'Ball 2', 'Ball 3', 'Ball 4', 'Ball 5']].apply(pd.Series.value_counts).sum(axis='columns').sort_values(ascending=False).head(5).index.values
euro_bonus_mode = euro_history[['Lucky Star 1', 'Lucky Star 2']].apply(pd.Series.value_counts).sum(axis='columns').sort_values(ascending=False).head(2).index.values
euro_mode_sort = numpy.sort(euro_mode)
euro_bonus_mode_sort = numpy.sort(euro_bonus_mode)

#####LOTTO JACKPOT
res_lotto = requests.get("https://www.national-lottery.co.uk/games/lotto?icid=home:bd:3:gc:lo:dbg:pl:btn")
lotto_page = bs4.BeautifulSoup(res_lotto.text, "html.parser")
lotto_jackpot_selector = lotto_page.select("#nextdrawpromo > h2 > span.pixel-placement > span.amount")
try:
    lotto_jackpot = "Current jackpot is " + lotto_jackpot_selector[0].text.strip().replace("M", " Million").replace("*","")
except:
    lotto_jackpot = "Next jackpot will show once next game opens"

#####LOTTO TICKET PRICE
try:
    lotto_ticket_selector = lotto_page.select(".game_price")
    lotto_ticket = "Current price per ticket is " + lotto_ticket_selector[0].text.strip().replace(" per play", "")
except:
    lotto_ticket = "Ticket price will be available when next game opens"

#####LOTTO NEXT DRAW
wednesday = today + datetime.timedelta( (2-today.weekday()) % 7 )
saturday = today + datetime.timedelta( (5-today.weekday()) % 7 )
weds_formatted = wednesday.strftime("%d %B %Y")
sat_formatted = saturday.strftime("%d %B %Y")

if wednesday == datetime.date.today():
    lotto_wednesday_message = "TONIGHT"
elif datetime.date.today() - wednesday == datetime.timedelta(days=-1):
    lotto_wednesday_message = ("tomorrow, Wednesday " + str(weds_formatted))
else:
    lotto_wednesday_message = ("on Wednesday " + str(wednesday))

if saturday == datetime.date.today():
    lotto_saturday_message = "TONIGHT"
elif datetime.date.today() - saturday == datetime.timedelta(days=-1):
    lotto_saturday_message = ("tomorrow, Saturday " + str(weds_formatted))
else:
    lotto_saturday_message = ("on Saturday " + str(saturday))

if wednesday < saturday:
    lotto_next_draw = lotto_wednesday_message
else:
    lotto_next_draw = lotto_saturday_message

#####LOTTO COUNTDOWN
try:
    lotto_days_selector = lotto_page.select("span.unit:nth-child(1) > span:nth-child(1)")
    lotto_hours_selector = lotto_page.select("span.unit:nth-child(2) > span:nth-child(1)")
    lotto_minutes_selector = lotto_page.select("span.unit:nth-child(3) > span:nth-child(1)")
    lotto_days = lotto_days_selector[0].text.strip()
    lotto_hours = lotto_hours_selector[0].text.strip()
    lotto_minutes = lotto_minutes_selector[0].text.strip()
    euro_counts = [lotto_days, lotto_hours, lotto_minutes]
    if all(int(v) == 0 for v in euro_counts):
        lotto_countdown = "Tonight's game has already closed"
    else:
        lotto_countdown = ("Game closes in " + str(lotto_days) + " days, " + str(lotto_hours) + " hours, and " + str(lotto_minutes) + " minutes")
except:
    lotto_countdown = "Tonight's game has already closed"

#####LOTTO RESULTS HISTORY
lotto_history = pd.read_csv("https://www.national-lottery.co.uk/results/lotto/draw-history/csv")

#####LOTTO LEAST COMMON BALLS
lotto_least = lotto_history[['Ball 1', 'Ball 2', 'Ball 3', 'Ball 4', 'Ball 5', 'Ball 6']].apply(pd.Series.value_counts).sum(axis='columns').sort_values(ascending=False).head(6).index.values
lotto_least_sort = numpy.sort(lotto_least)

#####LOTTO MOST COMMON BALLS
lotto_mode = lotto_history[['Ball 1', 'Ball 2', 'Ball 3', 'Ball 4', 'Ball 5', 'Ball 6']].apply(pd.Series.value_counts).sum(axis='columns').sort_values(ascending=False).head(6).index.values
lotto_mode_sort = numpy.sort(lotto_mode)

#####THUNDERBALL JACKPOT
res_thunderball = requests.get("https://www.national-lottery.co.uk/games/thunderball?icid=home:bd:3:gc:tb:dbg:pl:btn")
thunderball_page = bs4.BeautifulSoup(res_thunderball.text, "html.parser")
thunderball_jackpot_selector = thunderball_page.select(".amount")
try:
    thunderball_jackpot = "Current jackpot is " + thunderball_jackpot_selector[0].text.strip().replace("KThousand", ",000").replace("*","")
except:
    thunderball_jackpot = "Next jackpot will show once next game opens"

#####THUNDERBALL TICKET PRICE
try:
    thunderball_ticket_selector = thunderball_page.select(".game_price")
    thunderball_ticket = "Current price per ticket is " + thunderball_ticket_selector[0].text.strip().replace("KThousand", ",000").replace("*","")
except:
    thunderball_ticket = "Ticket price will be available when next game opens"

#####THUNDERBALL NEXT DRAW
if tuesday == datetime.date.today():
    tball_tuesday_message = "TONIGHT"
elif datetime.date.today() - tuesday == datetime.timedelta(days=-1):
    tball_tuesday_message = ("tomorrow, Tuesday " + str(tues_formatted))
else:
    tball_tuesday_message = ("on Tuesday " + str(tues_formatted))

if wednesday == datetime.date.today():
    tball_wednesday_message = "TONIGHT"
elif datetime.date.today() - wednesday == datetime.timedelta(days=-1):
    tball_wednesday_message = ("tomorrow, Wednesday " + str(weds_formatted))
else:
    tball_wednesday_message = ("on Wednesday " + str(wednesday))

if friday == datetime.date.today():
    tball_friday_message = "TONIGHT"
elif datetime.date.today() - friday == datetime.timedelta(days=-1):
    tball_friday_message = ("tomorrow, Friday " + str(fri_formatted))
else:
    tball_friday_message = ("on Friday " + str(fri_formatted))

if saturday == datetime.date.today():
    tball_saturday_message = "TONIGHT"
elif datetime.date.today() - saturday == datetime.timedelta(days=-1):
    tball_saturday_message = ("tomorrow, Saturday " + str(weds_formatted))
else:
    tball_saturday_message = ("on Saturday " + str(saturday))

tball_dates = [tuesday, wednesday, friday, saturday]
tball_messages = {tuesday: tball_tuesday_message, wednesday: tball_wednesday_message, friday: tball_friday_message, saturday: tball_saturday_message}

next_tball_date = min(tball_dates)
tball_next_draw = tball_messages[next_tball_date]

#####THUNDERBALL COUNTDOWN
try:
    tball_days_selector = thunderball_page.select("span.unit:nth-child(1) > span:nth-child(1)")
    tball_hours_selector = thunderball_page.select("span.unit:nth-child(2) > span:nth-child(1)")
    tball_minutes_selector = thunderball_page.select("span.unit:nth-child(3) > span:nth-child(1)")
    tball_days = tball_days_selector[0].text.strip()
    tball_hours = tball_hours_selector[0].text.strip()
    tball_minutes = tball_minutes_selector[0].text.strip()
    tball_counts = [tball_days, tball_hours, tball_minutes]
    if all(int(v) == 0 for v in euro_counts):
        tball_countdown = "Tonight's game has already closed"
    else:
        tball_countdown = ("Game closes in " + str(tball_days) + " days, " + str(tball_hours) + " hours, and " + str(tball_minutes) + " minutes")
except:
    tball_countdown = "Tonight's game has already closed"

#####THUNDERBALL RESULTS HISTORY
thunderball_history = pd.read_csv("https://www.national-lottery.co.uk/results/thunderball/draw-history/csv")

#####THUNDERBALL LEAST COMMON BALLS
thunderball_least = thunderball_history[['Ball 1', 'Ball 2', 'Ball 3', 'Ball 4', 'Ball 5']].apply(pd.Series.value_counts).sum(axis='columns').sort_values(ascending=False).head(5).index.values
thunderball_bonus_least = thunderball_history[['Thunderball']].apply(pd.Series.value_counts).sum(axis='columns').sort_values(ascending=True).head(1).index.values
thunderball_least_sort = numpy.sort(thunderball_least)
thunderball_bonus_least_sort = thunderball_bonus_least

#####THUNDERBALL MOST COMMON BALLS
thunderball_mode = thunderball_history[['Ball 1', 'Ball 2', 'Ball 3', 'Ball 4', 'Ball 5']].apply(pd.Series.value_counts).sum(axis='columns').sort_values(ascending=False).head(5).index.values
thunderball_bonus_mode = thunderball_history[['Thunderball']].apply(pd.Series.value_counts).sum(axis='columns').sort_values(ascending=False).head(2).index.values
thunderball_mode_sort = numpy.sort(thunderball_mode)
thunderball_bonus_mode_sort = numpy.sort(thunderball_bonus_mode)

def clear_screen():
    if sys.platform == "linux" or sys.platform == "linux2":
        os.system("clear")
    elif sys.platform == "darwin":
        os.system("clear")
    elif sys.platform == "win32":
        os.system("cls")

def main_menu():
    clear_screen()
    print("--------LOTTERY PICKER--------\n\n Lotteries to play:\n\n1) EuroMillions\n2) Lotto\n3) Thunderball\n\nType number of lottery to play and press ENTER:", end=" ")
    while 1:
        lottery_choice = input()
        try:
            lottery_choice = int(lottery_choice)
        except:
            print("Not a valid selection, please choose 1, 2 or 3:", end=" ")
            continue
        if lottery_choice == 1:
            lottery_menu(1)
        elif lottery_choice == 2:
            lottery_menu(2)
        elif lottery_choice == 3:
            lottery_menu(3)
        else:
            print("Not a valid selection, please choose 1, 2 or 3:", end=" ")
    
def lottery_menu(lottery_choice):
    clear_screen()
    if lottery_choice == 1:
        print(f"--------EUROMILLIONS--------\n\nEuroMillions draw consists of 5 main balls (between 1 and 50) + 2 bonus balls (between 1 and 12)\n\nO O O O O - O O\n\n{euromillions_jackpot}\n{euromillions_ticket}\nNext draw is {euro_next_draw}\n{euro_countdown}")
    elif lottery_choice == 2:
        print(f"--------LOTTO--------\n\nLotto draw consists of 6 main balls + 1 bonus ball (all between 1 and 59) - you pick 6 balls, the bonus ball is a \"backup\" match\n\nO O O O O O\n\n{lotto_jackpot}\n{lotto_ticket}\nNext draw is {lotto_next_draw}\n{lotto_countdown}")
    elif lottery_choice == 3:
        print(f"--------THUNDERBALL--------\n\nThunderball draw consists of 5 main balls (between 1 and 39) + 1 bonus ball (between 1 and 14)\n\nO O O O O - O\n\n{thunderball_jackpot}\n{thunderball_ticket}\nNext draw is {tball_next_draw}\n{tball_countdown}")
    print("\nOptions:\n\n1) Pick numbers\n2) See results history\n3) Return to Main Menu\n\nType option number and press ENTER:", end=" ")
    while 1:
        option_choice = input()
        try:
            option_choice = int(option_choice)
        except:
            print("Not a valid selection, please choose 1, 2 or 3:", end=" ")
            continue
        if option_choice == 1:
            pick_numbers_menu(lottery_choice)
            continue
        elif option_choice == 2:
            results_history(lottery_choice)
            continue
        elif option_choice == 3:
            main_menu()
        else:
            print("Not a valid selection, please choose 1, 2 or 3:", end=" ")

def pick_numbers_menu(lottery_choice):
    clear_screen()
    lotteries = {1: "EuroMillions", 2: "Lotto", 3: "Thunderball"}
    pick_options = ["1) Random numbers","2) Average of previous results", "3) Most drawn numbers","4) Least drawn numbers","5) Return to previous menu","6) Return to Main Menu"]
    if lottery_choice == 1:
        print("--------EUROMILLIONS: Pick Numbers--------")
    elif lottery_choice == 2:
        print("--------LOTTO: Pick Numbers--------")
    elif lottery_choice == 3:
        print("--------THUNDERBALL: Pick Numbers--------")
    print("\nHow would you like to generate your numbers?\n")
    for i in pick_options:
        print(i)
    print("\nType option number and press ENTER:", end=" ")
    while 1:
        option_choice = input()
        try:
            option_choice = int(option_choice)
        except:
            print("Not a valid selection, please choose a number from the list of options shown:", end=" ")
            continue
        # Option for picking lottery numbers
        if option_choice == 1:
            rand_result(lottery_choice)
        # Option for viewing previous lottery numbers
        elif option_choice == 2:
            average_numbers_menu(lottery_choice)
        elif option_choice == 3:
            top_numbers_result(lottery_choice)
        elif option_choice == 4:
            least_numbers_result(lottery_choice)
        elif option_choice == 5:
            lottery_menu(lottery_choice)
        elif option_choice == 6:
            main_menu()
        else:
            print("Not a valid selection, please choose a number from the list of options shown:", end=" ")

def rand_result(lottery_choice):
    clear_screen()
    if lottery_choice == 1:
        euromillions_random()
    elif lottery_choice == 2:
        lotto_random()
    elif lottery_choice == 3:
        thunderball_random()

def euromillions_random():
    # Define lists for lottery numbers
    rand_result_main = []
    rand_result_bonus = []
    # Select EuroMillions balls 1 to 5
    i = 0
    while i < 5:
        a = random.randint(1, 50)
        if rand_result_main.count(a):
            continue
        else:
            i += 1
            rand_result_main.append(a)
    # Select EuroMillions bonus balls 1 and 2
    x = 0
    while x < 2:
        b = random.randint(1, 12)
        if rand_result_bonus.count(b):
            continue
        else:
            x += 1
            rand_result_bonus.append(b)
    rand_result_main.sort()
    rand_result_bonus.sort()
    ticket = list(rand_result_main[0:6] + rand_result_bonus[0:3])
    print("--------EUROMILLIONS: Pick Random Numbers--------\n\nYour EuroMillions ticket:\n")
    print(*ticket, sep=" - ")
    print("\nMore options:\n\n1) Pick random numbers again\n2) Return to Euromillions number-picking menu\n3) Return to main menu\n\nType option number and press ENTER:", end=" ")
    while 1:
        option_choice = input()
        try:
            option_choice = int(option_choice)
        except:
            print("Not a valid selection, please choose a number from the list of options shown:", end=" ")
            continue
        if option_choice == 1:
            print("\n")
            euromillions_random()
        elif option_choice == 2:
            pick_numbers_menu(1)
        elif option_choice == 3:
            main_menu()
        else:
            print("Not a valid selection, please choose 1, 2 or 3:", end=" ")

def lotto_random():
    # Define list for lottery numbers
    rand_result_main = []
    # Select all Lotto balls
    i = 0
    while i < 6:
        a = random.randint(1, 59)
        if rand_result_main.count(a):
            continue
        else:
            i += 1
            rand_result_main.append(a)
    rand_result_main.sort()
    ticket = list(rand_result_main[0:7])
    print("--------LOTTO: Pick Random Numbers--------\n\nYour Lotto ticket:\n")
    print(*ticket, sep=" - ")
    print("\nMore options:\n\n1) Pick random numbers again\n2) Return to Lotto number-picking menu\n3) Return to main menu\n\nType option number and press ENTER:", end=" ")
    while 1:
        option_choice = input()
        try:
            option_choice = int(option_choice)
        except:
            print("Not a valid selection, please choose a number from the list of options shown:", end=" ")
            continue
        if option_choice == 1:
            print("\n")
            lotto_random()
        elif option_choice == 2:
            pick_numbers_menu(2)
        elif option_choice == 3:
            main_menu()
        else:
            print("Not a valid selection, please choose a number from the list of options shown:", end=" ")

def thunderball_random():
    # Define lists for lottery numbers
    rand_result_main = []
    rand_result_bonus = []
    # Select Thunderball balls 1 to 5
    i = 0
    while i < 5:
        a = random.randint(1, 39)
        if rand_result_main.count(a):
            continue
        else:
            i += 1
            rand_result_main.append(a)
    rand_result_main.sort()
    # Select Thunderball bonus ball
    b = random.randint(1, 14)
    rand_result_bonus.append(b)
    ticket = list(rand_result_main[0:6] + rand_result_bonus)
    print("--------THUNDERBALL: Pick Random Numbers--------\n\nYour Thunderball ticket:\n")
    print(*ticket, sep=" - ")
    print("\nMore options:\n\n1) Pick random numbers again\n2) Return to Thunderball number-picking menu\n3) Return to main menu\n\nType option number and press ENTER:", end=" ")
    while 1:
        option_choice = input()
        try:
            option_choice = int(option_choice)
        except:
            print("Not a valid selection, please choose a number from the list of options shown:", end=" ")
            continue
        if option_choice == 1:
            print("\n")
            thunderball_random()
        elif option_choice == 2:
            pick_numbers_menu(3)
            pick_numbers_menu(3)
        elif option_choice == 3:
            main_menu()
        else:
            print("Not a valid selection, please choose 1, 2 or 3:", end=" ")

#AVERAGE NUMBERS
def average_numbers_menu(lottery_choice):
    clear_screen()
    pick_options = ["1) Mean numbers","2) Median numbers"]
    if lottery_choice == 1:
        print("--------EUROMILLIONS: Average Numbers--------")
    elif lottery_choice == 2:
        print("--------LOTTO: Average Numbers--------")
    elif lottery_choice == 3:
        print("--------THUNDERBALL: Average Numbers--------")
    print("\nHow would you like the average to be calculated?\n\n(Note: Averages are calculated amongst previous draws of a given ball number - ball 1, ball 2 etc. Choosing Mean will round to nearest whole number.)\n")
    for i in pick_options:
        print(i)
    print("\nType option number and press ENTER:", end=" ")
    while 1:
        option_choice = input()
        try:
            option_choice = int(option_choice)
        except:
            print("Not a valid selection, please choose a number from the list of options shown:", end=" ")
            continue
        if option_choice == 1:
            mean_result(lottery_choice)
        elif option_choice == 2:
            median_result(lottery_choice)
        else:
            print("Not a valid selection, please choose a number from the list of options shown:", end=" ")
            
def mean_result(lottery_choice):
    clear_screen()
    if lottery_choice == 1:
        euromillions_mean()
    elif lottery_choice == 2:
        lotto_mean()
    elif lottery_choice == 3:
        thunderball_mean()

def median_result(lottery_choice):
    clear_screen()
    if lottery_choice == 1:
        euromillions_median()
    elif lottery_choice == 2:
        lotto_median()
    elif lottery_choice == 3:
        thunderball_median()

def top_numbers_result(lottery_choice):
    clear_screen()
    if lottery_choice == 1:
        euromillions_top_balls()
    elif lottery_choice == 2:
        lotto_top_balls()
    elif lottery_choice == 3:
        thunderball_top_balls()

def least_numbers_result(lottery_choice):
    clear_screen()
    if lottery_choice == 1:
        euromillions_least_balls()
    elif lottery_choice == 2:
        lotto_least_balls()
    elif lottery_choice == 3:
        thunderball_least_balls()

def euromillions_mean():
    # Define lists for lottery numbers
    mean_result_main = []
    mean_result_bonus = []
    # Select EuroMillions balls 1 to 5
    i = 1
    while i < 6:
        a = round(euro_history.loc[:, str('Ball '+ str(i))].mean())
        mean_result_main.append(a)
        i += 1
    x = 1
    # Select EuroMillions bonus balls 1 and 2
    while x < 3:
        b = round(euro_history.loc[:, str('Lucky Star ' + str(x))].mean())
        mean_result_bonus.append(b)
        x += 1
    ticket = list(mean_result_main[0:6] + mean_result_bonus[0:3])
    print("--------EUROMILLIONS: Mean Average Numbers--------\n\n(Note: Averages of ball numbers are shown in ball-number order, and may not necessarily be in numerical order. May also contain duplicates.)\n\nYour EuroMillions ticket:\n")
    print(*ticket, sep=" - ")
    print("\nMore options:\n\n1) Return to EuroMillions number-picking menu\n2) Return to main menu\n\nType option number and press ENTER:", end=" ")
    while 1:
        option_choice = input()
        try:
            option_choice = int(option_choice)
        except:
            print("Not a valid selection, please choose a number from the list of options shown:", end=" ")
            continue
        if option_choice == 1:
            pick_numbers_menu(1)
        elif option_choice == 2:
            main_menu()
        else:
            print("Not a valid selection, please choose a number from the list of options shown:", end=" ")

def lotto_mean():
    # Define lists for lottery numbers
    mean_result_main = []
    # Select Lotto balls 1 to 6
    i = 1
    while i < 7:
        a = round(lotto_history.loc[:, str('Ball '+ str(i))].mean())
        mean_result_main.append(a)
        i += 1
    x = 1
    ticket = list(mean_result_main[0:7])
    print("--------LOTTO: Mean Average Numbers--------\n\nYour Lotto ticket:\n")
    print(*ticket, sep=" - ")
    print("\nMore options:\n\n1) Return to Lotto number-picking menu\n2) Return to main menu\n\nType option number and press ENTER:", end=" ")
    while 1:
        option_choice = input()
        try:
            option_choice = int(option_choice)
        except:
            print("Not a valid selection, please choose a number from the list of options shown:", end=" ")
            continue
        if option_choice == 1:
            pick_numbers_menu(2)
        elif option_choice == 2:
            main_menu()
        else:
            print("Not a valid selection, please choose a number from the list of options shown:", end=" ")

def thunderball_mean():
    # Define lists for lottery numbers
    mean_result_main = []
    mean_result_bonus = []
    # Select Thunderball balls 1 to 5
    i = 1
    while i < 6:
        a = round(thunderball_history.loc[:, str('Ball '+ str(i))].mean())
        mean_result_main.append(a)
        i += 1
    x = 1
    # Select Thunderball bonus ball
    b = round(thunderball_history.loc[:, 'Thunderball'].mean())
    mean_result_bonus.append(b)
    ticket = list(mean_result_main[0:6] + mean_result_bonus)
    print("--------THUNDERBALL: Mean Average Numbers--------\n\nYour Thunderball ticket:\n")
    print(*ticket, sep=" - ")
    print("\nMore options:\n\n1) Return to Thunderball number-picking menu\n2) Return to main menu\n\nType option number and press ENTER:", end=" ")
    while 1:
        option_choice = input()
        try:
            option_choice = int(option_choice)
        except:
            print("Not a valid selection, please choose a number from the list of options shown:", end=" ")
            continue
        if option_choice == 1:
            pick_numbers_menu(1)
        elif option_choice == 2:
            main_menu()
        else:
            print("Not a valid selection, please choose a number from the list of options shown:", end=" ")

def euromillions_median():
    # Define lists for lottery numbers
    mean_result_main = []
    mean_result_bonus = []
    # Select EuroMillions balls 1 to 5
    i = 1
    while i < 6:
        a = round(euro_history.loc[:, str('Ball '+ str(i))].median())
        mean_result_main.append(a)
        i += 1
    x = 1
    # Select EuroMillions bonus balls 1 and 2
    while x < 3:
        b = round(euro_history.loc[:, str('Lucky Star ' + str(x))].median())
        mean_result_bonus.append(b)
        x += 1
    ticket = list(mean_result_main[0:6] + mean_result_bonus[0:3])
    print("--------EUROMILLIONS: Median Average Numbers--------\n\n(Note: Averages of ball numbers are shown in ball-number order, and may not necessarily be in numerical order. May also contain duplicates.)\n\nYour EuroMillions ticket:\n")
    print(*ticket, sep=" - ")
    print("\nMore options:\n\n1) Return to EuroMillions number-picking menu\n2) Return to main menu\n\nType option number and press ENTER:", end=" ")
    while 1:
        option_choice = input()
        try:
            option_choice = int(option_choice)
        except:
            print("Not a valid selection, please choose a number from the list of options shown:", end=" ")
            continue
        if option_choice == 1:
            pick_numbers_menu(1)
        elif option_choice == 2:
            main_menu()
        else:
            print("Not a valid selection, please choose a number from the list of options shown:", end=" ")

def lotto_median():
    # Define lists for lottery numbers
    mean_result_main = []
    # Select Lotto balls 1 to 6
    i = 1
    while i < 7:
        a = round(lotto_history.loc[:, str('Ball '+ str(i))].median())
        mean_result_main.append(a)
        i += 1
    x = 1
    ticket = list(mean_result_main[0:7])
    print("--------LOTTO: Median Average Numbers--------\n\nYour Lotto ticket:\n")
    print(*ticket, sep=" - ")
    print("\nMore options:\n\n1) Return to Lotto number-picking menu\n2) Return to main menu\n\nType option number and press ENTER:", end=" ")
    while 1:
        option_choice = input()
        try:
            option_choice = int(option_choice)
        except:
            print("Not a valid selection, please choose a number from the list of options shown:", end=" ")
            continue
        if option_choice == 1:
            pick_numbers_menu(2)
        elif option_choice == 2:
            main_menu()
        else:
            print("Not a valid selection, please choose a number from the list of options shown:", end=" ")

def thunderball_median():
    # Define lists for lottery numbers
    mean_result_main = []
    mean_result_bonus = []
    # Select Thunderball balls 1 to 5
    i = 1
    while i < 6:
        a = round(thunderball_history.loc[:, str('Ball '+ str(i))].median())
        mean_result_main.append(a)
        i += 1
    x = 1
    # Select Thunderball bonus ball
    b = round(thunderball_history.loc[:, 'Thunderball'].median())
    mean_result_bonus.append(b)
    ticket = list(mean_result_main[0:6] + mean_result_bonus)
    print("--------THUNDERBALL: Median Average Numbers--------\n\nYour Thunderball ticket:\n")
    print(*ticket, sep=" - ")
    print("\nMore options:\n\n1) Return to Thunderball number-picking menu\n2) Return to main menu\n\nType option number and press ENTER:", end=" ")
    while 1:
        option_choice = input()
        try:
            option_choice = int(option_choice)
        except:
            print("Not a valid selection, please choose a number from the list of options shown:", end=" ")
            continue
        if option_choice == 1:
            pick_numbers_menu(1)
        elif option_choice == 2:
            main_menu()
        else:
            print("Not a valid selection, please choose a number from the list of options shown:", end=" ")

#MOST COMMON BALLS
def euromillions_top_balls():
    # Define lists for lottery numbers
    top_result_main = []
    top_result_bonus = []
    # Select EuroMillions balls 1 to 5
    for x in euro_mode_sort:
        top_result_main.append(x)
    # Select EuroMillions bonus balls 1 and 2
    for y in euro_bonus_mode_sort:
        top_result_bonus.append(y)
    ticket = list(top_result_main[0:6] + top_result_bonus[0:3])
    print("--------EUROMILLIONS: Most Common Numbers--------\n\nYour EuroMillions ticket:\n")
    print(*ticket, sep=" - ")
    print("\nMore options:\n\n1) Return to EuroMillions number-picking menu\n2) Return to main menu\n\nType option number and press ENTER:", end=" ")
    while 1:
        option_choice = input()
        try:
            option_choice = int(option_choice)
        except:
            print("Not a valid selection, please choose a number from the list of options shown:", end=" ")
            continue
        if option_choice == 1:
            pick_numbers_menu(1)
        elif option_choice == 2:
            main_menu()
        else:
            print("Not a valid selection, please choose a number from the list of options shown:", end=" ")

def lotto_top_balls():
    # Define lists for lottery numbers
    top_result_main = []
    # Select Lotto balls 1 to 6
    for x in lotto_mode_sort:
        top_result_main.append(x)
    # Select EuroMillions bonus balls 1 and 2
    ticket = list(top_result_main[0:6])
    print("--------LOTTO: Most Common Numbers--------\n\nYour Lotto ticket:\n")
    print(*ticket, sep=" - ")
    print("\nMore options:\n\n1) Return to Lotto number-picking menu\n2) Return to main menu\n\nType option number and press ENTER:", end=" ")
    while 1:
        option_choice = input()
        try:
            option_choice = int(option_choice)
        except:
            print("Not a valid selection, please choose a number from the list of options shown:", end=" ")
            continue
        if option_choice == 1:
            pick_numbers_menu(1)
        elif option_choice == 2:
            main_menu()
        else:
            print("Not a valid selection, please choose a number from the list of options shown:", end=" ")

def thunderball_top_balls():
    # Define lists for lottery numbers
    top_result_main = []
    top_result_bonus = []
    # Select Thunderball balls 1 to 6
    for x in thunderball_mode_sort:
        top_result_main.append(x)
    # Select Thunderball bonus ball
    for y in thunderball_bonus_mode_sort:
        top_result_bonus.append(y)
    ticket = list(top_result_main[0:7] + top_result_bonus[0:2])
    print("--------THUNDERBALL: Most Common Numbers--------\n\nYour Thunderball ticket:\n")

    print(*ticket, sep=" - ")
    print("\nMore options:\n\n1) Return to Thunderball number-picking menu\n2) Return to main menu\n\nType option number and press ENTER:", end=" ")
    while 1:
        option_choice = input()
        try:
            option_choice = int(option_choice)
        except:
            print("Not a valid selection, please choose a number from the list of options shown:", end=" ")
            continue
        if option_choice == 1:
            pick_numbers_menu(1)
        elif option_choice == 2:
            main_menu()
        else:
            print("Not a valid selection, please choose a number from the list of options shown:", end=" ")

#LEAST COMMON BALLS
def euromillions_least_balls():
    # Define lists for lottery numbers
    least_result_main = []
    least_result_bonus = []
    # Select EuroMillions balls 1 to 5
    for x in euro_least_sort:
        least_result_main.append(x)
    # Select EuroMillions bonus balls 1 and 2
    for y in euro_bonus_least_sort:
        least_result_bonus.append(y)
    ticket = list(least_result_main[0:6] + least_result_bonus[0:3])
    print("--------EUROMILLIONS: Least Common Numbers--------\n\nYour EuroMillions ticket:\n")
    print(*ticket, sep=" - ")
    print("\nMore options:\n\n1) Return to EuroMillions number-picking menu\n2) Return to main menu\n\nType option number and press ENTER:", end=" ")
    while 1:
        option_choice = input()
        try:
            option_choice = int(option_choice)
        except:
            print("Not a valid selection, please choose a number from the list of options shown:", end=" ")
            continue
        if option_choice == 1:
            pick_numbers_menu(1)
        elif option_choice == 2:
            main_menu()
        else:
            print("Not a valid selection, please choose a number from the list of options shown:", end=" ")

def lotto_least_balls():
    # Define lists for lottery numbers
    least_result_main = []
    # Select Lotto balls 1 to 6
    for x in lotto_least_sort:
        least_result_main.append(x)
    # Select EuroMillions bonus balls 1 and 2
    ticket = list(least_result_main[0:6])
    print("--------LOTTO: Least Common Numbers--------\n\nYour Lotto ticket:\n")
    print(*ticket, sep=" - ")
    print("\nMore options:\n\n1) Return to Lotto number-picking menu\n2) Return to main menu\n\nType option number and press ENTER:", end=" ")
    while 1:
        option_choice = input()
        try:
            option_choice = int(option_choice)
        except:
            print("Not a valid selection, please choose a number from the list of options shown:", end=" ")
            continue
        if option_choice == 1:
            pick_numbers_menu(1)
        elif option_choice == 2:
            main_menu()
        else:
            print("Not a valid selection, please choose a number from the list of options shown:", end=" ")

def thunderball_least_balls():
    # Define lists for lottery numbers
    least_result_main = []
    least_result_bonus = []
    # Select Thunderball balls 1 to 6
    for x in thunderball_mode_sort:
        least_result_main.append(x)
    # Select Thunderball bonus ball
    for y in thunderball_bonus_least_sort:
        least_result_bonus.append(y)
    ticket = list(least_result_main[0:7] + least_result_bonus[0:2])
    print("--------THUNDERBALL: Least Common Numbers--------\n\nYour Thunderball ticket:\n")
    print(*ticket, sep=" - ")
    print("\nMore options:\n\n1) Return to Thunderball number-picking menu\n2) Return to main menu\n\nType option number and press ENTER:", end=" ")
    while 1:
        option_choice = input()
        try:
            option_choice = int(option_choice)
        except:
            print("Not a valid selection, please choose a number from the list of options shown:", end=" ")
            continue
        if option_choice == 1:
            pick_numbers_menu(1)
        elif option_choice == 2:
            main_menu()
        else:
            print("Not a valid selection, please choose a number from the list of options shown:", end=" ")

def results_history(lottery_choice):
    clear_screen()
    if lottery_choice == 1:
        print(f"--------EUROMILLIONS DRAW HISTORY--------\n\nInformation from previous draws:\n")
        print(euro_history)
        esc = input("\nType 1 then ENTER to return to previous menu: ")
        if esc:
            lottery_menu(1)
    if lottery_choice == 2:
        print(f"--------LOTTO DRAW HISTORY--------\n\nInformation from previous draws:\n")
        print(lotto_history)
        esc = input("\nType 1 then ENTER to return to previous menu: ")
        if esc:
            lottery_menu(2)
    if lottery_choice == 3:
        print(f"--------LOTTO DRAW HISTORY--------\n\nInformation from previous draws:\n")
        print(thunderball_history)
        esc = input("\nType 1 then ENTER to return to previous menu: ")
        if esc:
            lottery_menu(3)

while 1:
    clear_screen()
    a = input("PRESS ANY KEY TO CONTINUE")
    if a:
        break
    break

main_menu()