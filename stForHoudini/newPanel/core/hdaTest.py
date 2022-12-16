import os


def cleanUp():
    pass



def flush():


def TextureArray2Mat(kwargs):
    currentOp = kwargs["node"]
    texture_array_folder_path = currentOp.parm("./Texture_Array_Path")
    if (texture_array_folder_path):
        dir_name = texture_array_folder_path.eval()
        if os.path.exists(dir_name) :
            texture_list = os.listdir(dir_name)
            for tex in texture_list :
                full_name = os.path.join(dir_name, tex)
                matNode = currentOp.createNode("matnet")
                matNode.setName(tex.split(".")[0])
                shaderNode = matNode.createNode("principledshader")
                shaderNode.setParms({"basecolor_useTexture" : 1,
                                     "basecolor_texture"    : full_name})






def run():
    pass

