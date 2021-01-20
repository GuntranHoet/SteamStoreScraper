import requests

from random import *
from bs4 import BeautifulSoup # https://www.crummy.com/software/BeautifulSoup/bs4/doc/

##########################################################################

BASE_URL = "https://store.steampowered.com/app/"

##########################################################################

def scrape(appID):
    print("")

    pageUrl = BASE_URL + str(appID)
    print("> pageUrl=", pageUrl)
    page = requests.get(pageUrl)
    if ( page == None ):
        print("> loading", pageUrl, ": FAILED (page not found!)")
        return
    soup = BeautifulSoup(page.content, "html.parser")

    homeTest = soup.find(class_="home_page_content")
    if ( homeTest != None ):
        print("> loading", pageUrl, ": FAILED (home page redirect)")
        return
    else:
        print("> loading", pageUrl, ": OK")

    #########################################
    # \/ actual page scraping below here \/ #
    #########################################

    ### general

    gamePurchaseArea = soup.find(id="game_area_purchase")
    if ( gamePurchaseArea == None ):
        print("> ERROR:", "no game purchase area found")
        return

    # generic game item wrapper
    gameWrapperArr = gamePurchaseArea.find_all(class_="game_area_purchase_game_wrapper")
    if ( gameWrapperArr == None ):
        print("> WARNING:", "no game wrappers found")
    else:
        print("> game wrappers:", len(gameWrapperArr))

    # old games or free-to-play games might use this item wrapper instead
    oldFreePlayWrapper = gamePurchaseArea.find_all(class_="game_area_purchase_game")
    if ( oldFreePlayWrapper != None ):
        gameWrapperArr = gameWrapperArr + oldFreePlayWrapper
        print("> old free wrapper:", len(oldFreePlayWrapper), "additional free (old) wrapper(s) found.")

    if ( gameWrapperArr == None or len(gameWrapperArr) == 0):
        print("> ERROR:", "Absolutely NO game wrappers found !")
        return

    ### per game wrapper data

    for wrapper in gameWrapperArr:
        itemName = wrapper.find('h1')
        if ( itemName != None ):
            itemNameText = itemName.text.strip()
            print("")
            print( "# Item:", itemNameText )
        
        purchasePrice = wrapper.find(class_="game_purchase_price")
        if ( purchasePrice != None ):
            purchasePriceText = purchasePrice.text.strip()
            print( "  price:", purchasePriceText )
        
        originalPrice = wrapper.find(class_="discount_original_price")
        if ( originalPrice != None ):
            originalPriceText = originalPrice.text.strip()
            print( "  original:", originalPriceText )
        
        discountPct = wrapper.find(class_="discount_pct")
        if ( discountPct != None ):
            discountPctText = discountPct.text.strip()
            print( "  discount:", discountPctText )
        
        bundleDiscountPct = wrapper.find(class_="bundle_base_discount")
        if ( bundleDiscountPct != None ):
            bundleDiscountPctText = bundleDiscountPct.text.strip()
            print( "  bundle discount:", bundleDiscountPctText )
        
        finalPrice = wrapper.find(class_="discount_final_price")
        if ( finalPrice != None ):
            finalPriceText = finalPrice.text.strip()
            print( "  final:", finalPriceText )
        
        countdown = wrapper.find(class_="game_purchase_discount_countdown")
        if ( countdown != None ):
            countdownText = countdown.text.strip()
            span = countdown.find("span")
            if ( span != None ):
                countdownText = span.text.strip()
                print( "  countdown:", countdownText )
            else:
                print( "  countdown:", countdownText )
        
        ### This does not work since the options only appear once the dropdown has
        ### been clicked on. It's controlled by a javascript.
        #dropdown = wrapper.find(class_="game_area_purchase_game_dropdown_selection")
        #if ( dropdown != None ):
        #    #dropdownText = dropdown.text.strip()
        #    #print( "  dropdown:", dropdownText )
        #    dropOptionsArr = dropdown.find_all("game_area_purchase_game_dropdown_menu_item_text")
        #    if ( dropOptionsArr != None ):
        #        print( "  dropdown:", len(dropOptionsArr), "options:" )
        #        for option in dropOptionsArr:
        #            optionText = option.text.strip()
        #            print( "    price option:", optionText )

            
    ### DLC area

    print("")
    dlcArea = gamePurchaseArea.find(class_="game_area_dlc_list")
    if ( dlcArea == None ):
        print("> WARNING:", "no DLC list found")
        return
    
    dlcWrapperArr = dlcArea.find_all(class_="game_area_dlc_row")
    if ( dlcWrapperArr != None ):
        print( "> dlc packs:", len(dlcWrapperArr) )
    else:
        print("> ERROR:", "no DLC packs found!")

    ### per dlc wrapper data

    for wrapper in dlcWrapperArr:
        print("")

        itemName = wrapper.find(class_="game_area_dlc_name")
        if ( itemName != None ):
            itemNameText = itemName.text.strip()
            print("# dlc item:", itemNameText)

        itemPrice = wrapper.find(class_="game_area_dlc_price")
        if ( itemPrice != None ):
            itemPriceText = itemPrice.text.strip()
            print("# dlc price:", itemPriceText)
        

    
##########################################################################

### CORE ###

if True:
    #scrape(1410710) # https://store.steampowered.com/app/1410710/Democracy_4/
    #scrape(630) # https://store.steampowered.com/app/630/Alien_Swarm/
    scrape(548430) # https://store.steampowered.com/app/548430/Deep_Rock_Galactic/
    #scrape(1016920) # https://store.steampowered.com/app/1016920/Unrailed/
    #scrape(397540) # https://store.steampowered.com/app/397540/Borderlands_3/
    #scrape(230410) # https://store.steampowered.com/app/230410/Warframe/
    #scrape(489830) # https://store.steampowered.com/app/489830/The_Elder_Scrolls_V_Skyrim_Special_Edition/

if False:
    i = 0
    while ( i < 10 ):
        i += 1
        r = randint(0, 1000000)
        scrape(r)