init python:

    def defaultSortKey(fighter):
            return str.lower(fighter.Name)

    class EquipFighter(Action):
        def __init__(self, fighter, item):
            self._fighter = fighter
            self._item = item
            
        def get_sensitive(self):
            return (self._fighter.Equipment != None and self._fighter.Equipment.CanBeAdded(self._item))
            
        def __call__(self):
            if (self._fighter.Equipment != None and self._fighter.Equipment.CanBeAdded(self._item)):
                self._fighter.Equipment.Add(self._item)
                renpy.restart_interaction()

    class UnequipFighter(Action):
        def __init__(self, fighter, item):
            self._fighter = fighter
            self._item = item
            
        def __call__(self):
            if (self._fighter.Equipment != None and self._item in self._fighter.Equipment):
                self._fighter.Equipment.Remove(self._item)
                renpy.restart_interaction()

    class AddToInventory(Action):
        def __init__(self, inventory, item, quantity):
            self._inventory = inventory
            self._item = item
            self._quantity = int(quantity)
            
        def __call__(self):
            if (self._inventory != None and self._item != None and self._quantity > 0):
                self._inventory.AddItem(self._item, self._quantity)
                
    class RemoveFromInventory(Action):
        def __init__(self, inventory, item, quantity):
            self._inventory = inventory
            self._item = item
            self._quantity = int(quantity)
            
        def __call__(self):
            if (self._inventory != None and self._item != None and self._quantity > 0):
                self._inventory.RemoveItem(self._item, self._quantity)
                
    

    class RemoveFromList(Action):
        def __init__(self, list, item):
            self._list = list
            self._item = item
            
        def __call__(self):
            if (self._list != None):
                self._list.remove(self._item)
                renpy.restart_interaction()
                
    class AddToList(Action):
        def __init__(self, list, item, duplicates=True):
            self._list = list
            self._item = item
            self._duplicates = duplicates
            
        def __call__(self):
            if (self._list != None):
                if self._duplicates == True or ((self._item in self._list) == False):
                    self._list.append(self._item)
                    renpy.restart_interaction()
           
    # Returns a tuple of (categoryList, categoryDict)
    # categoryList is a simple list of strings which are the ordered names of categories to display
    # categoryDict is a dict mapping those categories to lists of (name, quantity, item) tuples.
    #   name is the string name of the item
    #   quantity is the integer number of that item that are available
    #   item is the BattleItem class instance for that item.
    def GetCategorisedEquipment(equipment, categories, includeOther):

        catDict = {}
        otherEquipment = equipment.GetItems()
        cats = categories[:]
        
        for c in categories:
            catDict[c] = []
            
            for e in [x for x in equipment.GetItems() if c in x[2].Attributes]:
                otherEquipment.remove(e)
                catDict[c].append(e)

        if includeOther and len(otherEquipment) > 0:
            cats.append("other")
            catDict["other"] = otherEquipment
            
        return (cats, catDict)


define EQUIP_ADJUSTMENT = ui.adjustment()
define FIGHTER_EQUIP_ADJUSTMENT = ui.adjustment()
define PARTY_INVENTORY_ADJUSTMENT = ui.adjustment()
define SHOP_INVENTORY_ADJUSTMENT = ui.adjustment()

# The 'stats' screen shows a fighter's portrait (if available) and a selection of stats.
# Parameters:
# - testEquip
#       If set to a BattleEquipment instance, will show the changes to the fighter's
#       current stats that equipping that equipment would make.
# - testRemove
#       If set to a BattleEquipment instance, will show the changes to the fighter's
#       current stats that unequipping that equipment would make.
# - fighter
#       The fighter for which to display stats
# - stats
#       A list of stats (by string name) to show.
#
# This screen is used inside the equip_select, party_select and rpg_shop screens to
# display the stats of party members and the effects certain pieces of 
# equipment may have.

