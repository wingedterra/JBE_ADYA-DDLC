label party_screen_demo:

    
    # The Party Screen demo does not assume any particular foreknowledge, but concentrates on the 
    # screen itself and not the battle-engine classes used in it; setting up fighters is covered
    # in other tutorials.
    
    # First, just to get some fighters to play with, we'll set up a few basic fighters:
    
    python:
        
        # Here we're using the 'portrait' parameter to define a headshot of the character for use in UIs
        a = PlayerFighter("Simon", portrait="gfx/head1.png", Speed=10, Move=5, Attack=15, Defence=3, Health=10)
        b = PlayerFighter("Cybil", portrait="gfx/head2.png", Speed=11, Move=5, Attack=14, Defence=3, Health=10)
        c = PlayerFighter("Robert", portrait="gfx/head3.png", Speed=12, Move=5, Attack=13, Defence=3, Health=10)
        d = PlayerFighter("Camille", portrait="gfx/head4.png", Speed=13, Move=6, Attack=12, Defence=3, Health=10)
        e = PlayerFighter("Edward", portrait="gfx/head5.png", Speed=14, Move=6, Attack=11, Defence=3, Health=10)

    # The first way that you can call the party screen is to simply use a Python command, which will output the
    # new party as the return from the screen.
    # The parameters to the screen are detailed in battle-screens.rpy, but in brief:
    # - available: the list of fighters who can join the party
    # - required: the list of fighters who cannot be removed from the party
    # - minSize: the minimum party size
    # - maxSize: the maximum party size
    $ party = renpy.call_screen("party_select", available=[a, b, c, d, e], required=[a], minSize=2, maxSize=4)

    # Just to display it, we'll get all the fighter names
    python:
        partyNames = []
        for f in party:
            partyNames.append(f.Name)
        x = len(partyNames) - 1
        partyString = ", ".join(partyNames[:x]) + " and " + partyNames[x]
        
    "[partyString] went adventuring one day, had some adventures, then stopped at a tavern to re-organise..."

    # If you prefer, you can call the screen in Ren'PyScript:
    # (Here we're passing in the party parameter to set the initial line-up to the same as the previous
    # screen's choices.)
    call screen party_select(party=party, available=[a, b, c, d, e], minSize=2, maxSize=4)

    # You'll have to pull the party list out of the _return variable like this, though.
    $ party=_return
    
    python:
        partyNames = []
        for f in party:
            partyNames.append(f.Name)
        x = len(partyNames) - 1
        partyString = ", ".join(partyNames[:x]) + " and " + partyNames[x]
        
    "[partyString] continued on to fight the evil lord in his dark dungeon."
    
    # Once you've organised your party, rather than setting up each fighter from scratch at the beginning of the
    # next battle, you can just do something like this:
    
    # battle.AddFaction('Player', playerFaction=True)
    # for f in party:
    #   battle.AddFighter(f)
    
    # ... of course, you'll still need some bad guys!


    jump start
    
    
