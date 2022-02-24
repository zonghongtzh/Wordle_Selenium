import nltk
import random
from utils import * 
from Scraper import * 

# set up 
invalid_words_path = os.path.join(utils.mypath, 'invalid_words.json')
invalid_words = utils.open_json(invalid_words_path)
word_list = list(set([w.lower() for w in nltk.corpus.words.words() if len(w) == 5])) # big corpus
word_list = [word for word in word_list if word not in invalid_words]

# initialize
attempt = 'house' # first guess
outcome = '-----'
count = 0
correct_letters = []
wrong_letters = []
incorrect_position = {
    0: [],
    1: [],
    2: [],
    3: [],
    4: []
}


########## Enter page ##########
# selenium 
url = 'https://www.powerlanguage.co.uk/wordle/'
scrape.browser.get(url)

# click x button (right click -> copy -> copy JS path)
x_selector = 'return document.querySelector("body > game-app").shadowRoot.querySelector("#game > game-modal").shadowRoot.querySelector("div > div > div > game-icon").shadowRoot.querySelector("svg > path")'
x_element = scrape.browser.execute_script(x_selector)
while True:
    try:
        x_element.click()
        break
    except:
        time.sleep(1)
        
        
########## Selectors #########
# keyboard
keyboard_selector = 'return document.querySelector("body > game-app").shadowRoot.querySelector("#game > game-keyboard").shadowRoot.querySelector("#keyboard")'
keyboard_elems = {
    i.text: i 
    for i in scrape.browser.execute_script(keyboard_selector).find_elements_by_xpath(".//*")
}

# outcomes (each row)
outcome_selector = 'return document.querySelector("body > game-app").shadowRoot.querySelector("#board")'
outcome_elems = {
    0 : 'return document.querySelector("body > game-app").shadowRoot.querySelector("#board > game-row:nth-child(1)").shadowRoot.querySelector("div")',
    1 : 'return document.querySelector("body > game-app").shadowRoot.querySelector("#board > game-row:nth-child(2)").shadowRoot.querySelector("div")',
    2 : 'return document.querySelector("body > game-app").shadowRoot.querySelector("#board > game-row:nth-child(3)").shadowRoot.querySelector("div")',
    3 : 'return document.querySelector("body > game-app").shadowRoot.querySelector("#board > game-row:nth-child(4)").shadowRoot.querySelector("div")',
    4 : 'return document.querySelector("body > game-app").shadowRoot.querySelector("#board > game-row:nth-child(5)").shadowRoot.querySelector("div")',
    5 : 'return document.querySelector("body > game-app").shadowRoot.querySelector("#board > game-row:nth-child(6)").shadowRoot.querySelector("div")',
}

# alerts 
not_in_list_selector = 'return document.querySelector("body > game-app").shadowRoot.querySelector("#game-toaster")'

########## Attempt ##########
while (outcome != 'GGGGG') & (count < 6):

    # guess
    print(f'Attempt: {attempt}')

    # typing in guess
    for letter in attempt:
        u_letter = letter.upper()
        while True:
            try:
                keyboard_elems[u_letter].click()
                break
            except:
                time.sleep(1)

    keyboard_elems['ENTER'].click()
    
    # alert if not in list -> store invalid
    check_not_in_list = scrape.browser.execute_script(not_in_list_selector).find_elements_by_xpath(".//*")
    if len(check_not_in_list) != 0:
        invalid_words.append(attempt)
        utils.save_json(invalid_words, invalid_words_path)

        # backspace in wordle
        for i in range(5):
            while True:
                try:
                    keyboard_elems[''].click() # backspace
                    break
                except:
                    time.sleep(1)
        
        # check if notification is still on 
        while len(check_not_in_list) != 0:
            time.sleep(1)
            check_not_in_list = scrape.browser.execute_script(not_in_list_selector).find_elements_by_xpath(".//*")
                
        # reattempt
        word_list.remove(attempt)
        attempt = random.choice(word_list)
        continue

    # fetching outcome
    time.sleep(5) # wait time for outcome to load 
    results = [i.get_attribute('evaluation') for i in scrape.browser.execute_script(outcome_elems[count]).find_elements_by_xpath(".//*")]
    outcome_list = []
    for result in results:
        if result == 'absent':
            outcome_list.append('-')
        elif result == 'present':
            outcome_list.append('Y')
        elif result == 'correct':
            outcome_list.append('G')

    outcome = ''.join(outcome_list)
    print(f'Outcome: {outcome}')
    
    # creating regex to search corpus -> correct letters + incorrect positions 
    correct_letters = correct_letters + [attempt[i] for i in range(len(outcome)) if outcome[i] == 'G']
    correct_regex = [attempt[i] if outcome[i] == 'G' else '\w' for i in range(len(outcome))] # e.g. 'e\w\w\w\w' when attempting 'entry' for 'earth' answer
    
    # factoring in incorrect positions -> e.g. after this: 'e\w[^t][^r]\w' when attempting 'entry' for 'earth' answer 'G-YY-' 
    for x in range(len(outcome)):
        if outcome[x] == 'G':
            continue    
    
        if outcome[x] == 'Y':
            incorrect_position[x].append(attempt[x]) # append to dictionary

        if len(incorrect_position[x]) > 0:
            exclude = ''.join(set(incorrect_position[x])) # join all incorrectly positioned letters
            exclude_str = f'[^{exclude}]'
            correct_regex[x] = exclude_str
            
    correct_regex_search = ''.join(correct_regex).replace('-', '\w') 
    
    # second priority 
    wrong_letters = wrong_letters + [attempt[i] for i in range(len(outcome)) if outcome[i] == '-'] # bag of letters that are not in word
    wrong_letters = list(set(wrong_letters)) # e.g. ['n', 'y'] when guessing 'entry' for 'earth' answer
    wrong_letters = [wrong_letter for wrong_letter in wrong_letters if wrong_letter not in correct_letters]
    
    # third priority 
    present_letters = utils.flatten_list(incorrect_position.values()) # use incorrect_position dict to derive letters that are present but not in right position # e.g. ['t', 'r'] when guessing 'entry' for 'earth' answer
    
    # filtering 
    word_list = [word for word in word_list if re.search(correct_regex_search, word)] # lock in correct position + remove incorrect position
    word_list = [word for word in word_list if any([letter in word for letter in wrong_letters]) == False] # remove wrong eltters
    word_list = [word for word in word_list if all([letter in word for letter in present_letters]) == True] # remove words not containing all present letters 
    
    # selcting next word
    word_list.sort()
    word_list.sort(key = lambda x: len(set(x)), reverse = True)
    print('Remaining', word_list[:5], len(word_list))
    attempt = random.choice(word_list) # select most differentiated letters 
    count += 1
    