screen stats:
    tag battle_stats
    default fighter = None
    default stats = ['Attack', 'Defence', 'Health', 'Speed']
    default testEquip = None
    default testRemove = None
    
    frame:
        background None
        xminimum 1.0
        
        hbox:
            spacing 5
            if fighter != None and fighter.Portrait != None:
                frame:
                    add fighter.Portrait
            vbox:
                yalign 0.5
                for stat in stats:
                    python:
                        statValue = getattr(fighter.Stats, stat)
                        oldStatValue = statValue
                        diff = 0
                        
                        if testEquip != None and isinstance(testEquip, BattleEquipment):
                            statValue = testEquip.OnRetrieveStat(stat, statValue)
                            
                        if testRemove != None and isinstance(testEquip, BattleEquipment):
                            fighter.Equipment.Remove(testRemove)
                            statValue = getattr(fighter.Stats, stat)
                            fighter.Equipment.Add(testRemove)
                        
                        statValue = int(statValue)
                        oldStatValue = int(oldStatValue)
                        
                        diff = statValue - oldStatValue
                        
                    if diff == 0:
                        text "[stat]: [statValue]"
                    elif diff > 0:
                        hbox:
                            text "[stat]: [oldStatValue] => "
                            text "[statValue]" color "#0A0"
                    else:
                        hbox:
                            text "[stat]: [oldStatValue] => "
                            text "[statValue]" color "#A00"

# The 'stats_popup' screen is used to display the stats screen in a popup window
# over the top of another screen.
# Parameters:
# - testEquip
#       If set to a BattleEquipment instance, will show the changes to the fighter's
#       current stats that equipping that equipment would make.
# - testRemove
#       If set to a BattleEquipment instance, will show the changes to the fighter's
#       current stats that unequipping that equipment would make.
# - fighter
#       The fighter for which to display stats
# - stats
#       A list of stats (by string name) to show.
# - xalign
#       The xalign to give the popup window
# - yalign
#       The yalign to give the popup window
#
# This screen is used in the party select screen to pop up the stats box when
# party members - or potential party members - are hovered.


screen stats_popup:
    tag battle_stats_popup
    default fighter = None
    default stats = ['Attack', 'Defence', 'Health', 'Speed']
    default testEquip = None
    default testRemove = None
    default xalign = 0.5
    default yalign = 0.5

    window:
        style "BattleMenuWindow"
        xalign xalign
        yalign yalign
        xminimum 300
        xmaximum 300
        
        use stats(fighter=fighter, stats=stats, testEquip=testEquip, testRemove=testRemove)


# The 'equip_select' screen is used to select equipment for a number of fighters
# from a list of available equipment.
# Parameters:
# - fighters
#       A list of the fighters to change the equipment of
# - equipment
#       A BattleInventory instance which contains the equipment to make available
# - categories
#       A list of categories into which to split the equipment - these must match up to
#       attributes set on the equipment instances (see engine-items.rpy, and equipment-demo.rpy
#       and assets.rpy in the demo code) and are case-sensitive, so be careful!
# - includeOther
#       Set to True if you want to make equipment which doesn't fit into one of the above
#       categories available in an 'other' category. Set to False is you don't want to
#       make that equipment available at all.
# - stats
#       A list of stats (by string name) to preview when equipment is hovered.

