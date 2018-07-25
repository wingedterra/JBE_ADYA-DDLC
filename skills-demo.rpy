# The Skills demo assumes that you've already read and understood the Grid demo, and
# will not repeat those concepts. Only new things will be commented in this demo.

init python:
    
    # Here, we'll set up a new skill or two, to show how to extend the battle framework to meet
    # your own needs. In this case, we're adding a spell to resurrect the dead.
    
    # To create a new skill, you'll need to write a new class which descends from the 'Skill' class provided
    # by the engine.
    class Resurrect(Skill):
        
        # In the __init__ method, we set up some basic configuration stuff about the skill that the 
        # engine will use.
        def __init__(self):
            
            # The skill name is shown when an enemy fighter uses the skill
            skillName = "Resurrect"
            
            # The command is the menu steps the player goes through when picking the skill. Each
            # step is a tuple of two values - one is the text label in the skill-picker menu that it will use,
            # the second is the 'weight' that the label has within that menu - higher weights go nearer the
            # bottom of the menu, so you can use this to sort the items in the skill menu.
            # So this one will be filed under 'Resurrect' in the 'Magic' sub-menu (we use a weight of 5 because
            # 'Magic' has a weight of 5 in all the pre-existing skills).
            # If we'd given it a command of: 
            #     [("Magic", 5), ("Black", 0), ("Raise Dead", 0)]
            # then it would create a sub-menu for "Black" magic under the main Magic menu, and the
            # skill would be accessible through the item "Raise Dead" in that menu.
            skillCommand = [("Magic", 5), (skillName, 0)]


            # This spell targets friendlies, so long as they're dead. You can set the targetting up how you like,
            # each of the parameters to TargetData should be fairly self-explanatory.
            self._targets = TargetData(fighters=True, positions=False, factions=False, los=True, friendly=True, enemy=False, live=False, dead=True, range=4, fightersImpede=True)
    
            # Each skill must call down to the base class' __init__ method, which generally just looks like this.
            # The 'name' and 'command' parameters are set up in that base __init__ method, along with
            # some other setup.
            super(Resurrect, self).__init__(name=skillName, command=skillCommand)
            

        # In the SetUpFighter method, we have to ensure that a fighter is ready to use this skill.
        # This method is called when the skill is registered on that fighter, and we use it to make sure that
        # he has the necessary stats to make use of it, so we don't get "stat not defined" errors later.
        def SetUpFighter(self, fighter):
            
            # The 'RegisterStat' method on Fighter will check whether the stat with that name already exists,
            # and if it doesn't, it will create it with the given default value. So if we add the Resurrect skill to a
            # fighter and they don't already have an MP stat (magic points), they'll get given one with a value
            # of 10. If they already have the stat, nothing will happen.
            fighter.RegisterStat("MP", 10)

        # The IsAvailable method returns a 'True' or a 'False' to tell the engine whether the skill is available for
        # use by this fighter at this time. This will determine whether it can be clicked in the skill menu, for
        # example.
        def IsAvailable(self, fighter):
            
            # In our case, we need to check whether the fighter in question has sufficient magic points to 
            # cast the 'Resurrect' spell. 
            if (fighter.Stats.MP >= 10):
                return True
            else:
                return False
                
        # PerformAction is the method which is called when the skill is actually used by a fighter.
        # The 'fighter' parameter is the fighter which is performing the action - the one who used the skill.
        # The 'target' parameter is a tuple, the first is the fighter who's been targetted, the second is the
        # path to the target, which is useful for skills like 'Move'.
        def PerformAction(self, fighter, target):
            
            # first we get the target corpse, we don't care about the route there
            t = target[0]
            
            # Set the lucky (?) winner to Active again, to show he's no longer 'dead'.
            t.Active = True
            
            # Set his health to half his original health, because he was dead a minute ago.
            t.Stats.Health = t.BaseStats.Health / 2
            
            if t.Stats.Health < 1:
                t.Stats.Health = 1
            
            # We also have to show him, to make sure he shows up as a live person again - if he's drawn 
            # on-screen at all right now, it's as a corpse.
            t.Show()
            
            # Lastly, resurrecting a person is all the spell-caster can do this turn, so we take off the magic-points
            # he spent and end his turn.
            fighter.Stats.MP = fighter.Stats.MP - 10
            fighter.EndTurn()
            


    # Next we'll add a skill to entice opposition fighters to join your side.
    class Charm(Skill):
        
        def __init__(self):
            
            skillName = "Charm"
            # This time it'll just be a top-level skill item, on the first menu. If that's the case, you
            # don't have to specify a command, and it'll just use the skill name that you pass in.
            
            # A range of 1, so you have to go right up to them to do it, and only targetting live enemy fighters.
            self._targets = TargetData(fighters=True, positions=False, factions=False, los=True, friendly=False, enemy=True, live=True, dead=False, range=1, fightersImpede=True)
            
            # Calling through the base __init__ again:
            super(Charm, self).__init__(name=skillName)
    
        def SetUpFighter(self, fighter):
            fighter.RegisterStat("Charisma", 99)

        # In this case, we're talking about a built-in always-available skill, so we always return 'True' here.
        def IsAvailable(self, fighter):
            
            return True
                
        def PerformAction(self, fighter, target):
            
            # First, check a percentage against the fighter's Charisma:
            score = renpy.random.random()* 100
            if score <= fighter.Stats.Charisma:
                # get the target fighter
                t = target[0]
            
                # Change his faction to the faction of the skill user
                t._battle.ChangeFaction(t, fighter.Faction)
                
                # At this point you may want to throw up shiny graphics, but for now we'll just announce the success:
                t._battle.Announce(t.Name + " was charmed.")
            else:
                t._battle.Announce(fighter.Name + " failed to charm.")
                
            fighter.EndTurn()

