import hou
import os





# replace Your Folder Path With path

def DownloadFolderPath():
    path = "D:\\bridg\\Downloaded" # replace Your Folder Path With path 
    return path








print('--------------------------------------------------------')
print('--------------------------------------------------------')
print('--------------------------------------------------------')



print('--------------------------------------------------------')
print('--------------------------------------------------------')
print('--------------------------------------------------------')


download_path = DownloadFolderPath()



folders = os.listdir(download_path)

def search_files_by_extension(start_path, target_extension):
    result_files = []
    files_list=[]
    
    for root, dirs, files in os.walk(start_path):
        for file in files:
            if file.endswith(target_extension):
                result_files.append(os.path.join(root, file))
                files_list.append(file)
    
    return result_files, files_list

abc_list = search_files_by_extension(download_path,'.abc')
fbx_list = search_files_by_extension(download_path,'.fbx')
obj_list = search_files_by_extension(download_path,'.obj')


def display_tree(list):
    ext= ['abc','fbx','obj']
    ls = list
    emp_ls=[]
    for index,i in enumerate(list):
        for f in i:
            emp_ls.append(str(ext[index] +'/' + str(f)))
    return emp_ls

total_file_list = [abc_list[1],fbx_list[1],obj_list[1]]
main_tree_window = display_tree(total_file_list)


#  display tree windows



window_input = hou.ui.selectFromTree(main_tree_window, picked=(), exclusive=False, message=None, title="quixel import", clear_on_cancel=False, width=0, height=0)

# check file format and find file path

if 'abc/' in str(window_input[0]):
    window_input_file_name = str(window_input[0]).replace('abc/','')
    file_format = '.abc'
    file_format_extansion_name ='abc'
elif 'fbx/' in str(window_input[0]):
    window_input_file_name = str(window_input[0]).replace('fbx/','')
    file_format = '.fbx'
    file_format_extansion_name ='fbx'
elif 'obj/' in str(window_input[0]):
    window_input_file_name = str(window_input[0]).replace('obj/','')
    file_format = '.obj'
    file_format_extansion_name ='obj'


def findeFilePath(fileList,file,forment):
    for f in fileList:
        if file in str(f):
            filePath = f
            folder_path = str(filePath).replace(str(file),'')
        else:
            pass
    
    return filePath , folder_path


# export data to main.py

def importFilePath():
    filePath = findeFilePath(search_files_by_extension(download_path,file_format)[0],window_input_file_name,file_format)
    return filePath


def texture_list():
    
    filePathparentDir = os.path.dirname(os.path.dirname(importFilePath()[1]))
    texture_list = search_files_by_extension(filePathparentDir,'.exr')
    return texture_list


fileName = str(str(window_input[0]).replace(str(file_format_extansion_name)+'/',''))

obj = hou.node('/obj/')
geo = obj.createNode('geo',fileName)


# alembic_create and par set
if file_format == ".abc":
    file = geo.createNode('alembic',fileName)
    file.parm('fileName').set(importFilePath()[0])
else:
    file = geo.createNode('file',fileName)
    file.parm('file').set(importFilePath()[0])
print('create_import_node inside obj....')


# material node
material_assing = geo.createNode('material',"assing_material")
material_assing.setNextInput(file)

# out null
out_null = geo.createNode("null",'out_'+ fileName)
out_null.setNextInput(material_assing)
out_null.setRenderFlag(1)

# render_flage_node
display_flag_null = geo.createNode('null','display_flag')
display_flag_null.setDisplayFlag(1)

# layout network
geo.layoutChildren()

# Config Mat Network

mat  = hou.node('/mat/')
shader = mat.createNode('principledshader',"mat_" + fileName)
print('create_principledshader_inside mat....')
# set shader perameters
bascolour = 1
shader.parm('basecolorr').set(bascolour)
shader.parm('basecolorg').set(bascolour)
shader.parm('basecolorb').set(bascolour)
shader.parm('reflect').set(0)

# assing texture in shaders

texture=[]

# print(texture_list())
for t in texture_list()[0]:
    if 'Albedo.exr' in t:
        texture.append(t)
        shader.parm('basecolor_useTexture').set(1)
        path = str(t) #str(str(download_path) + '\\' + str(t))
        shader.parm('basecolor_texture').set(path)

    elif 'Displacement.exr' in t:
        texture.append(t)
        shader.parm('dispTex_enable').set(1)
        path = str(t) #str(str(download_path) + '\\' + str(t))
        shader.parm('dispTex_texture').set(path)

    elif 'Normal.exr' in t:
        texture.append(t)
        shader.parm('baseBumpAndNormal_enable').set(1)
        path = str(t) #str(str(download_path) + '\\' + str(t))
        shader.parm('baseNormal_texture').set(path)

    elif 'Metallic.exr' in t:
        texture.append(t)
        shader.parm('metallic_useTexture').set(1)
        path = str(t) #str(str(download_path) + '\\' + str(t))
        shader.parm('metallic_texture').set(path)
        shader.parm('metallic').set(1)   

    elif 'Roughness.exr' in t:
        texture.append(t)
        shader.parm('rough_useTexture').set(1)
        path = str(t) #str(str(download_path) + '\\' + str(t))
        shader.parm('rough_texture').set(path)
        shader.parm('rough').set(1)



    else:
        pass






# assing shader to material assing node
    
material_assing.parm('shop_materialpath1').set(str(shader.path()))





print('--------------------------------------------------------')
print('--------------------------------------------------------')
print('--------------------------------------------------------')
print('texture assing done.....')
print('--------------------------------------------------------')
print('--------------------------------------------------------')

print('..............Thank You For using quixel import script..............')

print('--------------------------------------------------------')
print('--------------------------------------------------------')

print('..............Developed By Vivek Rakholiya..............')
print('..............Email :- vivekrakholiya53@gmail.com ..............')

print('--------------------------------------------------------')
print('--------------------------------------------------------')