screen equip_select:
    tag battle_equip_select
    modal True
    
    default fighters = []
    default stats = ['Attack', 'Defence', 'Health', 'Speed']
    default categories = ['weapon', 'armour', 'helmet', 'shield']
    default openCategories = []
    default includeOther = True
    default index = 0
    default testEquip = None
    default testRemove = None
    default equipment = BattleInventory()
    
    python:
        xSize = int(config.screen_width * 0.9)
        ySize = int(config.screen_height * 0.9)
        current = fighters[index]
        
        # Get a list of categories and a dict of equipment sorted by category
        # (We have to get the list out even though we supply it because the 'other' category
        #  may or may not have been added.)
        cats, catDict = GetCategorisedEquipment(equipment, categories, includeOther)
        
        # Next filter each dict entry to only include items which are actually equipment.
        for cat in cats:
            catDict[cat] = filter(lambda x: isinstance(x[2], BattleEquipment), catDict[cat])
            
    window:
        style "BattleMenuWindow"
        
        xmaximum xSize
        xminimum xSize
        ymaximum ySize
        yminimum ySize
        
        # The left-and-right pick-fighter controls go at the top, then below that the
        # two columns with the equipment lists, then below that the 'Done' button.
        vbox:
            hbox:
                xminimum 1.0
                side "l c r":
                    
                    button:
                        style "BattleButton"
                        xalign 0.0
                        text "<<"
                        action SetScreenVariable("index", (index-1)%len(fighters))
                    
                    frame:
                        background None
                        xfill True
                        null
                    
                    button:
                        style "BattleButton"
                        xalign 1.0
                        text ">>"
                        action SetScreenVariable("index", (index+1)%len(fighters))
             
            # Current equipment/stats in the left column, available equipment in the right
            hbox:
                
                window:
                    xmaximum (xSize/2)
                    xalign 0.0
                    yalign 0.0
                    left_margin 5
                    background None
                    
                    vbox:
                        frame:
                            background None
                            yminimum 0.5
                            ymaximum 0.5
                            bottom_padding 10
                            vbox:
                                text "[current.Name]'s Equipment"
                                
                                side "c r":
                                    viewport:
                                        draggable True
                                        mousewheel True
                                        yadjustment FIGHTER_EQUIP_ADJUSTMENT
                                        
                                        vbox:
                                            for e in current.Equipment.All:
                                                hbox:
                                                    xfill True
                                                    text e.Name xfill True
                                                    button:
                                                        xalign 1.0
                                                        text "-"
                                                        action [SetScreenVariable("testRemove", None), UnequipFighter(current, e), AddToInventory(equipment, e, 1)]
                                                        hovered SetScreenVariable("testRemove", e)
                                                        unhovered SetScreenVariable("testRemove", None)
                                    vbar:
                                        style "l_vscrollbar"
                                        adjustment FIGHTER_EQUIP_ADJUSTMENT
                                                    
                        # Stats display
                        use stats(fighter=current, stats=stats, testEquip=testEquip, testRemove=testRemove)
                        
                window:
                    background None
                    
                    vbox:
                        text "Available Equipment"
                        
                        side "c r":
                            
                            viewport:
                                draggable True
                                mousewheel True
                                yadjustment EQUIP_ADJUSTMENT
                                
                                vbox:
                                    for c in cats:
                                        
                                        if c in openCategories:
                                            
                                            button:
                                                xalign 0.0
                                                xfill True
                                                text c.capitalize()
                                                action RemoveFromList(openCategories, c)
                                                
                                            for e in catDict[c]:
                                                python:
                                                    # Construct the string description of the item + quantity
                                                    equipText = e[0] + " (" + str(e[1]) + ")"
                                                    
                                                    # Count the number of hands an item requires so we can display it if necessary
                                                    hands = int(len(filter(lambda x: x=='hand', e[2].Attributes)))
                                                    
                                                    if hands > 0:
                                                        equipText = "("+str(hands)+"H) " + equipText
                                                hbox:
                                                    xfill True
                                                    text equipText xfill True
                                                    button:
                                                        xalign 1.0
                                                        text "+"
                                                        action [SetScreenVariable("testEquip", None), EquipFighter(current, e[2]), RemoveFromInventory(equipment, e[2], 1)]
                                                        hovered SetScreenVariable("testEquip", e[2])
                                                        unhovered SetScreenVariable("testEquip", None)
                                        else:
                                            button:
                                                xalign 0.0
                                                xfill True
                                                text c.capitalize()
                                                action AddToList(openCategories, c)
                            vbar:
                                style "l_vscrollbar"
                                adjustment EQUIP_ADJUSTMENT
            button:
                xalign 0.5
                text "Done"
                action [Hide("equip_select"), Return()]