label skills_demo:

    python:
        schema = CustomSchema(SimpleTurnSchema, attackResolver=ElementalAttackResolver)
        battle = Battle(schema)
        fieldSprite = BattlefieldSprite('bg woodland iso grid')
        battlefield = GridBattlefield(fieldSprite, origin=(362, 441), gridSize=(6,5), spaceSize=(75, -38), diagonals=False, isometric=True)
        battle.SetBattlefield(battlefield)

        treeSprite = BattleSprite('scenery tree', anchor=(0.57, 0.85))
        tree = Scenery('Tree', sprite=treeSprite, blocksPosition=True, blocksLoS=False)
        battle.AddScenery(tree, x=2, y=0)
        
        battle.AddFaction('Player', playerFaction=True)
        
        bobSprite = BattleSprite('bob', anchor=(0.5, 0.75), placeMark=(0,-100))
        bob = PlayerFighter("Bob", Speed=8, Move=4, Attack=20, Defence=20, sprite=bobSprite) 
        bob.RegisterSkill(Library.Skills.SwordAttack)
        bob.RegisterSkill(Library.Skills.Skip)
        bob.RegisterSkill(Library.Skills.Move)
        battle.AddFighter(bob, x=0, y=4)
        
        geoffSprite = BattleSprite('geoff', anchor=(0.5, 0.8), placeMark=(0,-100))
        geoff = PlayerFighter("Geoff", Speed=13, Move=5, Attack=7, Defence=10, MP=30, sprite=geoffSprite)
        geoff.RegisterSkill(Library.Skills.SwordAttack)
        geoff.RegisterSkill(Library.Skills.Skip)
        geoff.RegisterSkill(Library.Skills.Move)
        geoff.RegisterSkill(Library.Skills.Fire1)
        geoff.RegisterSkill(Library.Skills.Water1)
        geoff.RegisterSkill(Library.Skills.Earth1)

        # Now we'll also add the new skills we defined earlier...
        
        geoff.RegisterSkill( Resurrect() )
        geoff.RegisterSkill( Charm() )

        battle.AddFighter(geoff, x=0, y=0)
        
        
        battle.AddFaction('Enemies', playerFaction=False)
        
        banditSprite = BattleSprite('bandit', anchor=(0.5, 0.75), placeMark=(0,-80))
        banditChiefSprite = BattleSprite('bandit chief', anchor=(0.5, 0.75), placeMark=(0,-80))
        
        bandit1 = MovingAIFighter("Bandit 1", Library.Skills.Move, idealDistance=1, Move=4, Speed=10, Attack=10, Defence=8, sprite=banditSprite)
        bandit1.RegisterSkill(Library.Skills.KnifeAttack, 1)
        battle.AddFighter(bandit1, x=5, y=0)
        bandit2 = MovingAIFighter("Bandit 2", Library.Skills.Move, idealDistance=1, Move=4, Speed=10, Attack=10, Defence=8, sprite=banditSprite)
        bandit2.RegisterSkill(Library.Skills.KnifeAttack, 1)
        battle.AddFighter(bandit2, x=5, y=4)
        bandit3 = MovingAIFighter("Bandit Chief", Library.Skills.Move, idealDistance=1, Move=4, Speed=13, Attack=20, Defence=15, sprite=banditChiefSprite)
        bandit3.RegisterSkill(Library.Skills.SwordAttack, 1)
        battle.AddFighter(bandit3, x = 5, y=2)
        
        
        battle.AddExtra(RPGDamage())
        battle.AddExtra(RPGDeath())
        battle.AddExtra(GridStatsDisplay("Player", {"HP": "Health", "Move": "Move", "MP":"MP"}))
        battle.AddExtra(SimpleWinCondition())
        
        battle.Start()

        winner = battle.Won
    
    # Back in regular Ren'Py land:
    if (winner == 'Player'):
        #TODO: Play victory music
        "Well done, you beat the bad guys."
    else:
        #TODO: Play failure music
        "Game Over: You Died."
        
    jump start
