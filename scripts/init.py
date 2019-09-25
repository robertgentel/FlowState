import bge
from scripts.gameUtils import utils
render = bge.render
logic = bge.logic
logic.utils = utils()

logic.loadGlobalDict()

logic.globalDict['sceneHistory'] = []
#logic.utils.setDefaultState()
logic.saveGlobalDict()
logic.utils.setMode(logic.utils.MODE_MENU)

profileIndex = logic.globalDict['currentProfile']
profiles = logic.globalDict['profiles']
profile = profiles[profileIndex]
graphicsSettings = profile['graphicsSettings']

shaders = graphicsSettings['shaders']
shading = graphicsSettings['shading']
specularity = graphicsSettings['specularity']
shadows = graphicsSettings['shadows']
frameRate = graphicsSettings['frameRate']

render.showFramerate(frameRate)
#render.setGLSLMaterialSetting("lights",shading)
#render.setGLSLMaterialSetting("shaders",specularity)
#render.setGLSLMaterialSetting("shadows",shadows)

print("INIT!!!!")