# The 'party_select' screen is used to select a subset of available fighters
# to form a party.
# Parameters:
# - available
#       A list of fighters to choose from
# - party
#       A list of fighters in the existing party
# - required
#       A list of fighters who are required to be in the party and
#       cannot be removed
# - minSize
#       The minimum allowed party size
# - maxSize
#       The maximum allowed party size
# - stats
#       The stats (by string name) to show when previewing a fighter's stats
#       on mouseover.
# - listSort
#       An optional funtion to obtain a sorting key from a fighter instance.
#       This can be provided to change the way fighters are sorted - for example,
#       if you want to sort the available fighters by level, then set listSort to
#       a function which returns the fighter's level. By default, an alphabetical
#       sort is used.

screen party_select:
    tag battle_party_select
    modal True
    

    default available = []
    default party = []
    default required = []
    default minSize = 1
    default maxSize = 4
    default listSort = defaultSortKey
    default stats = ['Attack', 'Defence', 'Health', 'Speed']
    
    python:
        xSize = int(config.screen_width * 0.9)
        ySize = int(config.screen_height * 0.9)

        # First we convert all the lists into sets just in case -
        # we don't want to have a fighter who's both in the party
        # and also available to add to the party!
        
        availableSet = set(available)
        partySet = set(party)
        requiredSet = set(required)

        currentParty = requiredSet | partySet
        availableSet = availableSet - currentParty
        
        currentParty = sorted(currentParty, key=listSort)
        availableSet = sorted(availableSet, key=listSort)
        
        currentSize = len(currentParty)

    window:
        style "BattleMenuWindow"
        
        xmaximum xSize
        xminimum xSize
        ymaximum ySize
        yminimum ySize
        
        vbox:
            hbox:
            
                yfill True
            
                window:
                    xmaximum (xSize/2)
                    xalign 0.0
                    yalign 0.0
                    left_margin 5
                    background None
                    
                    vbox:
                        text "Current Party:"
                        frame:
                            background None
                            yminimum 0.5
                            ymaximum 0.5
                            top_padding 10
                            bottom_padding 10
                            
                            vbox:
                                for f in currentParty:
                                    
                                    python:
                                        name = f.Name
                                        if f in requiredSet:
                                            name = name + " (required)"
                                    
                                    hbox:
                                        xfill True
                                        
                                        text name xfill True xalign 0.0
                                        
                                        if ((f in requiredSet) == False) and (currentSize > minSize):
                                            button:
                                                xalign 1.0
                                                text ">>"
                                                action [RemoveFromList(party, f), AddToList(available, f), Hide("stats_popup")]
                                                hovered Show("stats_popup", fighter=f, stats=stats, xalign=0.8, yalign=0.5)
                                                unhovered Hide("stats_popup")
                                            

                window:
                    background None
                    yalign 0.0
                    
                    vbox:
                        text "Available Characters:"
                        frame:
                            background None
                            yminimum 0.5
                            ymaximum 0.5
                            top_padding 10
                            bottom_padding 10
                            
                            vbox:
                                for f in availableSet:
                                    hbox:
                                        
                                        spacing 5
                                        
                                        if (currentSize < maxSize):
                                        
                                            button:
                                                text "<<"
                                                action [RemoveFromList(available, f), AddToList(party, f), Hide("stats_popup")]
                                                hovered Show("stats_popup", fighter=f, stats=stats, xalign=0.2, yalign=0.5)
                                                unhovered Hide("stats_popup")
                                        
                                        text f.Name xfill True xalign 0.0 
                                        
                
            vbox:
                yalign 1.0
                xalign 0.5
                
                if (currentSize < minSize):
                    text "You must select at least [minSize] characters for your party."
                elif (currentSize > maxSize):
                    text "You can select no more than [maxSize] characters for your party."
                else:
                
                    button:
                        xalign 0.5
                        text "Done"
                        action [Hide("party_select"), Return(currentParty)]

