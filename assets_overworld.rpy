init python:
    
    class Dummy: #a dummy class used in place of a battle. Normally this should be integrated with Jake's battle engine, instead of using a dummy class.
        def __init__(self,won):
            self.won = won
            
        
    ari_battle = Dummy(False)
    #sprite arrays should always be in north, south, east, west order.
    map_on = False #Is a map being displayed? This governs whether the "yesno" screen is modal.
    
    #SPRITES
    ari_sprites = [["ari-n2.png", "ari-n3.png", "ari-n1.png", "ari-n1.png"],  #enemy sprites
        ["ari-s2.png", "ari-s3.png", "ari-s1.png", "ari-s1.png"], 
        ["ari-e2.png", "ari-e3.png", "ari-e4.png", "ari-e1.png"], 
        ["ari-w2.png", "ari-w3.png", "ari-w4.png", "ari-w1.png"],
        (64,64)]
        
    ken_sprites =[ #player sprites
    ["ken_m_n.png", "ken_m_n1.png", "ken_m_n1.png", "ken_m_n.png", "ken_m_n3.png", "ken_m_n3.png"],
    ["ken_m_s.png", "ken_m_s1.png", "ken_m_s1.png", "ken_m_s.png", "ken_m_s3.png", "ken_m_s3.png"],
    ["ken_m_e.png", "ken_m_e1.png", "ken_m_e1.png", "ken_m_e.png", "ken_m_e3.png", "ken_m_e3.png"],
    ["ken_m_w.png", "ken_m_w1.png", "ken_m_w1.png", "ken_m_w.png", "ken_m_w3.png", "ken_m_w3.png"],
    (64,64)
    ]
    
    villager_sprites = [ #villager
    ["villager-n1.png", "villager-n2.png", "villager-n3.png"],
    ["villager-s1.png", "villager-s2.png", "villager-s3.png"],
    ["villager-e1.png", "villager-e2.png", "villager-e3.png"],
    ["villager-w1.png", "villager-w2.png", "villager-w3.png"],
    (96,96)
    ]
    
    #TILESETS
      
    #signifier, base name, building size, roof size, has roof, goToLabel, actionLabel (used for descriptions)
    moordell_tiles = [
    ["1","cute_buildings/1", (256,216), (256,256),True,None,"building_locked"],
    ["2","cute_buildings/2", (256,216), (256, 256),True,None,"building_locked"],
    ["3","cute_buildings/3", (256,216), (256,256),True,None,"building_locked"],
    ["*","cute_buildings/inn", (342,216),(342,256),True, "inn","inn_desc"],
    ["n", "cute_buildings/wall", (128,128),None,False,None,None],
    ["e", "cute_buildings/wall", (128,128),None,False,None,None],
    ["w", "cute_buildings/wall", (128,128),None,False,None,None],
    ["s", "cute_buildings/wall", (128,128),None, False,None,None],
    ["p", "dirt", (128,128),None, False, None,None],
    ["g", "grass", (128,128),None, False, None,None],
    ]
    #signifier, range, roaming,  sprite set, facing, associated battle label, associated battle
    moordell_enemies = [
    ["a", (512,512), True, ari_sprites, "down", "ari_caught", ari_battle],
    ]
    
    #signifier, range, roaming,  sprite set, facing, conversation label
    moordell_villagers = [
    ["v", (256,256), True, villager_sprites, "down", "talky_label"], #example of roaming NPC
    ["b",None, False, villager_sprites,  "down", "talky2"], #example of static NPC
    ["c",None, False, villager_sprites,  "down", "talky3"],
    ["d",None, False, villager_sprites,  "down", "talky4"]
    ]
    
    #[signifier, goToLabel]
    moordell_portal_tiles = [['p', 'leave_city'], ['i', 'inn']]
    
    
    #MAP LAYOUTS
    #these maps should align for ease of use. 
    #If they don't look square, switch to a monospace font like consolas!   
    
    moordell_layout =[
    "nnnnnnnonnnnnnn",
    "w3oo*ooo2oo1ooe",
    "woooooo+ooooooe",
    "woooooooooooooe",
    "w3oooooo1oooooe",
    "woooooooooooooe",
    "woooooooooooooe",
    "w2o3ooooo1oo2oe",
    "woooooooooooooe",
    "woooooooooooooe",
    "w3ooo1o3o2oo1oe",
    "woooooooooooooe",
    "woooooooooooooe",
    "w1o2o2ooo3o1ooe",
    "woooooooooooooe",
    "woooooooooooooe",
    "sssssssssssssss",
    ]
    
    moordell_portals =[
    "ooooooopooooooo",
    "ooooioooooooooo",
    "ooooooooooooooo",
    "ooooooooooooooo",
    "ooooooooooooooo",
    "ooooooooooooooo",
    "ooooooooooooooo",
    "ooooooooooooooo",
    "ooooooooooooooo",
    "ooooooooooooooo",
    "ooooooooooooooo",
    "ooooooooooooooo",
    "ooooooooooooooo",
    "ooooooooooooooo",
    "ooooooooooooooo",
    "ooooooooooooooo",
    "ooooooooooooooo",
    ]
    
    
    moordell_ground =[
    "gggggggpggggggg",
    "gggggggpggggggg",
    "gggggggpggggggg",
    "ppppppppppppppp",
    "gggggggpggggggg",
    "gggggggpggggggg",
    "ppppppppppppppp",
    "gggggggpggggggg",
    "gggggggpggggggg",
    "ppppppppppppppp",
    "gggggggggggggpg",
    "gggggggggggggpg",
    "gggggggggggggpg",
    "ppppppppppppppp",
    "ggggggggggggggg",
    "ggggggggggggggg",
    "ggggggggggggggg",
    ]  
    moordell_enemies_layout =[
    "ooooooooooooooo",
    "ooooooooooooooo",
    "ooooooooooooooo",
    "oodoooooooocooo",
    "ooooooooooooooo",
    "ooooovooooooooo",
    "ooooooooooooooo",
    "ooooooooooooooo",
    "ooooooooboooooo",
    "ooooooooooooooo",
    "ooooooooooooooo",
    "oooooaooooooooo",
    "ooooooooooooooo",
    "ooooooooooooooo",
    "ooooooooooooooo",
    "ooooooooooooooo",
    "ooooooooooooooo",
    ]

