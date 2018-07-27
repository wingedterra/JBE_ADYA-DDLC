# JBE_ADYA-DDLC
Implementation of Jake's Battle Engine and ADYA Overworld Engine for Doki Doki Literature Club.

You will need to add images.rpa, fonts.rpa, and audio.rpa from an install of DDLC. The result is a "game" folder for a DDLC mod build.

Main additions from the default engines:

Scaled up Jake's engine to work with DDLC's resolution (800x600 -> DDLC's 1280x720).

Made a more DDLC-themed sample battle using the chibi sticker sprites from the poem minigame. 

Scaled the DDLC sprites to be callable from within ADYA. (They are too big, needed to be about 75% of their original size)

Added two more NPCs to the default map so all the girls' sprites can be tested at the same time.

Here's what engine each of the files are for (in case you want just one of the engines):

activedemo.rpy - J
ari*.png - A
assets.rpy - J
assets_overworld.rpy - A
astar.rpy - A
autoscroll.rpy - J
battle-screens.rpy - J
cgs.rpy - JA
definitions.rpy - JA
dirt.png - A
door.ogg - A
effects.rpy - JA
engine.rpy - J
engine-battlefields.rpy - J
engine-display.rpy - J
engine-events.rpy - J
engine-extras.rpy - J
engine-fighters.rpy - J
engine-items.rpy - J
engine-schema.rpy - J
engine-skills.rpy - J
engine-ui.rpy - J
engine-xp.rpy - J
equipment-demo.rpy - J
example-items.rpy - J
extension-demo.rpy - J
gui.rpy - JA
matrices.rpy - J
options.rpy - JA
overrides.rpy - JA
overworld.rpy - A
overworld_script.rpy - A
screen_demo.rpy - J
screens.rpy - JA
script.rpy - JA
skills-demo.rpy - J
splash.rpy - JA
test_main.rpy - JA
transforms.rpy - JA
villager*.png - A
xp-demo.rpy - J

Current work to-do:

JBE:
Move the enemy sprites over to the far right portion of the screen so the whole screen is used (and move the command box over so it's centered when this is done)

Align the party and enemy sprites better. 

ADYA:
Find a tilemap that more closely resembles DDLC's art style.
Create another map to demo transitioning between maps (possibly use the "inn" as a classroom?)

Jake's Battle Engine can be found here. Credits to, well, Jake. https://lemmasoft.renai.us/forums/viewtopic.php?t=16943
ADYA Overworld Engine can be found here. Credits to Moley. https://lemmasoft.renai.us/forums/viewtopic.php?f=51&t=29964
