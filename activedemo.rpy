label active_demo:
    python:
        _game_menu_screen = None
        #Need to disable the menu during a battle as it's pretty buggy jumping out of the engine that way.
        #Also, access to the menu means saving during a battle. Which works perfectly fine, just probably isn't desired behavior..
        config.skipping = False
        config.allow_skipping = False
        allow_skipping = False
    play music "audio/battle2.ogg" fadein 0.5


    python:
        
        # First, we create the battle itself, and choose a schema to use.
        # In this case, the schema describes an active battle - so we'll have the initiative bars deciding the order of actions, for example.
        battle = Battle(ActiveSchema())

        # Next, we need to set up our battlefield - this is accomplished in three steps:
        
        # Step one: create a sprite for the battlefield BG.
        # Note that we're just passing the name of the image defined in assets.rpy; we could equally pass a Displayable instance if we preferred. 
        #fieldSprite = BattlefieldSprite('bg woodland')
        fieldSprite = BattlefieldSprite('bg house')
        # Step two: create the battlefield object, in this case we're using a SimpleBattlefield (so we have the classic FF-style face-off).
        battlefield = SimpleBattlefield(fieldSprite)
        
        # Step three: add the battlefield object to the battle, so our battle knows which one to use.
        battle.SetBattlefield(battlefield)
        
        # (This could all be done on one line if you prefer, as in the following line of commented-out code:
        # battle.SetBattlefield(SimpleBattlefield(BattlefieldSprite('bg woodland')))
        
        # Next, we need to add some fighters to our battle; we'll start off with the players.
        # Before we can add any fighters, we have to create a faction for them to belong to:
        battle.AddFaction("Player", playerFaction=True)
        
        # To add a fighter, first create a sprite.
        # - The first parameter is the name of the image to use for that sprite.
        # - The 'anchor' parameter denotes the part of the sprite (in the same way as xanchor/yanchor in 
        #   Ren'Py position properties) where the character's feet are found. This is the point which is placed in that fighter's position 
        #   on the battlefield. (This is more relevant for grid battles.)
        # - The 'placeMark' parameter denotes the offset from the anchor point that should be used for giant-floating-hand-style
        #   selection cursors. This is also where the bouncy damage numbers come out, if your fighters get hit.
        #   Bearing in mind that Ren'Py coordinates have (0,0) in the top-left corner, this example placeMark of
        #   (0, -100) means "in line with the anchor point left-to-right, but 100 pixels higher".
        natsukiSprite = BattleSprite('natsuki', anchor=(0.5, 1.10), placeMark=(0,-100))
        
        # Next, we create Bob as a player fighter - meaning he'll be controlled by the player, who'll get to choose his moves.
        # the first parameter is the fighter's name, and the 'sprite' parameter gives the sprite to use for that character;
        # all other params, with names, are used for Bob's stats.
        # If you don't include a particular stat in the list, then if Bob needs it to use a skill or something, it'll be added automatically
        # with a reasonable default, so you only actually have to define the non-default stats.
        # (Bob is a bit of a brawler, good at hand-to-hand combat but not so fast.)
        natsuki = PlayerFighter("Natsuki", Speed=11, Attack=20, Defence=20, sprite=natsukiSprite) 
        
        # Next, we give Bob his skills. Skills are the things that show up on the command menu when we're selecting what Bob should
        # do in a turn.
        # We're only going to give him 'attack' (a physical attack) and 'skip' (in case he doesn't want to attack) for now.
        natsuki.RegisterSkill(Library.Skills.SwordAttack)
        natsuki.RegisterSkill(Library.Skills.Skip)


        # Finally, we have to add Bob to the battle. He'll automatically get added to the last faction you defined (in this case, 'Player').
        battle.AddFighter(natsuki)
        
        # Then we'll do much the same for Bob's compatriot Geoff. Geoff is a nimble but weak character who backs up his team-mate
        # with magic attacks.
        yuriSprite = BattleSprite('yuri', anchor=(0.5, 0.95), placeMark=(0,-100))
        yuri = PlayerFighter("Yuri", Speed=13, Attack=7, Defence=10, MP=20, sprite=yuriSprite)
        yuri.RegisterSkill(Library.Skills.SwordAttack)
        yuri.RegisterSkill(Library.Skills.Skip)
        yuri.RegisterSkill(Library.Skills.Fire1)
        yuri.RegisterSkill(Library.Skills.Water1)
        yuri.RegisterSkill(Library.Skills.Earth1)
        battle.AddFighter(yuri)
        
        sayoriSprite = BattleSprite('sayori', anchor=(0.5, 0.75), placeMark=(0,-100))
        sayori = PlayerFighter("Sayori", Speed=13, Attack=15, Defence=10, MP=15, sprite=sayoriSprite)
        sayori.RegisterSkill(Library.Skills.SwordAttack)
        sayori.RegisterSkill(Library.Skills.Skip)
        sayori.RegisterSkill(Library.Skills.Fire1)
        sayori.RegisterSkill(Library.Skills.Water1)
        battle.AddFighter(sayori)

        
        # Now, we have a player team, so we have to give them some opposition. We'll start out by creating a faction for the bad guys:
        battle.AddFaction('Enemies', playerFaction=False)
        
        # For the enemies' sprites, we're adding a 'placeMark' parameter. This determines where the button to
        # click to target that enemy will be drawn, relative to the point they're standing (the 'anchor' point
        # described earlier). In this case we're setting it to (0, -75), which means 75 pixels directly above
        # the point they're standing on.
        # (We're also using a 100px-tall graphic which is mostly empty and just has a pointing hand at the top.
        # That will be centred on the placeMark point, so the top of our pointing hand will be 125px above the
        # anchor point (75 + (100/2)).)
        banditSprite = BattleSprite('bandit', anchor=(0.5, 0.75), placeMark=(0,-75))
        
        # Defining enemies is much the same as defining players, except we use the 'SimpleAIFighter' class instead of 'PlayerFighter':
        bandit1 = SimpleAIFighter("Bandit 1", Speed=10, Attack=15, Defence=8, sprite=banditSprite)
        # When we register a skill for a SimpleAIFighter, we provide a weight - how often compared to other skills the fighter uses this one.
        # Since we only have one skill, it doesn't matter what the value is. If we had two, one of which had a weight of 1 and the other of 2, 
        # the 2-weighted skill would be used twice as often.
        bandit1.RegisterSkill(Library.Skills.KnifeAttack, 1)
        battle.AddFighter(bandit1)
        bandit2 = SimpleAIFighter("Bandit 2", Speed=10, Attack=15, Defence=8, sprite=banditSprite)
        bandit2.RegisterSkill(Library.Skills.KnifeAttack, 1)
        battle.AddFighter(bandit2)
        bandit3 = SimpleAIFighter("Bandit 3", Speed=10, Attack=15, Defence=8, sprite=banditSprite)
        bandit3.RegisterSkill(Library.Skills.KnifeAttack, 1)
        battle.AddFighter(bandit3)
        
        
        # Next, we add any Extras we care about. Extras are plug-in bits which add to the behaviour of the battle in some way.
        
        # We'll start with one for RPG damage, to show a bouncing red number when someone gets hit.
        battle.AddExtra(RPGDamage())
        
        # Along similar lines, RPGDeath fades the fighter out when they die.
        # (We could have made the sprite do this when its fighter dies, but then we'd have to replicate that
        # for every sprite in the battle, it could be tedious.)
        battle.AddExtra(RPGDeath())
        
        # Next we'll add 'ActiveDisplay', which draws a stats box for the given faction (we'll do it for the players).
        # The first parameter here is the name of the faction to display.
        # The second parameter is a Python dictionary telling us what to display on the stat line, and which of the fighter's stats to get the number from.
        # (Mostly we're using the stat name for display, but - for example - we're showing the 'Health' stat with the label 'HP'.)
        battle.AddExtra(ActiveDisplay("Player", {"HP": "Health", "Move": "Move", "MP":"MP"}))
        
        # This one will cause any fighter performing an action to bob a bit first, so it's easy to see who's doing what.
        battle.AddExtra(RPGActionBob())
        
        # Finally, we'll add a win condition! The engine doesn't actually decide a winner on its own at all, 
        # you have to add an Extra which will do it... this is because sometimes, you might want to create
        # battles where one side can be wiped out but still win becuase they prevented the opponents from
        # advancing for ten turns, or something like that, where a built-in win condition might make it
        # difficult or impossible to code what you want.
        # However, for the 99% of times when you just want to have one side hit the other side until they
        # fall over, we can use 'SimpleWinConditon', which just ends the battle in favour of the last
        # faction standing.
        battle.AddExtra(SimpleWinCondition())
        
        # That's it! We're ready to go, so we just hit the 'Start()' method on our battle object, and the battle will kick off!
        battle.Start()
        # After the battle concludes, we can pull the winner out from the 'Won' property on the battle object:
        winner = battle.Won
    
    # Back in regular Ren'Py land:
    if (winner == 'Player'):
        #TODO: Play victory music DID IT
        stop music fadeout 1.0
        play music "audio/victory1.ogg" fadein 0.5
        python:
            import random
            bg_choice = random.randint(1,3)
            _game_menu_screen = 'save' #Re-enable the menu

        if bg_choice == 1:
            show image "cg/y_cg2.png"
        elif bg_choice == 2:
            show image "cg/s_cg2_base1.png"
        else:
            scene n_cg1_bg
            show n_cg1_base

        "You won!"
    else:
        #TODO: Play failure music
        "Game Over: You Died."
        
    jump start
