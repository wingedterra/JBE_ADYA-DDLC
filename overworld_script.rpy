label map:
    $map_on = True
    window hide None
    scene black
    #play music "happy.ogg" fadein .5
    play music t3 fadein 0.5
    python:
        ui.layer("mapEngine")

        ui.add(OverworldDisplayable(map_layout = moordell_layout, tileList = moordell_tiles,
            portals = moordell_portals, portal_tiles = moordell_portal_tiles,
            enemy_layout = moordell_enemies_layout, enemySprites = moordell_enemies,
            
            NPCSprites = moordell_villagers, #villagers, uses the same layout as enemies
            groundLayout = moordell_ground,
            playerSprites = ken_sprites, playerX = playerX, playerY = playerY,
            scrolling = True))
        ui.close()
        results = ui.interact(suppress_overlay=True, suppress_underlay= False)
        closeMap()
        gotoLabel = results[0]
        playerX = results[1]
        playerY = results[2]
        renpy.jump(gotoLabel) 
    with dissolve
    return
    
label talky_label:
    show sayori 4bxo at left onlayer npcPortraits with dissolve
    s "I'm an NPC!"
    s "You can talk to me if you need help."
    
    s "I might have something useful to say."
    s "Or not."
    s "Until then I'll just go about my day."
    hide sayori with dissolve
    return
label talky2:
    #show girl at left onlayer npcPortraits with dissolve
    show monika 2ao at left onlayer npcPortraits with dissolve
    m "I'm also an NPC!"
    m "But I'm static. I'm content to just sit around."
    m "I'm more likely to be important, so the programmer made me easier to find!"
    m "By the way, I wonder what's beyond that gate. Maybe you should go see."
    hide monika with dissolve
    return
label talky3:
    #show girl at left onlayer npcPortraits with dissolve
    show yuri 1do at left onlayer npcPortraits with dissolve
    y "I'm here to test adding more sprites!"
    hide yuri with dissolve
    return
label talky4:
    #show girl at left onlayer npcPortraits with dissolve
    show natsuki 1do at left onlayer npcPortraits with dissolve
    n "I'm here to test adding more sprites!"
    hide natsuki with dissolve
    return


label ari_caught:
    scene field with dissolve
    "Oh no! You got caught."
    $ari_battle.won = True
    jump map
    
label leave_city:
    scene field with dissolve
    "Looks like it's time to go."
    return
    
label inn:
    scene inn with dissolve
    "This is where an inn would go!"
    "Truly amazing."
    jump map
label building_locked:
    "It's locked."
    return
label inn_desc:
    "It's an inn. A faint light is cast through the window, and figures can be seen moving inside."
    "A pleasant din is heard through the door."
    return
    
