init python:
    
    class AlternateUIProvider(UIProvider):
        # This method expects a list of fighters, and is expected to return the single fighter that is picked.
        def PickFighter(self, fighters):
            
            # First, choose the 'UI' layer from the set of battle engine-controlled layers 
            l = self._battle.GetLayer("UI")

            # Set up an 'End Turn' button, so that if the player doesn't want to continue his
            # turn he can stop it here.
            endText = Text("End Turn", slow=False, style='EndTurnPickTargetFighterText')
            endButton = Button(endText, clicked=ui.returns(-1), style='EndTurnPickTargetFighterButton')
            renpy.show("UI_PickFighter_EndTurnButton", what=endButton, layer=l)
                                    
            # Next we set up a list of displayables to hide later, 'cause we're going to be displaying UI items directly
            hideList = ["UI_PickFighter_EndTurnButton"]

            # Set up a count of which fighter's pointer we're showing             
            x = 0
            
            # Loop through all fighters in the pick-from list passed into the method
            for fighter in fighters:

                # For each fighter we display a button with nothing much on it.
                # We're using the PickTargetFighter styles so that the pick-a-fighter-on-your-own-side
                # UI looks identical to the pick-an-enemy-fighter-to-target UI - in the demo, a pointing white-gloved hand.
                buttonText = Text(" ", slow=False, style='PickTargetFighterText')

                # The 'clicked' property of the button returns the current-fighter count 
                fButton = Button(buttonText, clicked=ui.returns(x), style='PickTargetFighterButton')

                # The tag of the button has to be unique, so we append the fighter's tag to a prefix string
                tag = "UI_PickTargetFighter_FighterButton_"+fighter.Tag

                # The position to place the picker button is determined by a combination of the fighter's position, and an offset Transform
                # constructed using the fighter's "PlaceMark", which is a property of the fighter designed just to show an offset from the 
                # fighter's actual on-field position to use for things like big pointing white-gloved hands.
                offset = Transform(xoffset=fighter.PlaceMark[0], yoffset=fighter.PlaceMark[1], xanchor=0.5, yanchor=0.5)
                renpy.show(tag, what=fButton, at_list=[fighter.Position.Transform, offset], layer=l)
                hideList.append(tag)
                x = x + 1

            
            result = self.Interact()
            
            # After we've got the result, hide all the buttons
            # (This isn't actually all that critical for the purposes of "pick which fighter to use", because the battlefield
            # is refreshed at the start of a fighter's turn and everything that isn't redrawn by the battlefield,
            # the fighters or an Extra will be lost anyway, but it's good form and necessary if there's ever any other
            # reason to pick a fighter other than for targetting.)
            for d in hideList:
                renpy.hide(d, layer=l)

                
            # Lastly, we return whichever of the fighters from the list was picked.
            # If the user clicked 'End Turn' there'll be a -1 result, so just return 'None' to
            # signal to the engine that no more fighter turns are required.
            if (result == -1):
                return None
            else:
                return fighters[result]
            
            
    class  AlternateBattleMechanic(BattleMechanic):
        
        def RunBattleRound(self):
            
            # for each faction, perform a turn, one after another:
            for faction in self._battle.Factions:
                
                # First make sure the battle is still running, otherwise return immediately.
                # So, for example, if one faction kills everyone else we don't want to move on to the next faction and run their turn,
                # we want to end the battle as soon as possible, and that means not doing anything else here.
                if self._battle.On == False:
                    return
                    
                # Just to be sure, we show the current state of the battle here.
                self._battle.Show()
                
                # Let the player know whose turn it is
                self._battle.Announce("%(fac)s's Turn" % {"fac": faction})
                
                # get a list of fighters
                fighters = self._battle.FactionLists[faction][:]
                
                # loop while the fighter list isn't empty
                while len(fighters) > 0 and self._battle.On:
                    
                    # check that all fighters are still active:
                    for fighter in fighters[:]:
                        if fighter.Active == False:
                            fighters.remove(fighter)

                    
                    # select a fighter to use, then act with that fighter
                    if len(fighters) == 1:
                        fighter = fighters[0]
                    elif len(fighters) == 0:
                        fighter = None
                    else:
                        
                        # There's a neater way to do this, but for the sake of demonstration we'll use the more-readable way.
                        
                        # First, pick an arbitrary fighter to be your current 'most-high initiative found' fighter.
                        highestInitiative = fighters[0]
                        
                        # Then, loop through all fighters
                        for f in fighters:
                            # At each step, check if the fighter f's initiative is higher than the current best-initiative-found-so-far fighter.
                            if (f.Stats.Initiative > highestInitiative.Stats.Initiative):
                                # If you find someone with a higher initiative, then replace the current champion with the new one
                                highestInitiative = f
                        
                        # Now we've found the fighter with the highest initiative of all the fighters who haven't had a turn yet,
                        # so mark them as the one whose turn to run:
                        
                        fighter = highestInitiative
                        
                    # Now, we've selected a fighter to perform their actions next, so we need to actually run their turn
                    if (fighter != None):
                        self.RunFighterTurn(fighter)
                        # After they've had their turn, we remove them from the fighters-who-haven't-had-their-turn-yet
                        # list so they can't have two goes in the same faction-turn.
                        fighters.remove(fighter)
