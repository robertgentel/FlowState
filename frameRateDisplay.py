import bge.logic as logic
cont = logic.getCurrentController()
own = cont.owner
own['Text'] = logic.getAverageFrameRate()