label shop_screen_demo:


    python:
        
        # The shop's inventory is stored in a BattleInventory instance - same as the player's
        # party inventory.
        shopInventory = BattleInventory()
        
        # To add a quantity of equipment, call the 'AddItem' method with two parameters -
        # the item itself, and the number to add.
        shopInventory.AddItem(Library.Equipment.Knife, 4)
        shopInventory.AddItem(Library.Equipment.ShortSword, 2)
        
        # If you don't specify a quantity, it will default to 1.
        shopInventory.AddItem(Library.Equipment.Sword)
        shopInventory.AddItem(Library.Equipment.Spear)
        shopInventory.AddItem(Library.Equipment.Halberd)
        shopInventory.AddItem(Library.Equipment.LeatherArmour, 3)
        shopInventory.AddItem(Library.Equipment.Chainmail, 2)
        shopInventory.AddItem(Library.Equipment.ScaleMail)
        shopInventory.AddItem(Library.Equipment.RoundShield)
        shopInventory.AddItem(Library.Equipment.Scutum)
        shopInventory.AddItem(Library.Equipment.FeltHat, 4)
        shopInventory.AddItem(Library.Equipment.LeatherHelmet)
        shopInventory.AddItem(Library.Equipment.SteelHelmet)
        
        # Adding a non-equipment item won't cause a problem, it just
        # won't show up in the equip screen
        shopInventory.AddItem(Library.Items.Potion, 10)
        
        # You'll also need an inventory for the party (it'll start off empty here)
        # and a variable to track available money.
        
        partyInventory = BattleInventory()
        money = 1000
        
        # We need a couple of fighters to preview items' stat gains against...
        camille = PlayerFighter("Camille", portrait="gfx/head4.png", Speed=13, Move=6, Attack=12, Defence=3, Health=10)
        edward = PlayerFighter("Edward", portrait="gfx/head5.png", Speed=14, Move=6, Attack=11, Defence=3, Health=10)

        # Just like with the party select screen, we can call the shop screen either in Python:
        # The screen parameters are detailed in battle-screens.rpy, but in brief:
        # - partyInventory: a BattleInventory instance for the party's inventory
        # - shopInventory: a BattleInventory instance for the shop's inventory
        # - currency: the name of the currency being used
        # - money: the money available to spend
        # - fighters: a list of fighters to use for previews
        # the screen returns the unspent money at the end of the shopping session.
        
        money = renpy.call_screen("rpg_shop", partyInventory=partyInventory, shopInventory=shopInventory, currency="Gold", money=money, fighters=[camille, edward])
        
        # Let's go through all the stuff we bought:
        invItems = []
        for i in partyInventory.GetItems():
            # i[0] is the name
            # i[1] is the quantity
            # i[2] is the item instance (in case you need it)
            itemString = str(i[1]) + " " + i[0]
            if i[1] > 1:
                itemString = itemString + "s"
            invItems.append(itemString)
        invString = ", ".join(invItems)
        
    "Camille and Edward bought: [invString]"
    
    python:
        
        # Next we'll go into a specialist shop which only buys or sells amulets:
        
        amulets = BattleInventory()
        amulets.AddItem(Library.Equipment.AttackAmulet, 5)
        amulets.AddItem(Library.Equipment.HealthAmulet, 5)
        amulets.AddItem(Library.Items.Potion, 10)
        
        # An optional parameter to the screen is a pricelist, which determines how much a shop charges
        # and how much a shop pays for particular items. By default the price is determined by the 'cost'
        # property of the item itself (see assets.rpy).
        # The 'sellExclusive' and 'buyExclusive' parameters determine whether the shop will only sell items
        # with values entered explicitly into the price list, or only buy items explicitly entered.
        # Here we're only buying or selling amulets so we set them both to True; the default is False. 
        priceList = RPGPriceList(sellExclusive=True, buyExclusive=True)

        # We add a sell price - the price that the shop will sell the item at - by passing in the item's
        # class instance and a value
        priceList.SetSellPrice(Library.Equipment.AttackAmulet, 500)
        priceList.SetSellPrice(Library.Equipment.HealthAmulet, 450)
        
        # Similarly we set the price that the shop will buy the player's items for.
        priceList.SetBuyPrice(Library.Equipment.AttackAmulet, 300)
        priceList.SetBuyPrice(Library.Equipment.HealthAmulet, 250)

    # As with the party select screen, you can opt to use Ren'PyScript to call the screen, but you have to
    # get the unspent money out via the _return variable.
    # To use the price list we're simply setting the priceList param to the screen.
    # If you don't set this param, then the shop will default to a pricelist which buys and sells anything
    # at the default price defined on the item itself, and buys for half the sale price.
    call screen rpg_shop(partyInventory=partyInventory, shopInventory=amulets, currency="Gold", money=money, fighters=[camille, edward], priceList=priceList)

    $ money = _return
    
    jump start