# The 'rpg_shop' screen is used to display a buying and selling interface for items and equipment.
# Parameters:
# - categories
#       A list of categories into which to split the equipment - these must match up to
#       attributes set on the equipment instances (see engine-items.rpy, and equipment-demo.rpy
#       and assets.rpy in the demo code) and are case-sensitive, so be careful!
# - includeOther
#       Set to True if you want to make equipment which doesn't fit into one of the above
#       categories available in an 'other' category. Set to False is you don't want to
#       make that equipment available at all.
# - partyInventory
#       A BattleInventory instance which represents the current party inventory.
# - shopInventory
#       A BattleInventory instance which represents the items the shop has available to sell.
# - priceList
#       An RPGPriceList instance which describes the prices the shop sells and buys at.
# - currency
#       A string used to describe the unit of currency (default 'Gold').
# - money
#       An integer amount of money that the user has available to buy things with.
# - fighters
#       A list of fighters to make available for the stat-change preview (generally this will be
#       either your current party or your entire set of available fighters).
# - stats
#       A list of stats (by string name) to use for the stat preview.


screen rpg_shop:
    tag rpg_shop
    modal True
    
    # Params for fighter preview
    default fighters = []
    default index = 0
    default stats = ['Attack', 'Defence', 'Health', 'Speed']
    default testEquip = None
    
    # Params for equipment display
    default categories = ['weapon', 'armour', 'helmet', 'shield']
    default openPartyCategories = []
    default openShopCategories = []
    default includeOther = True
    
    # Params for equipment and price lists
    default partyInventory = BattleInventory()
    default shopInventory = BattleInventory()
    default priceList = RPGPriceList()
    
    # Params for party money
    default currency = "Gold"
    default money = 0
    
    python:
        xSize = int(config.screen_width * 0.9)
        ySize = int(config.screen_height * 0.9)
        current = fighters[index]
        money = int(max(money, 0))
        
        # Get a categorised list of store inventory
        partyCats, partyCatDict = GetCategorisedEquipment(partyInventory, categories, includeOther)
        shopCats, shopCatDict = GetCategorisedEquipment(shopInventory, categories, includeOther)

    window:
        style "BattleMenuWindow"
        
        xmaximum xSize
        xminimum xSize
        ymaximum ySize
        yminimum ySize
        
        # The party coffers goes first, then two columns of inventories, then after that the 'Done' button
        vbox:
            python:
                coffers = str(money) + " " + currency
                
            # party coffers
            text coffers xalign 0.5
            
            # two columns of inventories
            hbox:
                
                # First column: party inventory followed by fighter stat preview
                window:
                    xmaximum (xSize/2)
                    xalign 0.0
                    yalign 0.0
                    left_margin 5
                    background None
                    
                    vbox:
                        # party inventory
                        frame:
                            background None
                            yminimum 0.60
                            ymaximum 0.60
                            bottom_padding 10
                            vbox:
                                text "Party Inventory"
                                
                                side "c r":
                                    viewport:
                                        draggable True
                                        mousewheel True
                                        yadjustment PARTY_INVENTORY_ADJUSTMENT
                                        
                                        vbox:
                                            for c in partyCats:
                                        
                                                if c in openPartyCategories:
                                                    
                                                    button:
                                                        xalign 0.0
                                                        xfill True
                                                        text c.capitalize()
                                                        action RemoveFromList(openPartyCategories, c)
                                                        
                                                    for e in partyCatDict[c]:
                                                        
                                                        python:
                                                            # We're talking about the price for the player to sell his item, but we need to look
                                                            # for the price the shop will buy it for...
                                                            sellPrice = priceList.GetBuyPrice(e[2])
                                                            itemTitle = str(e[1]) + " x " + e[0]
                                                            if sellPrice != None:
                                                                sellPrice = int(sellPrice)
                                                                newMoney = money + sellPrice
                                                            else:
                                                                newMoney = money
                                                                sellPrice = ""
                                                        
                                                        hbox:
                                                            xfill True
                                                            text itemTitle xfill True
                                                            
                                                            hbox:
                                                                xalign 1.0
                                                                text str(sellPrice) xalign 1.0
                                                                
                                                                if priceList.CanBuy(e[2]):
                                                                    button:
                                                                        xalign 1.0
                                                                        text "Sell"
                                                                        action [SetScreenVariable("testEquip", None), SetScreenVariable("money", newMoney), RemoveFromInventory(partyInventory, e[2], 1), AddToInventory(shopInventory, e[2], 1)]
                                                                        hovered SetScreenVariable("testEquip", e[2])
                                                                        unhovered SetScreenVariable("testEquip", None)
                                                                else:
                                                                    button:
                                                                        xalign 1.0
                                                                        text "Sell"
                                                                        hovered SetScreenVariable("testEquip", e[2])
                                                                        unhovered SetScreenVariable("testEquip", None)

                                                else:
                                                    button:
                                                        xalign 0.0
                                                        xfill True
                                                        text c.capitalize()
                                                        action AddToList(openPartyCategories, c)
                                    vbar:
                                        style "l_vscrollbar"
                                        adjustment PARTY_INVENTORY_ADJUSTMENT
                                                    
                        # Stats preview
                        use stats(fighter=current, stats=stats, testEquip=testEquip)
                            
                        hbox:
                            xfill True
                            
                            button:
                                style "BattleButton"
                                xalign 0.0
                                text "<<"
                                action SetScreenVariable("index", (index-1)%len(fighters))
                            
                            button:
                                style "BattleButton"
                                xalign 1.0
                                text ">>"
                                action SetScreenVariable("index", (index+1)%len(fighters))
                                
                        
                        
                window:
                    background None
                    
                    vbox:
                        text "Available To Buy"
                        
                        side "c r":
                            
                            viewport:
                                draggable True
                                mousewheel True
                                yadjustment SHOP_INVENTORY_ADJUSTMENT
                                
                                vbox:
                                    for c in shopCats:
                                        
                                        if c in openShopCategories:
                                            
                                            button:
                                                xalign 0.0
                                                xfill True
                                                text c.capitalize()
                                                action RemoveFromList(openShopCategories, c)
                                                
                                            for e in shopCatDict[c]:
                                                
                                                python:
                                                    # We're talking about the price for the player to buy the item, but we need to look
                                                    # for the price the shop will sell it for...
                                                    buyPrice = priceList.GetSellPrice(e[2])
                                                    itemTitle = str(e[1]) + "x " + e[0]
                                                    if (buyPrice != None):
                                                        buyPrice = int(buyPrice)
                                                        newMoney = money - buyPrice
                                                    else:
                                                        newMoney = money
                                                        buyPrice = ""
                                                
                                                hbox:
                                                    xfill True
                                                    text itemTitle xfill True
                                                    
                                                    hbox:
                                                        xalign 1.0
                                                        text str(buyPrice) xfill True xalign 1.0
                                                        if priceList.CanSell(e[2]) and newMoney >= 0:
                                                            button:
                                                                xalign 1.0
                                                                text "Buy"
                                                                
                                                                action [SetScreenVariable("testEquip", None), SetScreenVariable("money", newMoney), AddToInventory(partyInventory, e[2], 1), RemoveFromInventory(shopInventory, e[2], 1), AddToList(openPartyCategories, c, False)]
                                                                hovered SetScreenVariable("testEquip", e[2])
                                                                unhovered SetScreenVariable("testEquip", None)
                                                        else:
                                                            button:
                                                                xalign 1.0
                                                                text "Buy"
                                                                
                                                                hovered SetScreenVariable("testEquip", e[2])
                                                                unhovered SetScreenVariable("testEquip", None)

                                        else:
                                            button:
                                                xalign 0.0
                                                xfill True
                                                text c.capitalize()
                                                action AddToList(openShopCategories, c)
                            vbar:
                                style "l_vscrollbar"
                                adjustment SHOP_INVENTORY_ADJUSTMENT
                                
            
            button:
                xalign 0.5
                text "Done"
                action [Hide("rpg_shop"), Return(money)]