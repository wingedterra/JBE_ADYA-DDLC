init python:
    
    style.AutoPanButton = Style(style.BattleButton)
    
    # Position the directional buttons to take up most of the sides of the screen to a depth of 50 pixels,
    # but leave gaps at the corners for things like the 'Cancel' and 'End Turn' buttons.
    style.AutoPanButton['left'].xminimum = 50
    style.AutoPanButton['left'].xmaximum = 50
    style.AutoPanButton['left'].yminimum = 0.8
    style.AutoPanButton['left'].ymaximum = 0.8
    style.AutoPanButton['left'].xalign = 0.0
    style.AutoPanButton['left'].yalign = 0.5
    
    style.AutoPanButton['right'].xminimum = 50
    style.AutoPanButton['right'].xmaximum = 50
    style.AutoPanButton['right'].yminimum = 0.8
    style.AutoPanButton['right'].ymaximum = 0.8
    style.AutoPanButton['right'].xalign = 1.0
    style.AutoPanButton['right'].yalign = 0.5
    
    style.AutoPanButton['up'].xminimum = 0.8
    style.AutoPanButton['up'].xmaximum = 0.8
    style.AutoPanButton['up'].yminimum = 50
    style.AutoPanButton['up'].ymaximum = 50
    style.AutoPanButton['up'].xalign = 0.5
    style.AutoPanButton['up'].yalign = 0.0
    
    style.AutoPanButton['down'].xminimum = 0.8
    style.AutoPanButton['down'].xmaximum = 0.8
    style.AutoPanButton['down'].yminimum = 50
    style.AutoPanButton['down'].ymaximum = 50
    style.AutoPanButton['down'].xalign = 0.5
    style.AutoPanButton['down'].yalign = 1.0
    style.AutoPanButton.background = Solid('#0000')
    
    class AutoScroll(Extra):
        
        def __init__(self, leftLabel='', rightLabel='', upLabel='', downLabel='', distance=100):
            self._leftLabel = leftLabel
            self._rightLabel = rightLabel
            self._upLabel = upLabel
            self._downLabel = downLabel
            self._distance = distance
            self._dx = 0
            self._dy = 0
        
        def Show(self):
            l = self._battle.GetLayer('UI')

            b = Button(Text(self._leftLabel, style=style.PanButtonText['left']), clicked=self.PanLeft, hovered=self.PanLeft, unhovered=self.UnPan, style=style.AutoPanButton['left'])
            renpy.show('_battleAutoPanLeftButton', what=b, layer=l)
            b = Button(Text(self._rightLabel, style=style.PanButtonText['right']), clicked=self.PanRight, hovered=self.PanRight, unhovered=self.UnPan, style=style.AutoPanButton['right'])
            renpy.show('_battleAutoPanRightButton', what=b, layer=l)
            b = Button(Text(self._upLabel, style=style.PanButtonText['up']), clicked=self.PanUp, hovered=self.PanUp, unhovered=self.UnPan, style=style.AutoPanButton['up'])
            renpy.show('_battleAutoPanUpButton', what=b, layer=l)
            b = Button(Text(self._downLabel, style=style.PanButtonText['down']), clicked=self.PanDown, hovered=self.PanDown, unhovered=self.UnPan, style=style.AutoPanButton['down'])
            renpy.show('_battleAutoPanDownButton', what=b, layer=l)

            ui.layer(l)
            ui.timer(0.1, self.CheckPan, repeat=True)
            ui.close()
        
                
        def PanLeft(self):
            self._dx = -1 * self._distance
        def PanRight(self):
            self._dx = self._distance
        def PanUp(self):
            self._dy = -1 * self._distance
        def PanDown(self):
            self._dy = self._distance
        def UnPan(self):
            self._dx = 0
            self._dy = 0
            
        def CheckPan(self):
            if self._dx != 0:
                self._battle.CameraX = self._battle.CameraX + self._dx
            if self._dy != 0:
                self._battle.CameraY = self._battle.CameraY + self._dy
