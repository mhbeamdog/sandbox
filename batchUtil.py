import unreal

'''
    Returns all assets selected in Content Browser
'''
def get_selected_assets():
    selected_assets = unreal.EditorUtilityLibrary.get_selected_assets()
    return selected_assets

'''
    Returns all assets in project
'''
def get_all_assets():
    all_assets = unreal.AssetRegistryHelpers.get_asset_registry().get_all_assets()
    return all_assets

'''
    Returns all materials in project
'''
def get_all_materials():
    all_assets = get_all_assets()
    materials = [x for x in all_assets if x.asset_class == 'Material']
    return materials

'''
 Replace material on mesh
'''
def replace_materials(original_material, replace_material):
    selectedAssets = get_selected_assets()
    actor_names = []

    new_material = unreal.load_asset(replace_material)

    with unreal.ScopedEditorTransaction("Replace materials") as trans:
        #redraw_skeletal_meshes = False
        for asset in selectedAssets:
            if str(asset.get_class().get_fname()) == "StaticMesh":
                num_mats = unreal.EditorStaticMeshLibrary.get_number_materials(asset)
                for x in range(num_mats):
                    material = asset.get_material(x).get_path_name()
                    if material == original_material:
                        unreal.SystemLibrary.transact_object(asset)
                        asset.set_material(x, new_material)
            elif str(asset.get_class().get_fname()) == "SkeletalMesh":
                is_mat_replaced = replace_skeletal_materials(asset, new_material, original_material)
                if is_mat_replaced:
                    actor_names.append(asset.get_path_name())
                    #redraw_skeletal_meshes = True
        ''' 
        if redraw_skeletal_meshes:
            redraw_skeletal_meshes(actor_names)

        ''' 

def replace_skeletal_materials(mesh, new_material, original_material):
    is_material_replaced = False
    mats = mesh.materials
    for x in range(len(mats)):
        mat_interface = mats[x].get_editor_property('material_interface')
        material = mat_interface.get_path_name()
        if material == original_material:
            new_mat = unreal.SkeletalMaterial(material_interface = new_material, material_slot_name = mats[x].get_editor_property('material_slot_name'), uv_channel_data = mats[x].get_editor_property('uv_channel_data'))
            unreal.SystemLibrary.transact_object(mesh)
            mats[x] = new_mat
            is_material_replaced = True
    return is_material_replaced

'''
    This might be a bit heavy handed, all children of old material become children of new mat 
'''
def swap_material_parent(old_mat_name, new_mat_name):
    old_material = unreal.load_asset(old_mat_name)
    #print("Old material: ", old_material.get_name())
    new_material = unreal.load_asset(new_mat_name)
    #print("New material: ", new_material.get_name())

    child_materials = unreal.MaterialEditingLibrary.get_child_instances(old_material)
    for child in child_materials:
        unreal.MaterialEditingLibrary.set_material_instance_parent(child.get_asset(), new_material)


#swap_material_parent("/Game/BattleAxe/Rendering/Materials/CharacterShader/M_CharacterDualBasePass.M_CharacterDualBasePass", "/Game/BattleAxe/Rendering/Materials/CharacterShader/M_CharacterDualBasePass_Update.M_CharacterDualBasePass_Update")

