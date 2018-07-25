init python:
    
    top_bar = Frame('gfx/top_bar.png', 7, 8)
    
    style.vscrollbar.top_bar = top_bar
    style.vscrollbar.bottom_bar = top_bar
    style.vscrollbar.thumb = 'gfx/thumb.png'
    style.vscrollbar.xminimum = 14
    style.vscrollbar.xmaximum = 14


label equip_demo:
    
    nvl clear
    
    # The Equipment Demo assumes that you've already read and understood the comments in
    # the Active Demo, and will not repeat those concepts. Only new things are commented in this
    # demo.
    
    demo "In the following equipment-selection screen, use the top-left and top-right '<<' and '>>' buttons
        to select a fighter to equip, add items from the available equipment by clicking on them in the 
        right-hand list, and remove items by clicking on them in the left hand fighter-equipment list."
    demo "At the bottom-left, the fighter's stats will reflect the changes you've made to his equipment.
        Press 'Done' when you're happy with your whole party's equipment."
    demo "Bob has been set up so that he can only use what he can carry in two hands; a sword or a normal shield
        will take one hand, but a spear or a halberd - or a scutum, a very large shield - will take two."
    demo "Geoff has no hand restrictions, so he just has the default limit of one weapon, one shield, one armour,
        and one helmet. Amulets don't have any kind of 'type' attribute, so they are not limited."
    demo "(Obviously the ideal would be to change the sprites based on their equipment, but for now that's
        not considered.)"

    # This time, we're going to set up a few fighters we're going to keep through more than one battle.
    # So we set the fighters up before the battle - none of the fighter-setup stuff requires the battle to
    # be started already.
    
    # This also means that we can re-use the same Fighter instances over and over again in successive
    # battles - we don't have to create them all over again each time.
    
    python:
        
        
        # Create 'bob' fighter
        bobSprite = BattleSprite('bob', anchor=(0.5, 0.75), placeMark=(0,-100))
        # We're setting the 'portrait' property here, which is the image intended for use when the fighter is seen out-of-battle.
        # Think of the portraits you see in JRPGs in the party menus, for example. In this demo they're shown in the 
        # fighter-equip screen's stats box.
        bob = PlayerFighter("Bob", Speed=11, Attack=20, Defence=20, sprite=bobSprite, portrait='bob portrait') 

        # Register Bob's skills
        bob.RegisterSkill(Library.Skills.SwordAttack)
        bob.RegisterSkill(Library.Skills.Skip)
        
        # We give Bob a new skill that we've not used before - the Item skill - which will allow him to
        # use items on the field of battle.
        bob.RegisterSkill(Library.Skills.Item)
        
        # We'll also override his default equipment slot - which would allow him to equip as much of
        # anything as he liked - with one which restricts him to stuff he can wear or hold in two hands.
        
        # The HandedFighterEquipment allows - by default - a fighter to equip a maximum of 1 weapon,
        # 1 armour, 1 helmet, 1 shield and any number of other items. On top of this, some equipment 
        # requires a certain number of hands to hold it, and a fighter can only carry equipment he can
        # hold in two hands.
        bob.Equipment = HandedFighterEquipment()
        
        # By default we won't give Bob any equipment, but we'll let the player select some for him later.
        
        # Create a 'geoff' fighter
        geoffSprite = BattleSprite('geoff', anchor=(0.5, 0.8), placeMark=(0,-100))
        geoff = PlayerFighter("Geoff", Speed=13, Attack=7, Defence=10, MP=20, sprite=geoffSprite, portrait='geoff portrait')
        geoff.RegisterSkill(Library.Skills.SwordAttack)
        geoff.RegisterSkill(Library.Skills.Skip)
        geoff.RegisterSkill(Library.Skills.Fire1)
        geoff.RegisterSkill(Library.Skills.Water1)
        geoff.RegisterSkill(Library.Skills.Earth1)
        geoff.RegisterSkill(Library.Skills.Item)
 
        # By default, a fighter gets an Equipment slot of the 'FighterEquipment' class. If you want to alter the
        # limits, you could create a new one with the limits you want to impose. The following line actually
        # just recreates the default, so removing it won't change anything, but altering it will change the amount
        # of certain types of thing that Geoff can carry.
        # Equipment without a type - like the amulets in the equipment list later on - won't be limited; a fighter
        # can carry as much of it as they like.
        # (Bear in mind that these labels are case-sensitive, and must match up with the attributes placed on the
        #  equipment itself in order to function - see engine-items.rpy and assets.rpy.)
        geoff.Equipment = FighterEquipment(limits={'weapon':1, 'armour':1, 'helmet':1, 'shield':1})
        
        # We'll also create a single inventory that we'll give both fighters access to, and add a few items.
        
        # First, set up a normal inventory
        inv = BattleInventory()
        
        # Next, add some items.
        # First, 5 health potions.
        inv.AddItem(Library.Items.Potion, 5)
        
        # Lastly, we'll give both fighters access to the same inventory.
        bob.Inventory = inv
        geoff.Inventory = inv
        
        
        # Now we've set up our fighters, we'll need to let the player select equipment. This is just
        # a basic equipment-selection screen, but by using the same functions, you can create whatever
        # kind of equipment-selection screens you want.
        
        party = [bob, geoff]
        
        # Here we set up a BattleInventory object, which means we need to add quantities of items to it
        # in order to build up the available equipment.
        equipment = BattleInventory()
        
        # To add a quantity of equipment, call the 'AddItem' method with two parameters -
        # the item itself, and the number to add.
        equipment.AddItem(Library.Equipment.Knife, 4)
        equipment.AddItem(Library.Equipment.ShortSword, 2)
        
        # If you don't specify a quantity, it will default to 1.
        equipment.AddItem(Library.Equipment.Sword)
        equipment.AddItem(Library.Equipment.Spear)
        equipment.AddItem(Library.Equipment.Halberd)
        equipment.AddItem(Library.Equipment.LeatherArmour, 3)
        equipment.AddItem(Library.Equipment.Chainmail, 2)
        equipment.AddItem(Library.Equipment.ScaleMail)
        equipment.AddItem(Library.Equipment.RoundShield)
        equipment.AddItem(Library.Equipment.Scutum)
        equipment.AddItem(Library.Equipment.FeltHat, 4)
        equipment.AddItem(Library.Equipment.LeatherHelmet)
        equipment.AddItem(Library.Equipment.SteelHelmet)
        equipment.AddItem(Library.Equipment.AttackAmulet)
        equipment.AddItem(Library.Equipment.HealthAmulet)
        
        # Adding a non-equipment item won't cause a problem, it just
        # won't show up in the equip screen
        equipment.AddItem(Library.Items.Potion)
        
    # Here we drop back into Ren'PyScript and show the 'equip_select' screen,
    # which allows the player to select equipment from the provided list.
    # The two required parameters are 'fighters' (a list of the fighter entities
    # that can be equipped at this time) and 'equipment' (a list of available
    # equipment items).
    # Optionally you can also pass in 'stats' (a list of stat names to display
    # in the stats box), 'categories' (a list of categories equipment is 
    # divded into in the right panel, matching the attributes set on the
    # equipment - see engine-items.rpy) and 'includeOther' (a True/False value
    # which determines whether to only allow the user to select equpiment which
    # is in one of the specified categories, or to add an 'other' category which
    # contains all the equipment which doesn't fit into one of the specified ones.
    show screen equip_select(fighters=[bob, geoff], equipment=equipment)
    
    pause

    python:
        
        
        # Now we've finished selecting equipment, we just start the battle as normal, using the Fighters
        # we previously set up rather than setting new ones up just for this battle. Like this, we can use the
        # same fighters in may successive battles!
        
        battle = Battle(ActiveSchema())
        battle.SetBattlefield(SimpleBattlefield(BattlefieldSprite('bg woodland')))
        
        battle.AddFaction("Player", playerFaction=True)
        battle.AddFighter(bob)
        battle.AddFighter(geoff)
        
        battle.AddFaction('Enemies', playerFaction=False)
        banditSprite = BattleSprite('bandit', anchor=(0.5, 0.75), placeMark=(0,-75))
        
        bandit1 = SimpleAIFighter("Bandit 1", Speed=10, Attack=15, Defence=8, sprite=banditSprite)
        bandit1.RegisterSkill(Library.Skills.KnifeAttack, 1)
        battle.AddFighter(bandit1)
        bandit2 = SimpleAIFighter("Bandit 2", Speed=10, Attack=15, Defence=8, sprite=banditSprite)
        bandit2.RegisterSkill(Library.Skills.KnifeAttack, 1)
        battle.AddFighter(bandit2)
        bandit3 = SimpleAIFighter("Bandit 3", Speed=10, Attack=15, Defence=8, sprite=banditSprite)
        bandit3.RegisterSkill(Library.Skills.KnifeAttack, 1)
        battle.AddFighter(bandit3)
        
        battle.AddExtra(RPGDamage())
        battle.AddExtra(RPGDeath())
        battle.AddExtra(ActiveDisplay("Player", {"HP": "Health", "Move": "Move", "MP":"MP"}))
        battle.AddExtra(RPGActionBob())
        battle.AddExtra(SimpleWinCondition())

        renpy.music.play("audio/battle.ogg", fadein=0.5)
        battle.Start()
        
        winner = battle.Won

    # Back in regular Ren'Py land:
    stop music fadeout 1.0
        
    if (winner == 'Player'):
        #TODO: Play victory music
        "Well done, you beat the bad guys."
    else:
        #TODO: Play failure music
        "Game Over: You Died."
        jump start
        
    "Oh no! here comes a boss battle!"
    
    python:
        battle = Battle(ActiveSchema())
        battle.SetBattlefield(SimpleBattlefield(BattlefieldSprite('bg woodland')))
        
        battle.AddFaction("Player", playerFaction=True)
        battle.AddFighter(bob)
        battle.AddFighter(geoff)
        
        battle.AddFaction('Enemies', playerFaction=False)
        banditSprite = BattleSprite('bandit chief', anchor=(0.5, 0.75), placeMark=(0,-75))
        
        boss = SimpleAIFighter("Bandit Chief", Speed=15, Attack=45, Defence=35, Health=250, sprite=banditSprite)
        boss.RegisterSkill(Library.Skills.SwordAttack, 1)
        battle.AddFighter(boss)
        
        battle.AddExtra(RPGDamage())
        battle.AddExtra(RPGDeath())
        battle.AddExtra(ActiveDisplay("Player", {"HP": "Health", "Move": "Move", "MP":"MP"}))
        battle.AddExtra(RPGActionBob())
        battle.AddExtra(SimpleWinCondition())

        renpy.music.play("audio/battle.ogg", fadein=0.5)
        battle.Start()
        
        winner = battle.Won
        
    if (winner == 'Player'):
        #TODO: Play victory music
        "Well done, you beat everyone."
    else:
        #TODO: Play failure music
        "Game Over: You Died."
    
    jump start
