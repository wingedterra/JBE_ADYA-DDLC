label test_main:    
    stop music fadeout 2.0
    play music t2
    scene bg residential_day
    with dissolve_scene_full
    menu:
        
        mc "Pick testing:"
        "Fite Engine":
                return "m1"
        "Overworld Engine":
                #These vars need to be initialized before calling the overworld.
                #The original template does it in the script, which causes you to be teleported back to the entry point after interacting with the inn.
                $playerX = None
                $playerY = None
                return "m2"
                
label rpg:
    scene black
    jump active_demo

label test_overworld:
    call map
    #This is just to test returning from the overworld map
    play music t2
    scene bg sayori_bedroom
    show yuri 1d at t11
    y "This is just to show that returning from the overworld back into a main script works."

return