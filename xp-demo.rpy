init python:
    
    top_bar = Frame('gfx/top_bar.png', 7, 8)
    
    style.vscrollbar.top_bar = top_bar
    style.vscrollbar.bottom_bar = top_bar
    style.vscrollbar.thumb = 'gfx/thumb.png'
    style.vscrollbar.xminimum = 14
    style.vscrollbar.xmaximum = 14


label xp_demo:
    
    # The Experience Demo assumes that you've already read and understood the comments in
    # the Equipment Demo, and will not repeat those concepts. Only new things are commented in this
    # demo.
    
    python:
        
        
        # Create 'bob' fighter
        bobSprite = BattleSprite('bob', anchor=(0.5, 0.75), placeMark=(0,-100))
        bob = PlayerFighter("Bob", Speed=11, Attack=20, Defence=20, sprite=bobSprite) 

        bob.RegisterSkill(Library.Skills.SwordAttack)
        bob.RegisterSkill(Library.Skills.Skip)
        bob.RegisterSkill(Library.Skills.Item)
        
        bob.Equipment = HandedFighterEquipment()
        bob.Equipment.Add(Library.Equipment.Sword)
        bob.Equipment.Add(Library.Equipment.RoundShield)
        
        geoffSprite = BattleSprite('geoff', anchor=(0.5, 0.8), placeMark=(0,-100))
        geoff = PlayerFighter("Geoff", Speed=13, Attack=7, Defence=10, MP=20, sprite=geoffSprite)
        
        geoff.RegisterSkill(Library.Skills.SwordAttack)
        geoff.RegisterSkill(Library.Skills.Skip)
        geoff.RegisterSkill(Library.Skills.Fire1)
        geoff.RegisterSkill(Library.Skills.Water1)
        geoff.RegisterSkill(Library.Skills.Earth1)
        geoff.RegisterSkill(Library.Skills.Item)
 
        geoff.Equipment = HandedFighterEquipment()
        geoff.Equipment.Add(Library.Equipment.Sword)
        geoff.Equipment.Add(Library.Equipment.RoundShield)
        

        inv = BattleInventory()

        inv.AddItem(Library.Items.Potion, 3)
        inv.AddItem(Library.Items.Superpotion, 1)
        inv.AddItem(Library.Items.Elixir, 3)
        inv.AddItem(Library.Items.Superlixir, 1)

        bob.Inventory = inv
        geoff.Inventory = inv

        battle = Battle(ActiveSchema())
        battle.SetBattlefield(SimpleBattlefield(BattlefieldSprite('bg woodland')))
        
        battle.AddFaction("Player", playerFaction=True)
        battle.AddFighter(bob)
        battle.AddFighter(geoff)
        
        
        # If you want XP numbers to pop up over your fighters' heads when they gain XP, you may
        # want to use the 'RGPXP' extra:
        battle.AddExtra(RPGXP())
        
        # The order these Extras are added to the battle is important. If you want the bouncy
        # XP number to come up first, then add it first. If you want it to come up after the level
        # has been applied (if applicable) then add it after.


        
        # You also need to choose how your fighters actually gain experience. One option is to simply
        # give them experience whenever they cause damage... if you do this, you'll want to use the
        # 'DamageXPGain' extra, and supply a multiplier. The example below is commented out 'cause
        # we don't want to do that here, but if it were uncommented, fighters would gain 1 XP for every
        # 10 damage they cause (because the multiplier is 0.1 - one tenth).
        # battle.AddExtra(DamageXPGain(0.1))
        
        # Another option is to give XP to a fighter every time they kill an enemy. That's all we'll use
        # here. In your own games you'll probably want to use a variety of XP-generators - if you
        # just base it on kills or damage then healer characters may never get any XP at all!
        battle.AddExtra(KillsXPGain())
        
        
        # If you want announcements when fighters level up, use the 'RPGLevelUp' extra.
        # Here we want this announcement to occur *after* the level-up bonuses have
        # been applied, so we add the extra after the ExperienceTracker extra.
        battle.AddExtra(RPGLevelUp())
        
        
        
        # To have a fighter level up, we need to first create him an Experience Plan - this is a
        # schedule that keeps track of what bonuses/stat-gains/etc. to give him under what
        # conditions.
        
        # The default and most-straightforward Experience Plan is the LevelPlan class, which gives
        # the fighter stat boosts when he hits pre-set levels. To construct a LevelPlan for a fighter,
        # first create the plan itself:
        
        bobLevels = LevelPlan(bob)
        
        # Next, we create as many levels as we think we need, and associated stat bonuses. In this demo
        # game, our fighters only have a small number of stats, so it's quite easy.
        # If we were working on a more-complex game with more stats, it would probably be worth
        # writing a separate script file for each character in which we build up his skills and his level plan
        # and so on, to keep it easy to maintain.
        
        # For each level, we need to supply two things: the extra XP needed to gain this level, and a dictionary
        # mapping stat names to gains.
        
        bobLevels.AddLevel(10, {'Speed': 1, 'Attack': 5, 'Defence': 3, 'Health':10})
        
        # Not all levels have to provide benefits to all stats: it's simple to just miss a few out if you
        # only want to boost one or two stats:
        
        bobLevels.AddLevel(20, {'Attack': 8, 'Defence': 5, 'Health':10})
        bobLevels.AddLevel(25, {'Attack': 3, 'Defence': 8, 'Health':10})
        
        # Now, the XP required at each level is cumulative - we're not saying that once Bob has 25XP,
        # he reaches that last level and gains those stats; we're saying that once Bob has gained
        # another 25XP since his last level-up, he gains another level and those stats. To gain all of
        # these levels, Bob will need to get a total of 55XP.
        
        # Each fighter starts by default at level 1 and the levels you add to their plan go up one
        # at a time. So if Bob does get 55 or more XP, he'll be on level 4.
        
        geoffLevels = LevelPlan(geoff)
        
        geoffLevels.AddLevel(10, {'Speed': 4, 'MP': 10, 'Defence': 5, 'Health':10})
        geoffLevels.AddLevel(18, {'MP': 10, 'Attack': 3, 'Defence':3, 'Health':10})
        geoffLevels.AddLevel(20, {'Attack': 2, 'Defence': 4, 'MP': 10, 'Health':10})
        
        
        # Once we've set up the level plans, we need to actually tell the battle engine to use
        # experience in this battle. We do this by adding the ExperienceTracker, which functions the
        # same as any other extra, and adding each relevant plan to it.
        
        tracker = ExperienceTracker()
        tracker.SetPlan(bob, bobLevels)
        tracker.SetPlan(geoff, geoffLevels)
        
        battle.AddExtra(tracker)
        
        

        
        # Things to bear in mind about the experience tracker:
        # - If you don't call SetPlan for a particular fighter's plan, that fighter won't gain any levels.
        # - You only have to set it up once; after that, you can re-use the same instance. It's probably
        #    a good idea to have a single script that runs at the beginning of your game that sets up
        #    all your fighters and their experience plans and adds them all to the same tracker.
        
        # Since we're using the KillsXPGain experience option, we need to assign XP prizes for each
        # enemy that we introduce. We do this just by giving the enemy a 'Prize' stat with the value
        # being the amount of XP awarded for killing that enemy. Here, each of the bad guys has a
        # prize of 15 XP.
        
        # (You may remember that this will mean that the fighters will level up pretty quickly. Of course,
        # in a real game you probably want the level thresholds to be higher, or the prizes lower... but
        # this is just a demonstration, and it's a pretty rubbish demonstration if nobody ever levels up!)
        
        battle.AddFaction('Enemies', playerFaction=False)
        banditSprite = BattleSprite('bandit', anchor=(0.5, 0.75), placeMark=(0,-75))
        
        bandit1 = SimpleAIFighter("Bandit 1", Speed=10, Attack=15, Defence=8, Prize=15, sprite=banditSprite)
        bandit1.RegisterSkill(Library.Skills.KnifeAttack, 1)
        battle.AddFighter(bandit1)
        bandit2 = SimpleAIFighter("Bandit 2", Speed=10, Attack=15, Defence=8, Prize=15, sprite=banditSprite)
        bandit2.RegisterSkill(Library.Skills.KnifeAttack, 1)
        battle.AddFighter(bandit2)
        bandit3 = SimpleAIFighter("Bandit 3", Speed=10, Attack=15, Defence=8, Prize=15, sprite=banditSprite)
        bandit3.RegisterSkill(Library.Skills.KnifeAttack, 1)
        battle.AddFighter(bandit3)
        
        battle.AddExtra(RPGDamage())
        battle.AddExtra(RPGDeath())
        battle.AddExtra(ActiveDisplay("Player", {"HP": "Health", "Move": "Move", "MP":"MP", "XP":"XP", "Lvl":"Level"}))
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
        banditLeaderSprite = BattleSprite('bandit chief', anchor=(0.5, 0.75), placeMark=(0,-75))
        
        bandit1 = SimpleAIFighter("Bandit 1", Speed=10, Attack=15, Defence=8, Prize=15, sprite=banditSprite)
        bandit1.RegisterSkill(Library.Skills.KnifeAttack, 1)
        battle.AddFighter(bandit1)
        boss = SimpleAIFighter("Bandit Chief", Speed=15, Attack=45, Defence=35, Health=150, Prize=50, sprite=banditLeaderSprite)
        boss.RegisterSkill(Library.Skills.SwordAttack, 1)
        battle.AddFighter(boss)
        bandit2 = SimpleAIFighter("Bandit 2", Speed=10, Attack=15, Defence=8, Prize=15, sprite=banditSprite)
        bandit2.RegisterSkill(Library.Skills.KnifeAttack, 1)
        battle.AddFighter(bandit2)
        
        # Note that we don't have to go about setting up the tracker again - we can re-use the
        # existing one. The level plans and everything are already in place.
        
        battle.AddExtra(RPGXP())
        battle.AddExtra(KillsXPGain())
        battle.AddExtra(tracker)
        battle.AddExtra(RPGLevelUp())

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
